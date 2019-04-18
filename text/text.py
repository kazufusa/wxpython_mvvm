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

        self.__state = { 'string': 'This is default string in state.' }

    def change_string(self, evt):
        self.__state['string'] = evt.GetString()
        self.update()

    def update(self):
        self.__state = copy.deepcopy(self.__state)
        pub.sendMessage("update", state=self.__state)


class Text(wx.Frame):
    def __init__(self, parent, id, title, controllers):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self, -1)
        self.hbox = wx.BoxSizer()
        self.panel.SetSizer(self.hbox)

        self.text = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE)
        self.text_log = wx.StaticText(self.panel, -1, style=wx.TE_MULTILINE)
        self.hbox.Add(self.text, 1, wx.EXPAND, 5)
        self.hbox.Add(self.text_log, 1, wx.EXPAND, 5)

        self.Bind(wx.EVT_TEXT, controllers['change_string'], id=self.text.GetId())

        pub.subscribe(self.update, 'update')
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Center()

    def onClose(self, event):
        pub.unsubscribe(self.update, 'update')
        self.Destroy()

    def update(self, state):
        new = state['string']
        self.text_log.SetLabel(new)
        current = self.text.GetValue()
        if new != current: self.text.SetValue(new)


if __name__ == '__main__':
    app = wx.App()
    view_model = ViewModel.get_instance()
    controllers = {'change_string': view_model.change_string}

    frame = Text(None, -1, 'text.py', controllers)
    frame.Show(True)
    view_model.update()

    app.MainLoop()
