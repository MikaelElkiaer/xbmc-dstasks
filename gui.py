import xbmcgui
import threading
import Queue
from addon import Addon
from tasks import DS, DSTask

KEY_BUTTON_BACK = 275
KEY_MENU_ID = 92

MSG_METHOD = 1
MSG_EXIT = 2

class GUI(xbmcgui.WindowXML):
    def __init__(self, xmlFilename, scriptPath, addon):
        self.__addon = addon
        super(GUI, self).__init__()

    def onInit(self):
        self.__thread = threading.Thread(target=self.__update)
        self.__queue = Queue.Queue()
        self.__items = []
        self.__connect()

    def __connect(self):
        def loginFailed():
            if xbmcgui.Dialog().yesno("DS Error", "Unable to Connect", "Open Settings"):
                self.__addon.OpenSettings()
                self.__addon.Update()
                self.__connect()
            else:
                self.__close()

        self.__ds = DS(self.__addon.DSPath, self.__addon.IsSecured)

        p = xbmcgui.DialogProgress()
        p.create("DS", "Connecting to DS on %s..." % self.__addon.DSPath)
        p.update(25)

        try:
            if not self.__ds.Login(self.__addon.Username, self.__addon.Password):
                loginFailed()
                return

        except Exception, e:
            print e.args
            p.close()
            self.__close()

        else:
            p.update(75, "Getting tasks...")
            self.__getTasks()
            if p.iscanceled():
                p.close()
                self.__close()
            else:
                p.close()
                self.__thread.start()

    def __update(self):
        running = True

        while running:
            try:
                msgType, msgArgs = self.__queue.get(True, 1.0)
            except Queue.Empty:
                pass
            else:
                if msgType == MSG_METHOD:
                    try:
                        method, args, kwargs = msgArgs
                        method(*args, **kwargs)
                    except Exception, e:
                        xbmc.log("DSTasks: Failed to run method: %s" % e.message, xbmc.LOGWARNING)

                elif msgType == MSG_EXIT:
                    running = False
                    break

            self.__getTasks()


    def __getTasks(self):
        tasks = self.__ds.GetTaskList()
        taskList = self.getControl(51)

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

            item.setProperty("TaskDownProgress", "%.2f" % percentDownload)
            item.setProperty("DownloadFinished", str(1 if (percentDownload == 100.0) else 0))
            item.setProperty("TaskUpProgress", "%.2f" % percentUpload)
            item.setProperty("SpeedDownload", "%d" % (task.SpeedDownload / 1000))
            item.setProperty("SpeedUpload", "%d" % (task.SpeedUpload / 1000))

            if item.getLabel2() == "flip":
                item.setLabel2("flop")
            else:
                item.setLabel2("flip")

    def __close(self):
        self.__queue.put((MSG_EXIT, None))
        if not self.__thread.ident == None:
            self.__thread.join()
        xbmcgui.WindowXML.close(self)

    def onClick(self, controlID):
        selectedTask = self.getControl(51).getSelectedItem()

    def onFocus(self, controlID):
        pass

    def onAction(self, action):
        if (action.getButtonCode() == KEY_BUTTON_BACK) or(action.getId() == KEY_MENU_ID):
            self.__close()