"""contains the core install script
"""
from datetime import datetime
import time
import re
import shutil
import os
from inbund.pkgmgr import current_pkgmgr
from .utils import (
    execute_command,
    choose_option,
    logger,
    get_storage_file,
    run_bash_script
    )
from inbund import bucket
from inbund.bucket import commandPrefix, STORAGE_DIRS


def run_command(cmd:str):
    out_on_error = cmd.endswith("2>")
    if out_on_error: cmd=cmd[:-2]
    task_name="cmd"
    executed_command=logger.loading(
        task_name,
        f"Executing the command: {cmd}",
        logger.MessageLevel.IN_PROGRESS,
        lambda: execute_command(cmd)
    )

    if executed_command.returncode==0:
        logger.log(task_name,f"{cmd}: Executed successfully.",logger.MessageLevel.SUCCESS,log_to_file=True)
    else:
        logger.log(task_name,f"{cmd}: Failed to execute.",logger.MessageLevel.ERROR,log_to_file=True)
        
        if out_on_error:print(executed_command.stderr)
        
        run_time=datetime.now().strftime('%y.%m.%d-%H:%M:%S.%f')
        if bucket.current_bundle != None:
            with open(f"{bucket.current_bundle.log_dir}/cmd-{run_time}", "a") as command_out_file:
                command_out_file.write(f"{commandPrefix} {cmd}\n{executed_command.stderr}")



def run_scripts(*scripts):
    task_name="Bash"
    
    for script_name in scripts:
        sh_file=False
        location, src = get_storage_file(STORAGE_DIRS.scripts.value,f"{script_name}.sh")
        if src:
            sh_file=True
        if not sh_file:
            location, src = get_storage_file(STORAGE_DIRS.scripts.value,f"{script_name}")            
        if not src:
            logger.log(task_name,f"Script has run:  {script_name} is not found",logger.MessageLevel.ERROR,log_to_file=True)
            continue
        
        if bucket.tmux_flag:
            logger.loading(
                task_name,
                f"Running the script: {location} - {script_name}",
                logger.MessageLevel.IN_PROGRESS,
                lambda:run_bash_script(src)
            )
            logger.log(task_name,f"Script has run: {location} - {script_name}",logger.MessageLevel.SUCCESS,log_to_file=True)
        
        else:
            logger.log(
                task_name,
                f"Running the script: {location} - {script_name}",
                logger.MessageLevel.IN_PROGRESS,
                log_to_file=True
            )
            run_bash_script(src)
            logger.log(task_name,f"Script has run: {location} - {script_name}",logger.MessageLevel.SUCCESS,log_to_file=True)
        

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
        is_pkg_available = logger.loading(
            "Checking",
            f"Checking if {package} is available",
            logger.MessageLevel.IN_PROGRESS,
            lambda: current_pkgmgr.is_available(package)
        )
        
        if not is_pkg_available:
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



def update_system():
    task_name="Update"
    is_updated=logger.loading(
        task_name,
        f"System update",
        logger.MessageLevel.IN_PROGRESS,
        lambda: current_pkgmgr.update()
        )
    
    if is_updated:
        logger.log(task_name,f"Update completed successfully",logger.MessageLevel.SUCCESS,log_to_file=True)
    else:
        logger.log(task_name,f"failed to update.",logger.MessageLevel.ERROR,log_to_file=True)
    
    return is_updated



def refresh_pkgmgr():
    """basically removes cache and update database
    """
    
    task_name="Update"
    def refresh():
        current_pkgmgr.clear_cache()
        return current_pkgmgr.database_update()
        
    updates_number=logger.loading(
        task_name,
        f"refreshing {current_pkgmgr.get_name()}" ,
        logger.MessageLevel.IN_PROGRESS,
        refresh
        )
    logger.log(task_name,f"Found {updates_number} available updates",logger.MessageLevel.INFO,log_to_file=True)
    

def copy_files(*prompts):

    task_name = "Copy"
    pattern = r"^'(.+)'\s*(|r)(-|--)>\s*'(.+)'$"
    
    for prompt in prompts:
        if prompt['line'].startswith(commandPrefix):
            cmd = prompt['line'][len(commandPrefix):]
            run_command(cmd)
            continue
        match = re.match(pattern, prompt['line'])
        if not match:
            logger.log(task_name,f"Line {prompt['n']}: Syntax is not correct -> {prompt['line']}",logger.MessageLevel.ERROR,log_to_file=True)
            continue
        file_name = match.group(1).strip()  # Extract and trim the src path
        location, src = get_storage_file(STORAGE_DIRS.files.value,file_name)
        if not src: #if empty
            logger.log(task_name,f"{file_name} is not found",logger.MessageLevel.ERROR,log_to_file=True)
            continue
        dst = match.group(4).strip()
        allow_overwrite=match.group(3) == "-"
        allow_recursive=match.group(2) != "r"
        try:
            # Copy the file from src to dst
            if not allow_overwrite and os.path.exists(f"{dst}/{file_name}"):
                response = input(f"Over write the file \"{dst}/{file_name}\" (y/n): ").strip().lower()
                if response == "n" or not response == "":
                    logger.log(task_name,f"Will not overwrite \"{dst}/{file_name}\"",logger.MessageLevel.WARNING,log_to_file=True)
                    continue
            if not allow_recursive and not os.path.exists(dst):
                response = input(f"The directory \"{dst}/\" is not exists... create the path? (y/n): ").strip().lower()
                if response == "n" or not response == "":
                    logger.log(task_name,f"Will not create the path \"{dst}\"",logger.MessageLevel.WARNING,log_to_file=True)
                    continue
                
            try: os.makedirs(dst, exist_ok=True)
            except:pass
            
            logger.loading(
                task_name,
                f"Coping {file_name} to {dst}" ,
                logger.MessageLevel.IN_PROGRESS,
                lambda:shutil.copy(src, os.path.abspath(os.path.expanduser(dst)))
            )
            logger.log(task_name,f"{location} - {prompt['line']}",logger.MessageLevel.SUCCESS,log_to_file=True)
        except FileNotFoundError:
            logger.log(task_name,f"{file_name} is not found!",logger.MessageLevel.ERROR,log_to_file=True)
        except PermissionError:
            logger.log(task_name,f"No permission granted",logger.MessageLevel.ERROR,log_to_file=True)
        except Exception as e:
            logger.log(task_name,f"An unexpected error occurred: {e}",logger.MessageLevel.ERROR,log_to_file=True)