import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        print(f'Success: "{file_path}" is within the working directory')
        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content