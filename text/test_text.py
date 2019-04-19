import unittest
import wx
from text import Text, ViewModel
from pubsub import pub
from pubsub.utils.notification import useNotifyByWriteFile
import io


class TestView(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.string = ""
        self.controllers = dict(change_string=self.__change_string)
        self.frame = Text(None, -1, 'text.py', self.controllers)

    def tearDown(self):
        wx.CallAfter(self.frame.Close)
        self.app.MainLoop()

    def __change_string(self, evt):
        self.string = evt.GetString()

    def test_update(self):
        expected = ''
        self.assertEqual(self.frame.text.GetValue(), expected)
        self.assertEqual(self.frame.text_log.GetLabel(), expected)

        expected = 'Hello world!'
        pub.sendMessage("update", state={'string': expected})
        wx.CallAfter(lambda: self.assertEqual(self.frame.text.GetValue(), expected))
        wx.CallAfter(lambda: self.assertEqual(self.frame.text_log.GetLabel(), expected))

    def test_change_string(self):
        self.string = ''
        expected = "Changed!"

        event = wx.CommandEvent( wx.wxEVT_TEXT, self.frame.text.GetId())
        event.SetString(expected)
        self.frame.ProcessEvent(event)
        self.assertEqual(expected, self.string)


class TestViewModel(unittest.TestCase):

    def setUp(self):
        self.capture = io.StringIO()
        useNotifyByWriteFile(fileObj=self.capture)
        self.view_model = ViewModel.get_instance()
        pub.subscribe(self.__update_in_view, 'update')

    def tearDown(self):
        pub.unsubscribe(self.__update_in_view, 'update')

    def __update_in_view(self, state):
        pass

    def test_change_string(self):
        expected = "test string"
        evt = wx.CommandEvent(wx.wxEVT_TEXT, -1)
        evt.SetString(expected)

        self.view_model.change_string(evt)
        self.assertEqual(self.view_model._ViewModel__state['string'], expected)

        expected = """\
PUBSUB: Subscribed listener "TestViewModel.__update_in_view" to topic "update"
PUBSUB: Start sending message of topic "update"
PUBSUB: Sending message of topic "update" to listener TestViewModel.__update_in_view
PUBSUB: Done sending message of topic "update"
"""
        result = self.capture.getvalue()
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
