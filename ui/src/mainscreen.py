from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import asyncio
from ui.src.songlistview import SongListView # we need this import to make sure the songlistview is loaded from kv
from ui.src.setlistview import SetlistView # we need this import to make sure the setlistview is loaded from kv
from modules.helpers.modules import extractAndRemoveModules, validateModuleCompleteness

Builder.load_file('ui/kv/main.kv')


class MainScreen(Screen):
    def __init__(self, **kwargs):
        data = extractAndRemoveModules(kwargs=kwargs)
        super(Screen, self).__init__(**data['kwargs'])
        self.modules = data['modules']
        validateModuleCompleteness(self)
    def on_enter(self, *args):
        asyncio.to_thread(self.is_connected)
        self.manager.get_screen('MainScreen').ids.songlist.populate()
        self.manager.get_screen('MainScreen').ids.setlist.populate()

    async def is_connected(self):
        try:
            status = await self.modules['daw'].get_status()
        except Exception as e:
            print(e)

    
