from addon import Addon
from gui import GUI

Addon = Addon('script.dstasks')

GUI = GUI('script-dstasks-main.xml', Addon.Path, addon=Addon)
GUI.doModal()
del GUI