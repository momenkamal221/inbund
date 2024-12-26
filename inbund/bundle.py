import os
from datetime import datetime
from .core import (
    install_packages,
    flatpak_install,
    run_command,
    remove_packages,
    update_system,
    refresh_pkgmgr,
    copy_files,
    run_scripts
)
from .utils import (
    import_module,
    get_lines,
    get_names
)

class Bundle:
    def __init__(self,bundle_path:str):
        #check if bundle exists
        if not os.path.exists(bundle_path):
            raise FileNotFoundError(f"{bundle_path} does not exist")
        # to distinguish between last logs and future logs we use the current time and date
        current_time=datetime.now().strftime('%y.%m.%d-%H:%M:%S')
        #make the bundle log dir
        log_dir=f"{bundle_path}/logs/{current_time}"
        os.makedirs(log_dir)
        log_file_path = f"{log_dir}/{current_time}.log"
        
        self.path=bundle_path
        self.log_file_path=log_file_path
        self.log_dir = log_dir
        
        self.packages_definer = f"{bundle_path}/definers/pkgs"
        self.flatpak_definer = f"{bundle_path}/definers/flatpak"
        self.scripts_definer = f"{bundle_path}/definers/scripts"
        self.files_definer = f"{bundle_path}/definers/files"

    
    
    def unpack(self):
        path = self.path
        
        import_module(f"{path}/init.py")
        
        pkgs = self.get_packages()
        install_packages(*pkgs)
        
        flatpaks = self.get_flatpaks()
        flatpak_install(*flatpaks)
        
        scripts = self.get_scripts()
        run_scripts(*scripts)
        
        files = self.get_copy_files()
        copy_files(*files)
        
        import_module(f"{path}/final.py")

    def get_packages(self):
        return get_names(self.packages_definer)
    
    def get_scripts(self):
        return get_names(self.scripts_definer)
    
    def get_flatpaks(self):
        return get_names(self.flatpak_definer)
    
    def get_copy_files(self):
        return get_lines(self.files_definer)
    

    #navigating ljasdf laksdjf
# hjkl be w $0 %
#IA ia
#x R r
