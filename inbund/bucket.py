""" here is used to store value has to be accessible
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from inbund.bundle import Bundle 
from enum import Enum
class STORAGE_DIRS (Enum):
    files = "files"
    scripts = "scripts"
#this reference can be changed a lot, if you want to use it you have to import it like "import .bucket or from inbund import bucket" then bucket.current_bundle not "from .bucket import current_bundle"
current_bundle:Bundle = None 
commandPrefix=">>>"
tmux_flag=False
tmux_server=""