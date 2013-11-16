import xbmcaddon
import urlparse

class Addon:
    def __init__(self, addonID):
        addon = xbmcaddon.Addon(id=addonID)
        self.__name = addon.getAddonInfo('name')
        self.__icon = addon.getAddonInfo('icon')
        self.__language = addon.getLocalizedString

        self.__path = addon.getAddonInfo('path')

    @property
    def Name(self): return self.__name
    @property
    def Icon(self): return self.__icon
    @property
    def Path(self): return self.__path
    @property
    def Handle(self): return self.__handle
    @property
    def Parameters(self): return self.__params
    @property
    def DSPath(self): return self.__dsPath
    @property
    def DSSecured(self): return self.__dsSecured
    @property
    def DSUsername(self): return self.__dsUsername
    @property
    def DSPassword(self): return self.__dsPassword