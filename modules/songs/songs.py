from modules.songs.song import Song

class Songs:
    def __init__(self):
        self.songs = []
    
    def add_song(self, song: Song):
        self.songs.append(song)
    def set_songs(self, songs: list):
        self.songs = []
        for song in songs:
            self.add_song(Song(song[0], song[1]))
    def get_song_by_position(self, position: int):
        for song in self.songs:
            if song.position == position:
                return song
        return None
    def __len__(self):
        return len(self.songs)
    def __getitem__(self, index):
        return self.songs[index]
    def __iter__(self):
        return iter(self.songs)
    
        
    
