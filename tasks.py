import urllib2
import json
from decimal import Decimal

class DS:
    __loginURL = "auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=%s&passwd=%s&session=DownloadStation&format=sid"
    __taskListURL = "DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=list&_sid=%s"
    __taskInfoURL = "DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=getinfo&id=%s&additional=detail,transfer&_sid=%s"
    __taskPauseURL = "DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=pause&id=%s&_sid=%s"
    __logoutURL = "auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=DownloadStation"

    def __init__(self, path, isSecured):
        protocol = "http"
        port = "5000"

        if isSecured:
            protocol = "https"
            port = "5001"

        self.__baseURL = "%s://%s:%s/webapi/" % (protocol, path, port)
        
    def Login(self, username, password):
        response = urllib2.urlopen(self.__baseURL + self.__loginURL % (username, password))
        responseJSON = json.loads(response.read())

        success = responseJSON["success"]

        if success:
            self.__sessionID = responseJSON["data"]["sid"]

        return success
        
    def Logout(self):
        urllib2.urlopen(self.__baseURL + self.__logoutURL)

    def GetTaskList(self):
        response = urllib2.urlopen(self.__baseURL + self.__taskListURL % self.__sessionID)
        taskList = json.loads(response.read())["data"]["tasks"]
        ids = ""
        for task in taskList:
            ids += task["id"] + ","
        ids = ids[0:len(ids)-1]

        infoResponse = urllib2.urlopen(self.__baseURL + self.__taskInfoURL % (ids, self.__sessionID))

        taskInfoList = json.loads(infoResponse.read())["data"]["tasks"]
        
        dstasks = []

        for task in taskInfoList:
            id = task["id"]
            title = task["title"]
            status = task["status"]
            size = task["size"]
            sizeDownloaded = task["additional"]["transfer"]["size_downloaded"]
            sizeUploaded = task["additional"]["transfer"]["size_uploaded"]
            speedDownload = task["additional"]["transfer"]["speed_download"]
            speedUpload = task["additional"]["transfer"]["speed_upload"]
            dstasks.append(DSTask(id, title, status, size, sizeDownloaded, sizeUploaded, speedDownload, speedUpload))

        return dstasks

    def Pause(self, id):
        urllib2.urlopen(self.__baseURL + self.__taskPauseURL % (id, self.__sessionID))

class DSTask:
    def __init__(self, id, title, status, size, sizeDownloaded, sizeUploaded, speedDownload, speedUpload):
        self.__id = id
        self.__title = title
        self.__status = status
        self.__size = int(size)
        self.__sizeDownloaded = int(sizeDownloaded)
        self.__sizeUploaded = int(sizeUploaded)
        self.__speedDownload = int(speedDownload)
        self.__speedUpload = int(speedUpload)

    @property
    def ID(self): return self.__id
    @property
    def Title(self): return self.__title
    @property
    def Status(self): return self.__status
    @property
    def Size(self): return self.__size
    @property
    def SizeDownloaded(self): return self.__sizeDownloaded
    @property
    def SizeUploaded(self): return self.__sizeUploaded
    @property
    def SpeedDownload(self): return self.__speedDownload
    @property
    def SpeedUpload(self): return self.__speedUpload