from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ui.src.mainscreen import MainScreen
from modules.helpers.modules import extractAndRemoveModules, validateModuleCompleteness
from ui.src.connectionscreen import ConnectionScreen
class ScreenManagerApp(MDApp):
    def __init__(self, **kwargs):
        data = extractAndRemoveModules(kwargs=kwargs)
        self.modules = data['modules']
        super(ScreenManagerApp, self).__init__(**data['kwargs'])
        validateModuleCompleteness(self)
    def build(self: object) -> ScreenManager:
        '''This function is used to build the app'''
        # self.theme_cls.colors = colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Setlists by CodeBranch'
        root = ScreenManager()
        root.add_widget(ConnectionScreen(name='ConnectionScreen'))
        root.add_widget(MainScreen(name='MainScreen', modules=self.modules))
        return root

    


