import os
from .utils import (
    import_module,
    get_names,
    logger
)

from .core import (
    install_packages,
    flatpak_install,
    remove_packages,
    update_system,
    refresh_pkgmgr
)
from datetime import datetime


def unpack(bundle_path):
    
    if not os.path.exists(bundle_path):
        logger.log("Error","Wrong bundle directory.",logger.MessageLevel.ERROR)
        exit()
    
    run_time=datetime.now().strftime('%y.%m.%d-%H:%M:%S')
    log_dir=f"{bundle_path}/logs/{run_time}"
    os.makedirs(log_dir)

    logger.log_dir = log_dir
    logger.log_file_path = f"{log_dir}/{run_time}.log"

    refresh_pkgmgr()
    
    # import_module(f"{bundle_path}/init.py")
    # install_packages("vlc")
    # import_module(f"{bundle_path}/final.py")
    
    


def new(path,bundle_name):
    ...
