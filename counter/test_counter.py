import unittest
import wx
from counter import Counter, ViewModel
from pubsub import pub
from pubsub.utils.notification import useNotifyByWriteFile
import io


class TestView(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.count = 0
        self.controllers = dict(increment=self.__increment)
        self.frame = Counter(None, -1, 'simple.py', self.controllers)

    def tearDown(self):
        wx.CallAfter(self.frame.Close)
        self.app.MainLoop()

    def __increment(self, *args):
        self.count += 1

    def test_current_count(self):
        self.assertEqual(self.frame.text.GetLabel(), '0')
        pub.sendMessage("update", state={'count': '2'})
        self.assertEqual(self.frame.text.GetLabel(), '2')

    def test_button_click(self):
        self.count = 0
        event = wx.CommandEvent(
            wx.wxEVT_COMMAND_BUTTON_CLICKED,
            self.frame.button.GetId()
        )
        self.frame.ProcessEvent(event)
        self.assertEqual(1, self.count)


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

    def test_increment(self):
        self.view_model.increment()
        self.assertEqual(self.view_model._ViewModel__state['count'], 1)

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
