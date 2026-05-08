import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
    valid_file = os.path.isfile(target_file)
    if valid_target_dir == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    

    try:
        if valid_file == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"