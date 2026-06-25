import os
import subprocess
from functions import get_files_info

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:    
        if "outside" in get_files_info.get_files_info(working_directory, file_path):
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        filePath = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        if os.path.isdir(filePath):
            return f'Error: Cannot execute to "{file_path}" as it is a directory'
        if not os.path.isfile(filePath):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", filePath]
        if args:
            command.extend(args)

        try:
            proc = subprocess.run(command,cwd=working_directory,capture_output=True,text=True,timeout=30,)
        except subprocess.TimeoutExpired:
            return "Error: Process timed out after 30 seconds"

        output = ""
        if proc.stdout:
            output += "STDOUT: " + proc.stdout
        if proc.stderr:
            output += "STDERR: " + proc.stderr
        if proc.returncode != 0:
            output += f"\nProcess exited with code {proc.returncode}"
        return output if output else "No output produced"
    except Exception as e:
        f"Error: executing Python file: {e}"