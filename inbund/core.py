"""contains the core install script
"""
from datetime import datetime

from inbund.pkgmgr import current_pkgmgr
from .utils import (
    execute_command,
    logger,
    choose_option,
    commandPrefix
    )



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
        
        if out_on_error:print(executed_command.stderr)
        
        run_time=datetime.now().strftime('%y.%m.%d-%H:%M:%S.%f')
        with open(f"{logger.log_dir}/cmd-{run_time}", "a") as command_out_file:
            command_out_file.write(f"{commandPrefix} {cmd}\n{executed_command.stderr}")



def remove_packages(*packages):
    task_name="Remove"
    for package in packages:
        # Check if the package is already removed
        if not current_pkgmgr.is_installed(package):
            logger.log(task_name,f"{package}: Already not installed.",logger.MessageLevel.SUCCESS,log_to_file=True)
            continue
        # remove the package
        is_package_removed = logger.loading(
            task_name,
            f"removing {package}",
            logger.MessageLevel.IN_PROGRESS,
            lambda: current_pkgmgr.remove(package)
            )
        
        if is_package_removed:
            logger.log(task_name,f"{package}: Successfully removed.",logger.MessageLevel.SUCCESS,log_to_file=True)
        else:
            logger.log(task_name,f"{package}: Failed to remove.",logger.MessageLevel.ERROR,log_to_file=True)




def install_packages(*packages):
    task_name="Install"
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
    task_name="Flatpak"

    for app_id in apps_id:
        if app_id.startswith(commandPrefix):
            cmd = app_id[len(commandPrefix):]
            run_command(cmd)
            continue
        splitted_app_id=f"{app_id}@".split("@") if not app_id.endswith("@") else app_id.split("@")
        # Run the Flatpak install command
        app_id =  splitted_app_id[0]
        remote = splitted_app_id[1]
        
        #check if the app is installed
        if execute_command(f"flatpak list --columns=application | grep {app_id}").stdout.strip()==app_id:
            logger.log(task_name,f"{app_id}: Already installed.",logger.MessageLevel.SUCCESS,log_to_file=True)
            continue
        
        #check if app has more remotes and no remotes is assigned 
        remotes = execute_command(f"flatpak search {app_id} --columns=remotes | awk \'{{print $NF}}\'").stdout.strip().split(",")
        
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
            print(executed_command.stderr)
