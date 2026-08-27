from functions.get_files_info import get_files_info

directories = [".", "pkg", "/bin", "../"]

for directory in directories:
    label = "current directory" if directory == "." else f"'{directory}' directory"

    print(f"Result for {label}:")
    print(get_files_info("calculator", directory))
    print()