import unittest
from unittest.mock import AsyncMock
from modules.reacontrol.reacontrol import ReaControl

class TestReacontrol(unittest.IsolatedAsyncioTestCase):
    def test_setConnectionDataStoresData(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        self.assertEqual(reacontrol.host, 'localhost')
        self.assertEqual(reacontrol.port, 8080)
        self.assertEqual(reacontrol.password, 'password')
        self.assertEqual(reacontrol.username, 'username')
    async def test_getStatusRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.getStatus()
    async def test_getStatusReturnsStatus(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._ReaControl__reaper = AsyncMock()
        reacontrol._ReaControl__reaper.getStatus.return_value = '{"metronome": 1}'
        status = await reacontrol.get_status()
        self.assertEqual(status, {"metronome": 1})
    async def test_getMarkersRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.getMarkers()
    async def test_getMetronomeRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.getMetronome()
    async def test_toggleMetronomeRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.toggleMetronome()
    async def test_playRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.play()
    async def test_stopRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.stop()
    async def test_RaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol._raise_if_not_initialized()
    async def test_gotoTimeRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.gotoTime()
    async def test_getTimeRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.getTime()
    async def test_getTimeSignatureRaisesExceptionIfNotInitialized(self):
        reacontrol = ReaControl()
        with self.assertRaises(Exception):
            await reacontrol.getTimeSignature()
    async def test_getMarkersReturnsMarkers(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.sendCommand = AsyncMock()
        reacontrol._reaper.sendCommand.return_value = 'MARKER\tSONG1\t1\tmarker1\nMARKER\tSONG2\t2\tmarker2\nMARKER\t!1016'
        markers = await reacontrol.get_markers()
        self.assertEqual(markers, [['SONG1', '1', 'marker1'], ['SONG2', '2', 'marker2']])
    async def test_getMarkersReturnsEmptyMarkers(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.sendCommand = AsyncMock()
        reacontrol._reaper.sendCommand.return_value = 'MARKER BEGIN\nMARKER END'
        markers = await reacontrol.get_markers()
        self.assertEqual(markers, [])
    async def test_getMetronomeReturnsMetronome(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.getStatus = AsyncMock()
        reacontrol._reaper.getStatus.return_value = '{"metronome": 1}'
        metronome = await reacontrol.get_metronome()
        self.assertEqual(metronome, 1)
    async def test_toggleMetronomeTogglesMetronome(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.toggleMetronome = AsyncMock()
        await reacontrol.toggle_metronome()
        reacontrol._reaper.toggleMetronome.assert_called()
    async def test_playPlays(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.sendCommand = AsyncMock()
        play = await reacontrol.play('1')
        reacontrol._reaper.sendCommand.assert_called_with('PLAY')
    async def test_stopStops(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.sendCommand = AsyncMock()
        play = await reacontrol.stop()
        reacontrol._reaper.sendCommand.assert_called_with('STOP')
    async def test_gotoMarkerGoesToMarker(self):
        reacontrol = ReaControl()
        reacontrol.set_connection_data(host='localhost', port=8080, password='password', username='username')
        reacontrol._reaper.sendCommand = AsyncMock()
        marker = '1'
        await reacontrol.goto_marker(marker)
        reacontrol._reaper.sendCommand.assert_called_with("SET/POS_STR/%s" % marker)

