import subprocess
from .log import Log
from inbund.pkgmgr import current_pkgmgr
from datetime import datetime
logger=Log()
commandPrefix=">>>"


def execute_command(cmd):
    return subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



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
                    if line.startswith(commandPrefix):
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



def run_command(cmd:str):
    out_on_error = cmd.endswith("2>")
    if out_on_error: cmd=cmd[:-2]
    
    executed_command=logger.loading(
        "cmd",
        f"Executing the command: {cmd}",
        logger.MessageLevel.IN_PROGRESS,
        lambda: execute_command(cmd)
    )
    if executed_command.returncode==0:
        logger.log("cmd",f"{cmd}: Executed successfully.",logger.MessageLevel.SUCCESS,log_to_file=True)
    else:
        logger.log("cmd",f"{cmd}: Failed to execute.",logger.MessageLevel.ERROR,log_to_file=True)
        
        if out_on_error:print(executed_command.stderr.decode('utf-8'))
        
        run_time=datetime.now().strftime('%y.%m.%d-%H:%M:%S.%f')
        with open(f"{logger.log_dir}/cmd-{run_time}", "a") as command_out_file:
            command_out_file.write(f"{commandPrefix} {cmd}\n{executed_command.stderr.decode('utf-8')}")



def install_packages(*packages):
    task_name="install"
    for package in packages:
        if package.startswith(commandPrefix):
            cmd = package[len(commandPrefix):]
            run_command(cmd)
            continue

        # Check if the package is already installed
        if current_pkgmgr.is_installed(package):
            logger.log(task_name,f"{package}: Already installed.",logger.MessageLevel.SUCCESS,log_to_file=True)
            continue
        # Check if the package is available in dnf
        if not current_pkgmgr.is_available(package):
            logger.log(task_name,f"{package}: Is not available.",logger.MessageLevel.ERROR,log_to_file=True)
            continue
        
        # Install the package
        is_package_installed = logger.loading(
            task_name,
            f"installing {package}",
            logger.MessageLevel.IN_PROGRESS,
            lambda: current_pkgmgr.install(package)
            )
        
        if is_package_installed:
            logger.log(task_name,f"{package}: Successfully installed.",logger.MessageLevel.SUCCESS,log_to_file=True)
        else:
            logger.log(task_name,f"{package}: Failed to install.",logger.MessageLevel.ERROR,log_to_file=True)



def flatpak_install(*apps_id):
    task_name="flatpak"

    for app_id in apps_id:
        if app_id.startswith(commandPrefix):
            cmd = app_id[len(commandPrefix):]
            run_command(cmd)
            continue
        splited_app_id=f"{app_id}@".split("@") if not app_id.endswith("@") else app_id.split("@")
        # Run the Flatpak install command
        app_id =  splited_app_id[0]
        remote = splited_app_id[1]
        
        #check if the app is installed
        if execute_command(f"flatpak list --columns=application | grep {app_id}").stdout.decode('utf-8').strip()==app_id:
            logger.log(task_name,f"{app_id}: Already installed.",logger.MessageLevel.SUCCESS,log_to_file=True)
            continue
        
        #check if app has more remotes and no remotes is assigned 
        remotes = flatpak_get_remotes(app_id)
        
        if len(remotes)==1:remote=remotes[0]
        
        if len(remotes)>1 and remote=="" or not remote in remotes:
            if not remote in remotes: print(f"There is no remote called \"{remote}\" for \"{app_id}\"")
            print("Which remote do you want to use?")
            remote=choose_option(remotes)

        
        executed_command=logger.loading(
            task_name,
            f"{app_id}: Installing",
            logger.MessageLevel.IN_PROGRESS,
            lambda: execute_command(f'flatpak install {remote} {app_id} -y ')
        )
        if executed_command.returncode==0:
            logger.log(task_name,f"{app_id}: Successfully installed.",logger.MessageLevel.SUCCESS,log_to_file=True)
        else:
            logger.log(task_name,f"{app_id}: Failed to install.",logger.MessageLevel.ERROR,log_to_file=True)
            print(executed_command.stderr.decode('utf-8'))


def flatpak_get_remotes(appID):
    return execute_command(f"flatpak search {appID} --columns=remotes | awk \'{{print $NF}}\'").stdout.decode('utf-8').strip().split(",")


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
 