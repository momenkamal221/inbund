"""This module contains the utils that are only specific for pkgmrgr
    also to import the from the package with lower syntax like `inbund.pkgmgr.desired_method() instead of inbund.pkgmgr.utils.desired_method() by importing it in __init__.py
"""
import subprocess
def get_package_manager():
    # Check if apt is available (Debian/Ubuntu-based)
    apt_check = subprocess.run(['which', 'apt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if apt_check.returncode == 0:
        return 'apt'

    # Check if rpm is available (Red Hat-based)
    rpm_check = subprocess.run(['which', 'dnf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if rpm_check.returncode == 0:
        return 'dnf'

    # Check if pacman is available (Arch Linux)
    pacman_check = subprocess.run(['which', 'pacman'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if pacman_check.returncode == 0:
        return 'pacman'

    # Check if Zypper is available (openSUSE)
    zypper_check = subprocess.run(['which', 'zypper'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if zypper_check.returncode == 0:
        return 'zypper'


    # If none of the package managers are found, return None
    return None

def execute_command(cmd, capture_output=True):
    return subprocess.run(
        cmd, shell=True, text=True, capture_output=capture_output)
