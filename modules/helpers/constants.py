import os
marker_prefix_for_songlist = 'song-marker-'
marker_prefix_for_setlist = 'setlist-marker-'
play_state_stop = 'stopped'
hidden_folder_name = '.cbsetlist'
home_dir = os.path.expanduser("~")
hidden_folder_path = os.path.join(home_dir, hidden_folder_name)
setlist_file_name = 'setlist.json'
setlist_file_path = os.path.join(hidden_folder_path, setlist_file_name)
if not os.path.exists(hidden_folder_path):
    os.mkdir(hidden_folder_path)


PLAYSTATE_STOPPED = "stopped"
PLAYSTATE_PLAYING = "playing"
PLAYSTATE_PAUSED = "paused"
PLAYSTATE_RECORDING = "recording"
PLAYSTATE_RECORDPAUSED = "recordpaused"

FLAG_FOLDER = "folder"
FLAG_SELECTED = "selected"
FLAG_HAS_FX = "has-fx"
FLAG_MUTED = "muted"
FLAG_SOLOED = "soloed"
FLAG_SOLO_IN_PLACE = "solo-in-place"
FLAG_RECORD_ARMED = "record-armed"
FLAG_RECORD_MONITORING_ON = "record-monitoring-on"
FLAG_RECORD_MONITORING_AUTO = "record-monitoring-auto"

playState = {
    0: PLAYSTATE_STOPPED,
    1: PLAYSTATE_PLAYING,
    2: PLAYSTATE_PAUSED,
    5: PLAYSTATE_RECORDING,
    6: PLAYSTATE_RECORDPAUSED,
}