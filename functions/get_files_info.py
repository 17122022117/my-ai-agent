import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(working_dir_abs):
        return f'Error: "{directory}" is not a directory'
    else:
        print(f'Success: "{directory}" is within the working directory')
        string_list = []
        for file in os.listdir(os.path.abspath(target_dir)):
            try:
                file_abs_dir = os.path.join(target_dir, file)
                string_list.append(f"- {file}: file_size={os.path.getsize(file_abs_dir)} bytes, is_dir={os.path.isdir(file_abs_dir)}")
            except Exception as e:
                return f"Error: {e}"
        return "\n".join(string_list)