import os
from . import utils
from .utils import (
    import_module,
    install_packages,
    flatpak_install,
    get_names,
    logger
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

    # import_module(f"{bundle_path}/init.py")
    flatpak_install("it.mijorus.smiledasdasd")
    # import_module(f"{bundle_path}/final.py")
    
    


def new(path,bundle_name):
    ...
