import xbmcaddon

class Addon:
    def __init__(self, addonID):
        self.__addon = xbmcaddon.Addon(id=addonID)
        self.Update()

    def OpenSettings(self):
        self.__addon.openSettings()

    def Update(self):
        self.__name = self.__addon.getAddonInfo('name')
        self.__icon = self.__addon.getAddonInfo('icon')
        self.__language = self.__addon.getLocalizedString
        self.__path = self.__addon.getAddonInfo('path')
        self.__dsPath = self.__addon.getSetting("ds.path")
        self.__dsSecured = self.__addon.getSetting("ds.secured")[0].upper() == "T"
        self.__dsUsername = self.__addon.getSetting("ds.username")
        self.__dsPassword = self.__addon.getSetting("ds.password")

    @property
    def Name(self): return self.__name
    @property
    def Icon(self): return self.__icon
    @property
    def Language(self): return self.__language
    @property
    def Path(self): return self.__path
    @property
    def DSPath(self): return self.__dsPath
    @property
    def IsSecured(self): return self.__dsSecured
    @property
    def Username(self): return self.__dsUsername
    @property
    def Password(self): return self.__dsPassword