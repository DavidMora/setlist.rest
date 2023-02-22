from modules.songs.song import Song

class Songs:
    def __init__(self):
        self.songs = []
    
    def add_song(self, song: Song):
        self.songs.append(song)
    
