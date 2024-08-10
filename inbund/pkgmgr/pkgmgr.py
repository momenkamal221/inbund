from abc import ABC, abstractmethod

class Pkgmgr(ABC):
    
    @abstractmethod
    def is_installed(package): 
        pass
    
    @abstractmethod
    def is_available(package):
        pass
    
    @abstractmethod
    def install(package):
        pass
    
    @abstractmethod
    def check_update():
        pass
    
    @abstractmethod
    def update():
        pass
    
    @abstractmethod
    def clear_cache():
        pass
    
    
    @abstractmethod
    def database_update() :
        pass
    
    @abstractmethod
    def remove(package):
        pass