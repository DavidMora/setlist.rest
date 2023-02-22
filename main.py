import asyncio
import kivy
kivy.require('2.1.0') # replace with your current kivy version !
from ui.src.screenmanagerapp import ScreenManagerApp
from modules.songs.songs import Songs
from modules.reacontrol.reacontrol import ReaControl
from modules.setlists.setlist import SetList



async def main():
    daw = ReaControl()
    songs = Songs()
    setlist = SetList()
    modules = {
        'daw': daw,
        'songs': songs,
        'setlist': setlist
    }
    ScreenManagerApp(modules=modules).run()        


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
