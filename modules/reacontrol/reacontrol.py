import aiohttp
import json
from reaperdaw import Reaper

class ReaControl:
    def __init__(self) -> None:
        self.initialized = False
        self._reaper = Reaper
    def set_connection_data(self, *positional, host: str, port: int, username: str='', password: str='') -> None:
        self.initialized = True
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    async def get_status(self) -> str:
        self._raise_if_not_initialized()
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            status = await reaper.getStatus()
            status = json.loads(status)
            return status
    async def get_markers(self) -> list:
        self._raise_if_not_initialized()
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            response = await reaper.sendCommand("MARKER;")
            response = response.split('\n')
            markers = []
            for arrayMarker in response:
                marker = arrayMarker.split('\t')
                if len(marker) != 0 and marker[0] == 'MARKER' and marker[1] != '!1016':
                    markers.append(marker[1:])
            return markers
    async def get_metronome(self) -> int:
        self._raise_if_not_initialized()
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            status = await self.get_status()
            return status["metronome"]
    async def toggle_metronome(self) -> None:
        self._raise_if_not_initialized()
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            await reaper.toggleMetronome()
    async def play(self, marker: str) -> None:
        self._raise_if_not_initialized()
        await self.goto_marker(marker)
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            await reaper.sendCommand("PLAY")
    async def stop(self) -> None:
        self._raise_if_not_initialized()
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            await reaper.sendCommand("STOP")
    async def goto_marker(self, marker: str) -> None:
        self._raise_if_not_initialized()
        async with aiohttp.ClientSession() as session:
            reaper = self._reaper(session, self.host, self.port, self.username, self.password)
            await reaper.sendCommand("SET/POS_STR/%s" % marker)
    def _raise_if_not_initialized(self) -> None:
        if not self.initialized:
            raise Exception("ReaControl not initialized")
    