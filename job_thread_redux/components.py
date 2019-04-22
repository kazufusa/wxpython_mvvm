import wx
from pubsub import pub

class App(wx.Frame):
    def __init__(self, parent, id, title, state, actions):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self, -1)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.box)

        self.box_btn = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_start = wx.Button(self.panel, -1, label='START')
        self.btn_cancel = wx.Button(self.panel, -1, label='CANCEL')
        self.box_btn.Add(self.btn_start, 0, wx.LEFT, 5)
        self.box_btn.Add(self.btn_cancel, 0, wx.LEFT, 5)

        self.box.Add(self.box_btn, 0, wx.TOP, 5)
        self.log = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.box.Add(self.log, 2, wx.ALL | wx.EXPAND, 5)

        self.Bind(
            wx.EVT_BUTTON,
            lambda x: state.dispatch(actions.start_job()),
            id=self.btn_start.GetId()
        )

        self.Bind(
            wx.EVT_BUTTON,
            lambda x: [
                state.dispatch(actions.finish_job())
            ],
            id=self.btn_cancel.GetId()
        )

        pub.subscribe(self.update, 'update')
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Center()

    def onClose(self, event):
        pub.unsubscribe(self.update, 'update')
        self.Destroy()

    def update(self, state):
        wx.CallAfter(self.__update_core, state)

    def __update_core(self, state):
        if state['job']['job_ident'] is not None:
            self.btn_start.Disable()
            self.btn_cancel.Enable()
        else:
            self.btn_start.Enable()
            self.btn_cancel.Disable()

        self.log.SetValue(state['job']['log'])
