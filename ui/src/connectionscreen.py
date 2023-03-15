from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import pathlib
current_path = pathlib.Path(__file__).parent.parent.resolve()

Builder.load_file(f'{current_path}/kv/connectionscreen.kv')

class Content(BoxLayout):
    pass

class ConnectionScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.ids.hostname.text = 'localhost'
        self.ids.port.text = '8080'
        self.ids.username.text = ''
        self.ids.password.text = ''
    def set_connection_data(self):
        self.manager.get_screen('MainScreen').set_connection_data(
            self.ids.hostname.text,
            self.ids.port.text,
            self.ids.username.text,
            self.ids.password.text
        )
        self.manager.current = 'MainScreen'

