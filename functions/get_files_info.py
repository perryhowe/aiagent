import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        
        item_string = ""

        for item in os.listdir(target_dir):
            file_size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))
            item_string += f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return item_string
    
    except Exception as e:
        return f"Error: {e}"