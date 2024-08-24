""" here is used to store value has to be accessible
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from inbund.bundle import Bundle 

import inbund

#this reference can be changed a lot, so when importing it you have to import it like "import .utils or from inbund import utils" then utils.current_bundle not "from .utils import current_bundle"
current_bundle:Bundle = None 
commandPrefix=">>>"