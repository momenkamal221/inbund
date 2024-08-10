from .utils import (
    get_package_manager
    )
from .dnf import dnf
#check interfaces
dnf()
#code

#specify current pkgmgr
name=get_package_manager()
if name == "dnf":
    current_pkgmgr=dnf

