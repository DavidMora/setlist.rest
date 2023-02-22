import unittest
from modules.songs.songs import Songs
from modules.songs.song import Song

class TestSongs(unittest.TestCase):
    def setUp(self):
        self.songs = Songs()
    def test_song_is_added(self):
        self.songs.add_song(Song('FIRST HIT', 1))
        self.assertEqual(len(self.songs.songs), 1)