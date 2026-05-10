import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key not found")
    
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        function_results =[]
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if function_call_result.parts is None:
                    raise Exception("Parts list is empty")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function response does not exist")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function result does not exist")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(f"Response: {response.text}")
            return
    else: 
        print("Maximum number of iterations reached")
        sys.exit(1)

if __name__ == "__main__":
    main()