#! /usr/bin/env python

import wx
from pubsub import pub
import copy
import threading
import time
from datetime import datetime


class SingletonException(Exception):
    pass


class Singleton(object):
    __instance = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.__instance is not None:
            raise SingletonException("Class instance is already created")


class ViewModel(Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__state = { 'is_job_running': False, 'log': '' }

    def start_job(self, *args):
        self.__state['is_job_running'] = True
        self.__state['log'] = ''
        self.update()

        def job():
            self.add_log("# start\n")
            for i in range(5):
                time.sleep(1)
                self.add_log(f"{datetime.now()}\n")
            self.add_log("# end\n")
            self.finish_job()

        threading.Thread(target=job).start()

    def finish_job(self, *args):
        self.__state['is_job_running'] = False
        self.update()

    def add_log(self, text):
        self.__state['log'] += text
        self.update()

    def update(self):
        self.__state = copy.deepcopy(self.__state)
        pub.sendMessage("update", state=self.__state)


class JobThread(wx.Frame):
    def __init__(self, parent, id, title, controllers):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self, -1)
        self.hbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.hbox)

        self.button = wx.Button(self.panel, -1, label='START')
        self.log = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.hbox.Add(self.button, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.hbox.Add(self.log, 2, wx.ALL | wx.EXPAND, 5)

        self.Bind(wx.EVT_BUTTON, controllers['start_job'], id=self.button.GetId())

        pub.subscribe(self.update, 'update')
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Center()

    def onClose(self, event):
        pub.unsubscribe(self.update, 'update')
        self.Destroy()

    def update(self, state):
        wx.CallAfter(self.__update_core, state)

    def __update_core(self, state):
        if state['is_job_running']:
            self.button.Disable()
        else:
            self.button.Enable()

        self.log.SetValue(state['log'])


if __name__ == '__main__':
    app = wx.App()
    view_model = ViewModel.get_instance()
    controllers = {'start_job': view_model.start_job}

    frame = JobThread(None, -1, 'job_thread.py', controllers)
    frame.Show(True)
    view_model.update()

    app.MainLoop()
