#! /usr/bin/env python

import wx

import actions
import components
from reducers import reducers
from store import Store


if __name__ == '__main__':
    app = wx.App()
    state = Store.get_instance(reducers)
    frame = components.App(None, -1, 'job_thread_redux', state, actions)
    frame.Show(True)
    state.update()
    app.MainLoop()
