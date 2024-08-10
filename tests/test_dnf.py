from inbund.pkgmgr import dnf,get_package_manager

def test_get_package_manager():
    assert get_package_manager() =="dnf"
    
def test_is_installed():
    assert dnf.is_installed('picom')
