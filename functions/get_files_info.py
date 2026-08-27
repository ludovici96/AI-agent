import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, directory))

        valid_target_dir = os.path.commonpath([abs_working_dir, target_path]) == abs_working_dir
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        lines = []

        for name in os.listdir(target_path):

            full_path = os.path.join(target_path, name)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)

            lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f'Error: {str(e)}'