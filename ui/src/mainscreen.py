from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.toast import toast
from ui.src.songlistview import SongListView # we need this import to make sure the songlistview is loaded from kv
from ui.src.setlistview import SetlistView # we need this import to make sure the setlistview is loaded from kv
from modules.helpers.modules import extractAndRemoveModules, validateModuleCompleteness
from ui.src.workers.statusloopworker import StatusLoopWorker
from ui.src.workers.executeactionworker import ExecuteActionWorker
import modules.helpers.constants as constants
from modules.songs.song import Song
import copy
import pathlib
current_path = pathlib.Path(__file__).parent.parent.resolve()
Builder.load_file(f'{current_path}/kv/main.kv')

class MainScreen(Screen):
    '''
        Main screen of the app. 

        This screen is the main screen of the app. 
        It contains the songlist and the setlist and handles the connection and communications to the DAW.
    '''
    metronome_string = StringProperty('Metronome: unknown')
    play_state_string = StringProperty('Play state: stopped')
    def __init__(self, **kwargs):
        data = extractAndRemoveModules(kwargs=kwargs)
        super(Screen, self).__init__(**data['kwargs'])
        self.modules = data['modules']
        validateModuleCompleteness(self)
        self.event_loop_worker = None
        self.connection_error = False
        self.status = {
            'metronome': None,
            'play_state': None
        }
        self.previous_state = None
    def on_enter(self, *args) -> None:
        self.manager.get_screen('MainScreen').ids.songlist.songs = self.modules['songs']
        Clock.schedule_interval(lambda dt: self.periodic_processor(), 1)
        def repaint(dt):
            if (self.connection_error == True):
                toast('Connection to DAW failed')
                self.connection_error = False
                self.manager.current = 'ConnectionScreen'
            self.manager.get_screen('MainScreen').ids.songlist.populate()
        self.event = Clock.schedule_interval(repaint, 0.5)
        self.populate_setlist()
    def on_pre_leave(self, *args):
        self.event.cancel()
        if self.event_loop_worker is not None:
            self.event_loop_worker.stop()
            self.event_loop_worker = None
    def fetch_info_from_daw(self):
        """Start the asyncio event loop thread. Bound to the top button."""
        if self.event_loop_worker is not None:
            return
        self.event_loop_worker = worker =  StatusLoopWorker()
        worker.bind(on_status=self.is_connected,
                     on_error=self.on_error,
                     on_markers=self.on_markers)
        worker.start(self.modules['daw'])
    def set_connection_data(self, hostname, port, username, password):
        self.modules['daw'].set_connection_data(host=hostname, port=port, username=username, password=password)
        if self.event_loop_worker is not None:
            self.event_loop_worker.stop()
            self.event_loop_worker = None
        self.fetch_info_from_daw()
    def is_connected(self, instance: StatusLoopWorker, status: dict) -> None:
        if 'play_state' in status:
            self.status['play_state'] = status['play_state']
        if 'metronome' in status:
            self.status['metronome'] = status['metronome']
    def process_metronome(self):
        metronome_text = 'On' if self.status['metronome'] else 'Off'
        self.update_metronome_label(metronome_text)
    def process_play_state(self):
        current_state = self.status['play_state']
        if self.previous_state != current_state:
            icon = 'stop' if current_state == constants.play_state_stop else 'play'
            self.populate_setlist(icon)
        self.previous_state = current_state
    def on_markers(self, instance: StatusLoopWorker, markers: list) -> None:
        self.modules['songs'].set_songs(markers)
    def on_error(self, instance: StatusLoopWorker, error: Exception) -> None:
        self.connection_error = True
    def arrow_right(self):
        markers = self.manager.get_screen('MainScreen').ids.songlist.arrow_right()
        for id in markers:
            marker = id.replace(constants.marker_prefix_for_songlist, '')
            self.modules['setlist'].append(marker)
        self.populate_setlist()
        self.modules['setlist'].save_setlist()
    def arrow_left(self):
        ids = self.manager.get_screen('MainScreen').ids.setlist.get_selected_ids()
        for id in ids:
            setlist_item_id = int(id.replace(constants.marker_prefix_for_setlist, '').split('-')[0])
            self.modules['setlist'].remove(setlist_item_id)
        self.populate_setlist()
        self.modules['setlist'].save_setlist()
    def arrow_up(self):
        ids = self.manager.get_screen('MainScreen').ids.setlist.get_selected_ids()
        for id in ids:
            setlist_item_id = int(id.replace(constants.marker_prefix_for_setlist, '').split('-')[0])
            self.modules['setlist'].move_up(setlist_item_id)
        self.populate_setlist()
        self.modules['setlist'].save_setlist()
    def arrow_down(self):
        ids = self.manager.get_screen('MainScreen').ids.setlist.get_selected_ids()
        for id in ids:
            setlist_item_id = int(id.replace(constants.marker_prefix_for_setlist, '').split('-')[0])
            self.modules['setlist'].move_down(setlist_item_id)
        self.populate_setlist()
        self.modules['setlist'].save_setlist()
    def play(self):
        marker = self.modules['setlist'].next()
        self.populate_setlist()
        self.goto_marker_and_play(marker)
    def goto_marker_and_play(self, marker):
        self.modules['daw'].goto_marker(marker)
        self.modules['daw'].play()
    def stop(self):
        self.modules['daw'].stop()
    def toggle_metronome(self):
        self.modules['daw'].toggle_metronome()
    def skip_backward(self):
        marker = self.modules['setlist'].prev()
        self.populate_setlist()
        self.goto_marker_and_play(marker)
    def skip_forward(self):
        self.play()
        self.populate_setlist()
    def populate_setlist(self, icon_for_current_song: str='play'):
        setlist_songs = []
        currently_playing_id = self.modules['setlist'].get_currently_playing()
        for setlist_item in self.modules['setlist']:
            song = copy.deepcopy(self.modules['songs'].get_song_by_position(setlist_item['marker']))
            if song is not None:
                song.playing = None
                if currently_playing_id == setlist_item['id']:
                    song.playing = icon_for_current_song
                    now_playing_label = 'stopped'
                    if icon_for_current_song == 'play':
                        now_playing_label = song.title

                    self.update_now_playing_label(now_playing_label)
                song.id = setlist_item['id']
                setlist_songs.append(song)
        if currently_playing_id == -1 and len(setlist_songs) > 0:
            setlist_songs[0].playing = 'stop'
        self.manager.get_screen('MainScreen').ids.setlist.populate(setlist_songs)
    def periodic_processor(self):
        self.process_metronome()
        self.process_play_state()
    def update_now_playing_label(self, song_title: str=''):
        self.play_state_string = f'Now playing: {song_title}'
    def update_metronome_label(self, metronome_text: str=''):
        self.metronome_string = f'Metronome: {metronome_text}'