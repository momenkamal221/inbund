from . import bundle
from .utils import logger
from inbund import bucket


def unpack(*bundle_paths):
    for bundle_path in bundle_paths:
        bundle = setup_new_bundle(bundle_path)
        bundle.unpack()
        

def setup_new_bundle(bundle_path:str):
    new_bundle=bundle.Bundle(bundle_path)
    bucket.current_bundle = new_bundle
    # assign bundle log dir in the logger object
    logger.log_file_path = new_bundle.log_file_path
    return new_bundle
    
    


def new(path,bundle_name):
    ...
