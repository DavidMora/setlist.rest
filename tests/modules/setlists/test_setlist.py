import unittest
from modules.setlists.setlist import SetList

class TestSetList(unittest.TestCase):
    def test_songIsAppendedToSetList(self):
        setlist = SetList()
        setlist.append(1)
        self.assertEqual(len(setlist.setlist), 1)
    def test_songIsAppendedToEmptySetListAndWeightIs1000(self):
        setlist = SetList()
        setlist.append(1)
        self.assertEqual(setlist.setlist[-1]['weigth'], 1000)
    def test_secondSongIsAppendedToSetListAndWeightIs2000(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        self.assertEqual(setlist.setlist[-1]['weigth'], 2000)
    def test_thirdSongIsAppendedToSetListInBetween(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.append(3, 1500)
        self.assertEqual(setlist.setlist[1]['marker'], 3)    
    def test_thirdSongIsAppendedToSetListFirst(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.append(3, 500)
        self.assertEqual(setlist.setlist[0]['marker'], 3)   
    def test_getLastMarkerReturnsLastElement(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        self.assertEqual(setlist.getLastMarker(), 2)
    def test_findClosestIndexToTheRightByWeight(self):
        setlist = SetList()
        setlist.append(1, 100)
        setlist.append(2, 200)
        setlist.append(3, 300)
        self.assertEqual(setlist.findMarkerIndexByWeight(200), 1)
    def test_MarkerIsAppendedToSetListFirstWithExistingWeigth(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2, setlist.setlist[0]['weigth'])
        self.assertEqual(setlist.setlist[0]['marker'], 2)   
    def test_MarkerIsAppendedToSetListSecondWithExistingWeigth(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.append(3, setlist.setlist[1]['weigth'])
        self.assertEqual(setlist.setlist[1]['marker'], 3)  
    def test_createNodeReturnsCorrectSchema(self):
        setlist = SetList()
        node = setlist.createNode(1,100)
        self.assertEqual(node, {"marker":1, "weigth":100})
    def test_setlistStartsWithNoCurrentMarker(self):
        setlist = SetList()
        self.assertEqual(setlist.playing, -1)
    def test_emptySetlistNextDoesntIncrementsMarker(self):
        setlist = SetList()
        setlist.next()
        self.assertEqual(setlist.playing, -1)
    def test_setlistNextIncrementsMarker(self):
        setlist = SetList()
        setlist.append(1)
        setlist.next()
        self.assertEqual(setlist.playing, 0)
    def test_setlistNextIsCircular(self):
        setlist = SetList()
        setlist.append(1)
        setlist.next()
        setlist.next()
        self.assertEqual(setlist.playing, 0)
    def test_lengthIsZeroWhenEmpty(self):
        setlist = SetList()
        self.assertEqual(len(setlist), 0)
    def test_lengthIsOneWhenOneElement(self):
        setlist = SetList()
        setlist.append(1)
        self.assertEqual(len(setlist), 1)
    def test_getitemReturnsCorrectElement(self):
        setlist = SetList()
        setlist.append(1)
        self.assertEqual(setlist[0]['marker'], 1)
    def test_getitemReturnsCorrectElementWhenTwoElements(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        self.assertEqual(setlist[1]['marker'], 2)
    def test_setitemSetsCorrectElement(self):
        setlist = SetList()
        setlist.append(1)
        setlist[0] = setlist.createNode(2, 100)
        self.assertEqual(setlist[0]['marker'], 2)
    def test_setitemThrowsExceptionWhenIndexOutOfBounds(self):
        setlist = SetList()
        setlist.append(1)
        with self.assertRaises(IndexError):
            setlist[1] = setlist.createNode(2, 100)
    def test_setitemThrowsExceptionWhenDictHasNoMarker(self):
        setlist = SetList()
        setlist.append(1)
        with self.assertRaises(Exception):
            setlist[0] = {'weigth': 100}
    def test_setitemThrowsExceptionWhenDictHasNoWeigth(self):
        setlist = SetList()
        setlist.append(1)
        with self.assertRaises(Exception):
            setlist[0] = {'marker': 100}
    def test_restartResetsPlaying(self):
        setlist = SetList()
        setlist.append(1)
        setlist.next()
        setlist.restart()
        self.assertEqual(setlist.playing, -1)
    def test_nextSetsPlayingToMinusOneWhenEmpty(self):
        setlist = SetList()
        setlist.next()
        self.assertEqual(setlist.playing, -1)
    def test_nextSetsPlayingToZeroWhenOneElement(self):
        setlist = SetList()
        setlist.append(1)
        setlist.next()
        self.assertEqual(setlist.playing, 0)
    def test_nextSetsPlayingToZeroWhenTwoElements(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.next()
        self.assertEqual(setlist.playing, 0)
    def test_nextSetsPlayingToOneWhenTwoElements(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.next()
        setlist.next()
        self.assertEqual(setlist.playing, 1)
    def test_nextSetsPlayingToZeroWhenPlayingLast(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.next()
        setlist.next()
        setlist.next()
        self.assertEqual(setlist.playing, 0)
    def test_prevSetsPlayingToMinusOneWhenEmpty(self):
        setlist = SetList()
        setlist.prev()
        self.assertEqual(setlist.playing, -1)
    def test_prevSetsPlayingToZeroWhenOneElement(self):
        setlist = SetList()
        setlist.append(1)
        setlist.prev()
        self.assertEqual(setlist.playing, 0)
    def test_prevSetsPlayingToZeroWhenTwoElements(self):
        setlist = SetList()
        setlist.append(1)
        setlist.append(2)
        setlist.next()
        setlist.next()
        setlist.prev()
        self.assertEqual(setlist.playing, 0)



    
