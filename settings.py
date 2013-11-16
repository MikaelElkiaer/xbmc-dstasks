class Settings(self, addon):
    self.__dsPath = addon.getSetting("ds.path")
    self.__dsSecured = addon.getSetting("ds.secured")[0].upper() == "T"
    self.__dsUsername = addon.getSetting("ds.username")
    self.__dsPassword = addon.getSetting("ds.password")

    @property
    def Path(self): return self.__dsPath
    @property
    def IsSecured(self): return self.__dsSecured
    @property
    def Username(self): return self.__dsUsername
    @property
    def Password(self): return self.__dsPassword