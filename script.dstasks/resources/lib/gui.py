import xbmcgui
import threading
from tasks import DS, DSTask

KEY_BUTTON_BACK = 275
KEY_MENU_ID = 92
KEY_PLAYPAUSE = 61520
KEY_STOP = 61528

ID_TASK_LIST = 51

class GUI(xbmcgui.WindowXML):
    def __init__(self, xmlFilename, scriptPath, addon):
        self.__addon = addon
        super(GUI, self).__init__()

    def onInit(self):
        self.__thread = threading.Thread(target=self.__update)
        self.__items = []
        self.__connect()

    def __connect(self):
        def loginFailed():
            if xbmcgui.Dialog().yesno("DS Error", "Unable to Connect", "Try another host?"):
                self.__addon.openSettings()
                self.__connect()
            else:
                self.__close()

        self.__ds = DS(self.__addon.getSetting("ds.path"), self.__addon.getSetting("ds.secured"))

        p = xbmcgui.DialogProgress()
        p.create("DS", "Connecting to DS on '%s'" % self.__addon.getSetting("ds.path"))
        p.update(25)

        if not self.__ds.Login(self.__addon.getSetting("ds.username"), self.__addon.getSetting("ds.password")):
            loginFailed()
            return
        else:
            if p.iscanceled():
                p.close()
                self.__close()
            p.update(75, "Getting tasks from DS")
            self.__getTasks()
            if p.iscanceled():
                p.close()
                self.__close()
            else:
                p.close()
                self.__thread.start()

    def __update(self):
        self.running = True

        while self.running:
            self.__getTasks()
            if not self.running:
                break;

    def __getTasks(self):
        tasks = self.__ds.GetTaskList()
        taskList = self.getControl(ID_TASK_LIST)

        count = len(tasks)

        if count != len(self.__items):
            taskList.reset()
            self.__items = [xbmcgui.ListItem() for u in range(count)]
            taskList.addItems(self.__items)

        for task, item in zip(tasks, self.__items):
            size = float(task.Size) / 1000000000.0
            sizeDownloaded = float(task.SizeDownloaded) / 1000000000.0
            sizeUploaded = float(task.SizeUploaded) / 1000000000.0
            percentDownload = (float(task.SizeDownloaded) / float(task.Size)*100)
            percentUpload = (float(task.SizeUploaded) / float(task.Size)*100)
            
            item.setLabel("%s (%.2f Gb / %.2f Gb)" % (task.Title, sizeUploaded if percentDownload == 100.0 else sizeDownloaded, size))
            item.setIconImage("status/%s.png" % task.Status)
            
            item.setProperty("ID", task.ID)
            item.setProperty("Title", task.Title)
            item.setProperty("Status", task.Status)

            item.setProperty("TaskDownProgress", "%.2f" % percentDownload)
            item.setProperty("DownloadFinished", str(1 if (percentDownload == 100.0) else 0))
            item.setProperty("TaskUpProgress", "%.2f" % percentUpload)
            item.setProperty("SpeedDownload", "%d" % (task.SpeedDownload / 1000))
            item.setProperty("SpeedUpload", "%d" % (task.SpeedUpload / 1000))

            # HACK: force redraw
            if item.getLabel2() == "flip":
                item.setLabel2("flop")
            else:
                item.setLabel2("flip")

    def __close(self):
        self.running = False
        if not self.__thread.ident == None:
            self.__thread.join()
        xbmcgui.WindowXML.close(self)

    def onClick(self, controlID):
        selectedTask = self.getControl(ID_TASK_LIST).getSelectedItem()

    def onFocus(self, controlID):
        pass

    def onAction(self, action):
        selectedTask = self.getControl(ID_TASK_LIST).getSelectedItem()
        taskID = selectedTask.getProperty("ID")
        taskTitle = selectedTask.getProperty("Title")
        taskStatus = selectedTask.getProperty("Status")

        if (action.getButtonCode() == KEY_BUTTON_BACK) or (action.getId() == KEY_MENU_ID):
            self.__close()
        elif action.getButtonCode() == KEY_PLAYPAUSE:
            if taskStatus == "paused":
                self.__ds.Resume(taskID)
            else:
                self.__ds.Pause(taskID)
        elif action.getButtonCode() == KEY_STOP:
            if xbmcgui.Dialog().yesno("Delete task", "Are you sure you want to delete:", taskTitle + " ?"):
                self.__ds.Delete(taskID)