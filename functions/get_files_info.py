import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    if valid_target_dir == False:
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