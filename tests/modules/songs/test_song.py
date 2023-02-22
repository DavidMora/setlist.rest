import unittest
from modules.songs.song import Song

class TestSong(unittest.TestCase):
    def test_createSongIsSuccess(self):
        song = Song('data',1)
        self.assertEqual(song.title, 'data')