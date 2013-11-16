import sys
import xbmc
import xbmcgui
import threading
import time

KEY_BUTTON_BACK = 275
KEY_KEYBOARD_ESC = 61467
KEY_MENU_ID = 92

EXIT_SCRIPT = (KEY_BUTTON_BACK, KEY_KEYBOARD_ESC)

class GUI(xbmcgui.WindowXML):
    def onInit(self):
        #self.thread = threading.Thread(target=self.update)
        self.update()
        #self.thread.start()

    def update(self):
        tor_list = self.getControl(51)
        tor_list.reset()
        self.items = [xbmcgui.ListItem() for u in range(10)]
        tor_list.addItems(self.items)

        for key, item in zip(range(10), self.items):
            item.setLabel('Item %s' % key)
            item.setIconImage('DefaultFolder.png')

        tor_list.setEnabled(True)


    def close(self):
        #self.thread.join()
        xbmcgui.WindowXML.close(self)

    def onClick(self, controlID):
        pass

    def onFocus(self, controlID):
        pass

    def onAction(self, action):
        if (action.getButtonCode() in EXIT_SCRIPT) or (action.getId() == KEY_MENU_ID):
            self.close()