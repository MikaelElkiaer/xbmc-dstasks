import urllib2
import json
from decimal import Decimal

class DS:
    __loginURL = "auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=%s&passwd=%s&session=DownloadStation&format=sid"
    __taskListURL = "DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=list&_sid=%s"
    __taskInfoURL = "DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=getinfo&id=%s&additional=detail,transfer&_sid=%s"
    __versionURL = "query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task"
    __logoutURL = "auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=DownloadStation&_sid=%s"

    def __init__(self, path, isSecured, username, password):
        protocol = "http"
        port = "5000"

        if isSecured:
            protocol = "https"
            port = "5001"

        self.__baseURL = "%s://%s:%s/webapi/" % (protocol, path, port)

        self.__sessionID = self.__login(username, password)

        self.taskList = self.__getTaskList()

        self.__logout()
        
    def __login(self, username, password):
        loginResponse = urllib2.urlopen(self.__baseURL + self.__loginURL % (username, password))
        sessionID = json.loads(loginResponse.read())["data"]["sid"]
        
        return sessionID
        
    def __logout(self):
        urllib2.urlopen(self.__baseURL + self.__logoutURL % self.__sessionID)

    def __getTaskList(self):
        listResponse = urllib2.urlopen(self.__baseURL + self.__taskListURL % self.__sessionID)
        taskList = json.loads(listResponse.read())["data"]["tasks"]
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