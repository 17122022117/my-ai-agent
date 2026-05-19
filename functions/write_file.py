import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        working_dir_comm = os.path.normpath(working_dir_abs)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    else:
        print(f'Success: "{file_path}" is within the working directory')
        print(working_dir_comm)
        os.makedirs(working_dir_comm, exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'