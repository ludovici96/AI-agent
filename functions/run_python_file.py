import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        valid_target = os.path.commonpath([abs_working_dir, target_path]) == abs_working_dir
        
        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'



        command = ["python", target_path]

        if args:
            command.extend(args)


        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )


        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")

        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

        final_output = "\n".join(output)

        return final_output


    except Exception as e:
        return f"Error: executing Python file: {e}"
