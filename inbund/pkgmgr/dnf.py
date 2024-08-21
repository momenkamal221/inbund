from .pkgmgr import Pkgmgr
from .utils import execute_command


class dnf(Pkgmgr):
    def is_installed(package):
        check_installed_cmd = f"dnf list --installed {package}"
        is_installed = execute_command(check_installed_cmd)
        if is_installed.returncode == 0:
            return True
        return False
    def is_available(package):
        check_available_cmd = f"dnf list --available {package}"
        is_available = execute_command(check_available_cmd)
        if is_available.returncode == 0:
            return True
        return False
    def install(package, capture_output=True):
        # Install the package
        install_cmd = f"dnf install -y {package}"
        install_result = execute_command(install_cmd, capture_output)
        if install_result.returncode == 0:
            return True
        return False

    def update():
        update_cmd = f"dnf update -y"
        update = execute_command(update_cmd)
        if update.returncode == 0:
            return True
        return False
    def clear_cache():
        cmd="dnf clean all"
        execute_command(cmd)
        
    def database_update():
        database_update_cmd = f"dnf check-update"
        database_update = execute_command(database_update_cmd)
        #check-update returncode is the number the available updates
        return database_update.returncode
    
    def remove(package, capture_output=True):
        # Install the package
        remove_cmd = f"dnf remove -y {package}"
        remove_result = execute_command(remove_cmd, capture_output)
        if remove_result.returncode == 0:
            return True
        return False
    def get_name():
        return "dnf"
    


