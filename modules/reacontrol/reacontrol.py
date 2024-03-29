import urllib.request
from collections import ChainMap
import modules.helpers.constants as constants
from typing import List, Dict

class ReaControl:
    def __init__(self) -> None:
        self.initialized: bool = False
        self.counter: int = 0
        self.base_url: str = ''
    def set_connection_data(self, *positional, host: str, port: int, username: str='', password: str='') -> None:
        self.initialized = True
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        auth: str = f'{self.username}:{self.password}@' if self.username != '' and self.password != '' else ''
        self.base_url: str = f'http://{auth}{self.host}:{self.port}/_/'
    def get_status(self) -> list:
        self._raise_if_not_initialized()
        response = self.send_command('NTRACK;TRANSPORT;BEATPOS;GET/40364;GET/1157;TRACK;')
        status = self.parse(response)
        response = self.send_command("MARKER;")
        self.counter += 1
        markers = self.parse_markers(response)
        return [status, markers]
    def parse_markers(self, response: str) -> list:
        split_response: list = response.split('\n')
        markers: list = []
        for arrayMarker in split_response:
            marker: list = arrayMarker.split('\t')
            if len(marker) != 0 and marker[0] == 'MARKER' and marker[1] != '!1016':
                markers.append(marker[1:])
        return markers
    def toggle_metronome(self) -> None:
        self._raise_if_not_initialized()
        self.send_command("40364")
    def play(self) -> None:
        self._raise_if_not_initialized()
        self.send_command("1007")
    def stop(self) -> None:
        self._raise_if_not_initialized()
        self.send_command("1016")
    def goto_marker(self, marker: str) -> None:
        self._raise_if_not_initialized()
        self.send_command(f"SET/POS_STR/m{marker}")
    def _raise_if_not_initialized(self) -> None:
        if not self.initialized:
            raise Exception("ReaControl not initialized")
    def send_command(self, command: str) -> str:
        return urllib.request.urlopen(self.base_url + command).read().decode('utf-8')
    def trackFlags(self,field: int):
        """Process track flags"""
        flags: List = []
        if field & 1:
            flags.append(constants.FLAG_FOLDER)

        if field & 2:
            flags.append(constants.FLAG_SELECTED)

        if field & 4:
            flags.append(constants.FLAG_HAS_FX)

        if field & 8:
            flags.append(constants.FLAG_MUTED)

        if field & 16:
            flags.append(constants.FLAG_SOLOED)

        if field & 32:
            flags.append(constants.FLAG_SOLO_IN_PLACE)

        if field & 64:
            flags.append(constants.FLAG_RECORD_ARMED)

        if field & 128:
            flags.append(constants.FLAG_RECORD_MONITORING_ON)

        if field & 256:
            flags.append(constants.FLAG_RECORD_MONITORING_AUTO)

        return flags
    def parse(self, payload: str) -> dict:
        """Parse Reaper DAW payload"""
        tracks: Dict = {"tracks": []}

        def processLine(line: str) -> str:
            """Process line"""
            token: List[str] = line.strip().split("\t")
            name: str = token[0]
            if(name == "NTRACK"):
                return {"number_of_tracks": int(token[1])}
            elif(name == "TRANSPORT"):
                return {
                    "play_state": constants.playState[int(token[1])],
                    "transport": {
                        "playstate": constants.playState[int(token[1])],
                        "position_seconds": token[2],
                        "repeat": bool(int(token[3])),
                        "position_string": token[4],
                        "position_string_beats": token[5],
                    },
                }
            elif(name == "BEATPOS"):
                return {
                    "time_signature": f"{int(token[6])}/{int(token[7])}",
                    "beatpos": {
                        "position_seconds": token[2],
                        "full_beat_position": token[3],
                        "measure_cnt": token[4],
                        "beats_in_measure": token[5],
                    },
                }
            elif(name == "CMDSTATE"):
                if (token[1] == "40364"):
                    return {"metronome": bool(int(token[2]))}
                elif (token[1] == "1157"):
                    return {"repeat": bool(int(token[2]))}
            elif(name == "TRACK"):
                index = int(token[1])
                tracks["tracks"].append({
                    "index": index,
                    "name": token[2],
                    "flags": self.trackFlags(int(token[3])),
                    "volume": token[4],
                    "pan": token[5],
                    "last_meter_peak": token[6],
                    "last_meter_pos": token[7],
                    "width_pan2": token[8],
                    "panmode": token[9],
                    "sendcnt": token[10],
                    "recvcnt": token[11],
                    "hwoutcnt": token[12],
                    "color": "#000000" if int(token[13]) == 0 else f"#{hex(int(token[13]))[3:]}",
                })
                return tracks

        array: List[str] = payload.split("\n")
        lines: List[str] = [element for element in array if element]
        processedLines: List[Dict[str, str]] = map(processLine, lines)
        parsed: List[Dict[str, str]] = list(processedLines)
        result: List[Dict[str, str]] = [element for element in parsed if element]
        dictionary: Dict[str, str] = dict(ChainMap(*result))

        tracks = dictionary.get("tracks")

        # get tracks filtered by FLAG_RECORD_ARMED
        armedTracks = [
            track["name"]
            for track in tracks if constants.FLAG_RECORD_ARMED in track["flags"]
        ] if tracks else []
        dictionary["armed_tracks"] = armedTracks

        # get number of armed tracks
        dictionary["number_of_armed_tracks"] = len(armedTracks)

        return dictionary

            
        