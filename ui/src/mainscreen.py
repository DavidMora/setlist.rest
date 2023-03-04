from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
from ui.src.songlistview import SongListView # we need this import to make sure the songlistview is loaded from kv
from ui.src.setlistview import SetlistView # we need this import to make sure the setlistview is loaded from kv
from modules.helpers.modules import extractAndRemoveModules, validateModuleCompleteness
from ui.src.workers.statusloopworker import StatusLoopWorker
from ui.src.workers.executeactionworker import ExecuteActionWorker
import modules.helpers.constants as constants
from modules.songs.song import Song
import copy
Builder.load_file('ui/kv/main.kv')

class MainScreen(Screen):
    '''
        Main screen of the app. 

        This screen is the main screen of the app. 
        It contains the songlist and the setlist and handles the connection and communications to the DAW.
    '''
    def __init__(self, **kwargs):
        data = extractAndRemoveModules(kwargs=kwargs)
        super(Screen, self).__init__(**data['kwargs'])
        self.modules = data['modules']
        validateModuleCompleteness(self)
        self.event_loop_worker = None
        self.connection_error = False
    def on_enter(self, *args) -> None:
        self.manager.get_screen('MainScreen').ids.songlist.songs = self.modules['songs']
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
        pass
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
    def arrow_left(self):
        ids = self.manager.get_screen('MainScreen').ids.setlist.get_selected_ids()
        for id in ids:
            setlist_item_id = int(id.replace(constants.marker_prefix_for_setlist, '').split('-')[0])
            self.modules['setlist'].remove(setlist_item_id)
        self.populate_setlist()
    def arrow_up(self):
        ids = self.manager.get_screen('MainScreen').ids.setlist.get_selected_ids()
        for id in ids:
            setlist_item_id = int(id.replace(constants.marker_prefix_for_setlist, '').split('-')[0])
            self.modules['setlist'].move_up(setlist_item_id)
        self.populate_setlist()
    def arrow_down(self):
        ids = self.manager.get_screen('MainScreen').ids.setlist.get_selected_ids()
        for id in ids:
            setlist_item_id = int(id.replace(constants.marker_prefix_for_setlist, '').split('-')[0])
            self.modules['setlist'].move_down(setlist_item_id)
        self.populate_setlist()
    def play(self):
        marker = self.modules['setlist'].next()
        self.goto_marker_and_play(marker)
    def goto_marker_and_play(self, marker):
        ExecuteActionWorker().start([
            self.modules['daw'].goto_marker,
            self.modules['daw'].play
            ], [
             [marker],
             []
            ])
    def stop(self):
        ExecuteActionWorker().start([
            self.modules['daw'].stop,
            ], [
             []
            ])
    def skip_backward(self):
        marker = self.modules['setlist'].prev()
        self.goto_marker_and_play(marker)
    def skip_forward(self):
        self.play()
    def populate_setlist(self):
        setlist_songs = []
        for setlist_item in self.modules['setlist']:
            song = copy.deepcopy(self.modules['songs'].get_song_by_position(setlist_item['marker']))
            if song is not None:
                song.id = setlist_item['id']
                setlist_songs.append(song) 
        self.manager.get_screen('MainScreen').ids.setlist.populate(setlist_songs)