from addon import Addon
from query import Mode, TaskAction
import xbmcgui
import xbmcplugin

class Display:
    def __init__(self, addon):
        self.__addon = addon

    def BuildDirectory(self):
        xbmcplugin.endOfDirectory(self.__addon.Handle)

    def MainMenu(self):
        self.__addDirectory("Active Downloads", "mode=%s" % Mode.ActiveDownloads, "")
        self.__addDirectory("Unsorted Downloads", "mode=%s" % Mode.UnsortedDownloads, "")

    def ActiveDownloads(self):
        from tasks import DS, DSTask

        ds = DS(self.__addon.DSPath, self.__addon.DSSecured, self.__addon.DSUsername, self.__addon.DSPassword)

        for task in ds.taskList:
            self.__addTask(task, "")

    def UnsortedDownloads(self):
        from unsorted import Unsorted

        unsorted = Unsorted(self.__addon.DSPath, self.__addon.DSUsername, self.__addon.DSPassword, "download")

        list = unsorted.ListContent()

    def __addDirectory(self, name, url, iconimage):
        itemURL = "%s?%s" % (self.__addon.Path, url)
        listItem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        listItem.setInfo(type="Video", infoLabels={"Title": name })
    
        contextMenuItems = []
        listItem.addContextMenuItems(contextMenuItems, replaceItems=True)
        xbmcplugin.addDirectoryItem(self.__addon.Handle, url=itemURL, listitem=listItem, isFolder=True)

    def __addTask(self, task, iconimage):
        url = "%s?mode=%s&action=%s&id=%s" % (self.__addon.Path, Mode.ActiveDownloads, "%s", "%s")
        listItem = xbmcgui.ListItem(task.Title[0:60] + "..." if len(task.Title) > 60 else task.Title, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listItem.setInfo( type="Video", infoLabels={ "Title": task.Title } )

        #listitem.addContextMenuItems([('Theater Showtimes', 'XBMC.RunScript(special://home/scripts/showtimes/default.py,Iron Man)',)])

        contextMenuItems = []
        if task.Status == "paused":
            contextMenuItems.append(('Resume', url % ("resume", task.ID)))
        else:
            contextMenuItems.append(('Pause', url % ("pause", task.ID)))
        contextMenuItems.append(('Stop', url % ("stop", task.ID)))
        contextMenuItems.append(('Delete', url % ("delete", task.ID)))
        listItem.addContextMenuItems(contextMenuItems, replaceItems=True)
    
        xbmcplugin.addDirectoryItem(self.__addon.Handle, "%s?mode=%s" % (self.__addon.Path, Mode.Pass), listitem=listItem, isFolder=False)