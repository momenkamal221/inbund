import subprocess
from inbund import bucket
from .log import Log
import os
logger=Log()
bucket.logger=logger



def execute_command(cmd, capture_output=True):
    return subprocess.run(
        cmd, shell=True, text=True, capture_output=capture_output)

def run_bash_script(bash_script_path):
    subprocess.run(['bash', bash_script_path])

def import_module(module_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('module', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



def get_names(file_path:str) -> list:
    """Is used to get the packages names or script names and ignores what comes after "#"

    Returns:
        list: list contains the names or a command that starts with a specific prefix ">>>"
    """
    result = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Exclude lines starting with #
                if not line.strip().startswith('#'):
                    # Remove comments at the end of the line
                    line_without_comment = line.split('#')[0].strip()
                    if line.startswith(bucket.commandPrefix):
                        result.append(line_without_comment)
                        continue
                    # Split the line based on spaces and tabs
                    elements = line_without_comment.split()

                    # Remove leading and trailing whitespace from each element
                    elements = [elem.strip() for elem in elements]

                    # Add non-empty elements to the result list
                    result.extend(filter(None, elements))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return result

def get_lines(file_path:str) -> list:
    result = []
    try:
        with open(file_path, 'r') as file:
            for index,line in enumerate(file) :
                if(line.strip()==""):
                    continue
                # Exclude lines starting with #
                if not line.strip().startswith('#'):
                    # Remove comments at the end of the line
                    line_without_comment = line.split('#')[0].strip()
                    
                    result.append({
                        "n":index + 1,
                        "line": line_without_comment
                    })
                    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return result

def choose_option(options):
    # Display options
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    
    # Get user choice
    while True:
        try:
            choice = int(input("Choose an option (number): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")



    
def external_storage_exists() -> bool:
    external_storage_path = f"{bucket.current_bundle.path}/../../storage/"
    return os.path.exists(external_storage_path) and os.path.isdir(external_storage_path)


def file_in_internal(storage_dir:str, file:str) -> tuple:
    internal_file_path = f"{bucket.current_bundle.path}/storage/{storage_dir}/{file}"
    exists_in_internal = os.path.exists(internal_file_path)
    return (
        exists_in_internal,
        internal_file_path if exists_in_internal else ""
    )


def file_in_external(storage_dir:str, file:str) -> tuple:
    external_file_path = f"{bucket.current_bundle.path}/../../storage/{storage_dir}/{file}"
    exists_in_external = os.path.exists(external_file_path)
    return (
        exists_in_external,
        external_file_path if exists_in_external else ""
    )


def get_storage_file(storage_dir:str, file:str) -> tuple:
    exists_in_internal, file_path_internal = file_in_internal(storage_dir, file)
    if exists_in_internal:
        return ("internal", file_path_internal)

    exists_in_external, file_path_external = file_in_external(storage_dir, file)
    if exists_in_external:
        return ("external", file_path_external)

    return ("","")

    
    