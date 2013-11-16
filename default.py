from addon import Addon
from gui import GUI

Addon = Addon('script.dstasks')

w = GUI('script-dstasks-main.xml', Addon.Path, 'Default')
w.doModal()
del w