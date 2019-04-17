import unittest
import wx
from counter import Counter
from pubsub import pub


class TestCounter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.count = 0
        self.controllers = dict(increment=self.__increment)
        self.frame = Counter(None, -1, 'simple.py', self.controllers)

    def tearDown(self):
        wx.CallAfter(wx.Exit)
        self.app.MainLoop()

    def __increment(self, *args):
        self.count += 1

    def testCurrentCount(self):
        self.assertEqual(self.frame.text.GetLabel(), '0')
        pub.sendMessage("update", state={'count': '2'})
        self.assertEqual(self.frame.text.GetLabel(), '2')

    def testButtonClick(self):
        self.count = 0
        event = wx.CommandEvent(
            wx.wxEVT_COMMAND_BUTTON_CLICKED,
            self.frame.button.GetId()
        )
        self.frame.ProcessEvent(event)
        self.assertEqual(1, self.count)


if __name__ == '__main__':
    unittest.main()
