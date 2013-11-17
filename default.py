import xbmc
import xbmcaddon
import os
import sys

__addon = xbmcaddon.Addon(id='script.dstasks')
__name = __addon.getAddonInfo('name')
__icon = __addon.getAddonInfo('icon')
__path = __addon.getAddonInfo('path')
sys.path.append (xbmc.translatePath(os.path.join(__path, 'resources', 'lib' )))

from gui import GUI

GUI = GUI('script-dstasks-main.xml', __path, addon=__addon)
GUI.doModal()
del GUI