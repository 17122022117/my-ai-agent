import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        print(f"Error: {e}")
        return None

    if not valid_target_dir:
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    elif not os.path.isdir(directory):
        print(f'Error: "{directory}" is not a directory')
    else:
        print(f'Success: "{directory}" is within the working directory')