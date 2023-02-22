from kivymd.uix.selection.selection import MDSelectionList
from kivymd.uix.list import (OneLineIconListItem, IconLeftWidget)

class SetlistView(MDSelectionList):
    def __init__(self, **kwargs):
        super(SetlistView, self).__init__(**kwargs)
        self.selected_mode = True
        self.icon = 'music'
    def populate(self):
        for i in range(20):
            self.add_widget(
                OneLineIconListItem(
                    IconLeftWidget(icon='music'),
                    None,
                    text=f"Single-line item {i}"
                )    
            )
    def on_unselected(self, *_):
        self.selected_mode = True