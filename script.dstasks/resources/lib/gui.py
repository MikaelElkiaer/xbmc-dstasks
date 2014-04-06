import xbmcgui
import threading
from tasks import DS, DSTask

KEY_BUTTON_BACK = 275
KEY_MENU_ID = 92
ACTION_PAUSE = 79
ACTION_STOP = 13

ID_TASK_LIST = 201

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
                return

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
            done = sizeDownloaded == size
            speed = task.SpeedDownload / 1000

            if done:
                sizeUploaded = float(task.SizeUploaded) / 1000000000.0
                speed = task.SpeedUpload / 1000
            
            item.setLabel(task.Title)
            item.setLabel2("%.2f Gb / %.2f Gb (%.0f Kb/s)" % (sizeUploaded if done else sizeDownloaded, size, speed))
            item.setIconImage("status/%s.png" % task.Status)

            try:
                item.setProperty("Progress", "%.2f" % (float(sizeUploaded / size)*100) if done else (float(sizeDownloaded / size)*100))
            except:
                item.setProperty("Progress", "0.0")

            item.setProperty("ID", task.ID)
            item.setProperty("Title", task.Title)
            item.setProperty("Status", task.Status)

        taskList.setEnabled(count > 0)

    def __close(self):
        self.running = False
        if not self.__thread.ident == None:
            self.__thread.join()
        xbmcgui.WindowXML.close(self)

    def onClick(self, controlID):
      pass

    def onFocus(self, controlID):
        pass

    def onAction(self, action):
        control = self.getControl(ID_TASK_LIST)
        selectedTask = control.getSelectedItem()
        taskID = selectedTask.getProperty("ID")
        taskTitle = selectedTask.getProperty("Title")
        taskStatus = selectedTask.getProperty("Status")

        print action.getId()

        if (action.getButtonCode() == KEY_BUTTON_BACK) or (action.getId() == KEY_MENU_ID):
            self.__close()
        elif action.getId() == ACTION_PAUSE:
            if taskStatus == "paused":
                self.__ds.Resume(taskID)
            else:
                self.__ds.Pause(taskID)
        elif action.getId() == ACTION_STOP:
            if xbmcgui.Dialog().yesno("Delete task", "Are you sure you want to delete?", taskTitle):
                self.__ds.Delete(taskID)
