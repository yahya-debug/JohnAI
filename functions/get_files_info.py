from google.genai import types
import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, directory))

        validate_path = os.path.commonpath([abs_path, full_path]) == abs_path

        if validate_path == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        

        listin = os.listdir(full_path)
        output = []
        for item in listin:
            output.append(f"- {item}: file_size={os.path.getsize(os.path.normpath(os.path.join(full_path, item)))}, is_dir={os.path.isdir(os.path.normpath(os.path.join(full_path, item)))}")
        return "\n".join(output)
    except FileNotFoundError:
        return f'Error: The path "{directory}" does not exist.'
        
    except NotADirectoryError:
        return f'Error: "{directory}" is a file, not a directory.'
        
    except PermissionError:
        return f'Error: Permission denied to access "{directory}".'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)