import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file relative to the working directory, optionally with command-line arguments",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of file to run, relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of optional command-line arguments",
                items=types.Schema(type=types.Type.STRING)
            )        
        },    
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]

        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=abs_working_dir, capture_output=True, timeout=30, text=True)
        output_str = ""
        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}"
        if not completed_process.stdout and not completed_process.stderr:
            output_str += "No output produced"
        else:
            output_str += f"STDOUT:{completed_process.stdout}"
            output_str += f"STDERR:{completed_process.stderr}"
        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"