
class SetList:
    def __init__(self):
        self.setlist = []
        self.playing = -1
    def append(self, marker: int, weigth: float = -1) -> None:
        if weigth == 0:
            return
        if weigth == -1:
            new_weigth = 1000
            if len(self.setlist) > 0:
                new_weigth = self.setlist[-1]['weigth'] + 1000
            self.setlist.append(self.createNode(marker, new_weigth))
        else:
            index_to_insert_in = self.findMarkerIndexByWeight(weigth)
            if index_to_insert_in == -1:
                index_to_insert_in = self.findClosestIndexToTheLeftByWeight(weigth)
                new_weigth = weigth
            elif index_to_insert_in == 0:
                new_weigth = weigth/2
            else: 
                left_weigth = self.setlist[index_to_insert_in - 1]['weigth']
                right_weigth = self.setlist[index_to_insert_in]['weigth']
                new_weigth = left_weigth + (left_weigth + right_weigth)/2
            self.setlist.insert(index_to_insert_in, self.createNode(marker,weigth))
            
    def getLastMarker(self) -> int: 
        return self.setlist[-1]['marker']
    def findClosestIndexToTheLeftByWeight(self, weigth: float) -> int:
        for i in range(len(self.setlist)):
            if self.setlist[i]['weigth'] > weigth:
                return i
        return len(self.setlist)
    def findMarkerIndexByWeight(self, weigth: float) -> int:
        for i in range(len(self.setlist)):
            if self.setlist[i]['weigth'] == weigth:
                return i
        return -1
    def createNode(self, marker: int, weigth: float) -> dict:
        node = {'marker': marker, 'weigth': weigth}
        return node
    def next(self) -> None:
        if len(self.setlist) == 0:
            self.playing = -1
            return
        self.playing += 1
        if self.playing >= len(self.setlist):
            self.playing = 0
    def prev(self) -> None:
        if len(self.setlist) == 0:
            self.playing = -1
            return
        self.playing -= 1       
        if self.playing < 0:
            self.playing = len(self.setlist) - 1
    def restart(self):
        self.playing = -1
    def __len__(self) -> int:
        return len(self.setlist)
    def __getitem__(self, index: int) -> dict:
        return self.setlist[index]
    def __setitem__(self, index: int, value: dict) -> None:
        # validate that value has a key 'marker' and 'weigth'
        if not 'marker' in value:
            raise Exception('value must have a key "marker"')
        if not 'weigth' in value:
            raise Exception('value must have a key "weigth"')
        self.setlist[index] = value
