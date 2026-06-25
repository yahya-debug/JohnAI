from functions import get_files_info
import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        if "outside" in get_files_info.get_files_info(working_directory, file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        filePath = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        if os.path.isdir(filePath):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        target_dir = os.path.dirname(filePath)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        with open(filePath, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: An unexpected error occurred while reading "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a file at the given path relative to the working directory with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
    