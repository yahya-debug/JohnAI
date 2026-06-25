from functions import get_files_info
import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        if "outside" in get_files_info.get_files_info(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        filePath = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        if not os.path.isfile(filePath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        f = open(filePath)
        content = f.read(MAX_CHARS)

        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        f.close()
        return content
    except PermissionError:
        return f'Error: Permission denied to read file "{file_path}".'
    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" because it is not a valid text file (encoding error).'
    except FileNotFoundError:
        return f'Error: File "{file_path}" vanished or was deleted.'
    except Exception as e:
        return f'Error: An unexpected error occurred while reading "{file_path}": {e}'
        