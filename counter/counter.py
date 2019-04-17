#! /usr/bin/env python

import wx
from pubsub import pub
import copy

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

        self.__state = { 'count': 0 }

    def increment(self, *args, **kwargs):
        self.__state['count'] += 1
        self.update()

    def update(self):
        self.__state = copy.deepcopy(self.__state)
        pub.sendMessage("update", state=self.__state)


class Counter(wx.Frame):
    def __init__(self, parent, id, title, controllers):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self, -1)
        self.hbox = wx.BoxSizer()
        self.panel.SetSizer(self.hbox)

        self.button = wx.Button(self.panel, -1, '+')
        self.text = wx.StaticText(self.panel, -1, label='0', style=wx.ALIGN_CENTRE)
        self.hbox.Add(self.button, 1, wx.EXPAND | wx.ALL, 5)
        self.hbox.Add(self.text, 1, wx.ALIGN_CENTRE_VERTICAL, 5)

        self.Bind(wx.EVT_BUTTON, controllers['increment'], id=self.button.GetId())

        pub.subscribe(self.update, 'update')
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Center()

    def onClose(self, event):
        pub.unsubscribe(self.update, 'update')
        self.Destroy()

    def update(self, state):
        self.text.SetLabel(f"{state['count']}")
        self.hbox.Layout()


if __name__ == '__main__':
    app = wx.App()
    view_model = ViewModel.get_instance()
    controllers = {'increment': view_model.increment}

    frame = Counter(None, -1, 'simple.py', controllers)
    frame.Show(True)

    app.MainLoop()
