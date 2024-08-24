import subprocess
from inbund import bucket
from .log import Log
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



