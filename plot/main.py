from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx
import pdb

class Plot(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Show()
        self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        # self.toolbar.Bind(wx.EVT_TOOL, lambda x: print(x))

        self.Fit()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)


if __name__ == "__main__":
    app = wx.App(redirect=True)
    frame = Plot(None)
    frame.draw()
    frame.Show()
    # help(NavigationToolbar2Wx)
    app.MainLoop()
