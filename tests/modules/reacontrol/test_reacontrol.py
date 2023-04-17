import unittest
from unittest.mock import AsyncMock
from modules.reacontrol.reacontrol import ReaControl

import unittest
from unittest.mock import patch
from modules.reacontrol.reacontrol import ReaControl
import modules.helpers.constants as constants

class TestReaControl(unittest.TestCase):
    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_set_connection_data(self, mock_urlopen):
        r = ReaControl()
        r.set_connection_data(host='localhost', port=8080)
        self.assertTrue(r.initialized)
        self.assertEqual(r.host, 'localhost')
        self.assertEqual(r.port, 8080)
        self.assertEqual(r.username, '')
        self.assertEqual(r.password, '')
        self.assertEqual(r.base_url, 'http://localhost:8080/_/')

        r.set_connection_data(host='localhost', port=8080, username='user', password='pass')
        self.assertEqual(r.username, 'user')
        self.assertEqual(r.password, 'pass')
        self.assertEqual(r.base_url, 'http://user:pass@localhost:8080/_/')

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_get_status(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = 'NTRACK\t5\nTRANSPORT\t1\t0.0\t0\t0.0\t4.1.0\t4.1.0\nBEATPOS\t0.0\t0.0\t1\t1\t1\t1\t1\nMARKER\t0\t!1016\tname\n'.encode('utf-8')
        r = ReaControl()
        r.set_connection_data(host='localhost', port=8080)
        status, markers = r.get_status()
        self.assertEqual(status, {'time_signature': '1/1', 'beatpos': {'position_seconds': '0.0', 'full_beat_position': '1', 'measure_cnt': '1', 'beats_in_measure': '1'}, 'play_state': 'playing', 'transport': {'playstate': 'playing', 'position_seconds': '0.0', 'repeat': False, 'position_string': '0.0', 'position_string_beats': '4.1.0'}, 'number_of_tracks': 5, 'armed_tracks': [], 'number_of_armed_tracks': 0})
        self.assertEqual(markers, [['0', '!1016', 'name']])

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_parse_markers(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = 'MARKER\t0\t!1016\nMARKER\t1\tmarker1\nMARKER\t2\tmarker2\nMARKER\t3\tmarker3\n'
        r = ReaControl()
        markers = r.parse_markers(mock_urlopen.return_value.read.return_value)
        self.assertEqual(markers, [['0', '!1016'], ['1', 'marker1'], ['2', 'marker2'], ['3', 'marker3']])

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_toggle_metronome(self, mock_urlopen):
        r = ReaControl()
        r.set_connection_data(host='localhost', port=8080)
        r.toggle_metronome()
        mock_urlopen.assert_called_with('http://localhost:8080/_/40364')

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_play(self, mock_urlopen):
        r = ReaControl()
        r.set_connection_data(host='localhost', port=8080)
        r.play()
        mock_urlopen.assert_called_with('http://localhost:8080/_/1007')

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_stop(self, mock_urlopen):
        r = ReaControl()
        r.set_connection_data(host='localhost', port=8080)
        r.stop()
        mock_urlopen.assert_called_with('http://localhost:8080/_/1016')

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_goto_marker(self, mock_urlopen):
        r = ReaControl()
        r.set_connection_data(host='localhost', port=8080)
        r.goto_marker(2)
        mock_urlopen.assert_called_with('http://localhost:8080/_/SET/POS_STR/m2')
   
    def test___raise_if_not_initialized(self):
        r = ReaControl()
        with self.assertRaises(Exception):
            r._ReaControl__raise_if_not_initialized()

    @patch('modules.reacontrol.reacontrol.urllib.request.urlopen')
    def test_send_command(self, mock_urlopen):
        r = ReaControl()
        mock_urlopen.return_value.read.return_value = 'NTRACK\t5\nTRANSPORT\t1\t0.0\t0\t0.0\t4.1.0\t4.1.0\nBEATPOS\t0.0\t0.0\t1\t1\t1\t1\t1\nMARKER\t0\t!1016\tname\n'.encode('utf-8')
        r.send_command('test')
        mock_urlopen.assert_called_with('test')
    def test_empty_field(self):
        r = ReaControl()
        field = 0
        expected_flags = []
        self.assertEqual(r.trackFlags(field), expected_flags)

    def test_single_flag(self):
        r = ReaControl()
        field = 1  # 00000001
        expected_flags = [constants.FLAG_FOLDER]
        self.assertEqual(r.trackFlags(field), expected_flags)

        field = 16  # 00010000
        expected_flags = [constants.FLAG_SOLOED]
        self.assertEqual(r.trackFlags(field), expected_flags)

        field = 128  # 10000000
        expected_flags = [constants.FLAG_RECORD_MONITORING_ON]
        self.assertEqual(r.trackFlags(field), expected_flags)

    def test_multiple_flags(self):
        r = ReaControl()

        field = 19  # 00010011
        expected_flags = [constants.FLAG_FOLDER, constants.FLAG_SELECTED, constants.FLAG_SOLOED]
        self.assertEqual(r.trackFlags(field), expected_flags)

        field = 255  # 11111111
        expected_flags = [constants.FLAG_FOLDER, constants.FLAG_SELECTED, constants.FLAG_HAS_FX, constants.FLAG_MUTED,
                          constants.FLAG_SOLOED, constants.FLAG_SOLO_IN_PLACE, constants.FLAG_RECORD_ARMED,
                          constants.FLAG_RECORD_MONITORING_ON]
        self.assertEqual(r.trackFlags(field), expected_flags)


if __name__ == '__main__':
    unittest.main()


