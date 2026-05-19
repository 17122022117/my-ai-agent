import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file from specific directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of python file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="File path of python file to run",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        working_dir_comm = os.path.normpath(working_dir_abs)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not target_dir.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    else:
        print(f'Success: "{file_path}" is within the working directory')
        command = ["python", target_dir]
        if args is not None:
            command.extend(args)
        try:
            process = subprocess.run(command, cwd=working_dir_comm, capture_output=True, text=True, timeout=30)
        except Exception as e:
            return f"Error: executing Python file: {e}"
        string_list = []
        if process.returncode != 0:
            string_list.append(f'Process exited with code {process.returncode}')
        elif process.stdout is None and process.stderr is None:
            string_list.append(f'No output produced')
        else:
            string_list.append(f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}')
        return "".join(string_list)
        
            
