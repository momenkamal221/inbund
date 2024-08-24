import os
from datetime import datetime
from .core import (
    install_packages,
    flatpak_install,
    remove_packages,
    update_system,
    refresh_pkgmgr
)
from .utils import (
    import_module
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
    

    
    
    def unpack(self):
        path = self.path
        import_module(f"{path}/init.py")
        install_packages("vlc")
        import_module(f"{path}/final.py")