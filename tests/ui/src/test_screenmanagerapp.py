import unittest
import sys
import time
import os.path as op
from functools import partial
from kivy.clock import Clock


class SetList:
    pass

class ReaControl:
    pass

class Songs:
    pass

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path[:len(main_path) - len('tests/ui')])

from ui.src.screenmanagerapp import ScreenManagerApp

class Test(unittest.TestCase):
    # sleep function that catches `dt` from Clock
    def pause(*args):
        time.sleep(0.000001)

    # main test function
    def run_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)
        app.stop()
    # same named function as the filename(!)
    def test_screenManagerLoads(self):
        app = ScreenManagerApp(modules={'daw':ReaControl(), 'songs':Songs(), 'setlist':SetList()})
        p = partial(self.run_test, app)
        Clock.schedule_once(p, 0.000001)
        app.run()
    def test_screenManagerRaisesWhenNoDaw(self):
        with self.assertRaises(Exception):
            app = ScreenManagerApp(modules={'songs':Songs(), 'setlist':SetList()})
    def test_screenManagerRaisesWhenNoSongs(self):
        with self.assertRaises(Exception):
            app = ScreenManagerApp(modules={'daw':ReaControl(), 'setlist':SetList()})
    def test_screenManagerRaisesWhenNoSetlist(self):
        with self.assertRaises(Exception):
            app = ScreenManagerApp(modules={'daw':ReaControl(), 'songs':Songs()})
if __name__ == '__main__':
    unittest.main()