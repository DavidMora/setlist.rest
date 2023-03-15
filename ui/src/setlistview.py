from kivymd.uix.selection.selection import MDSelectionList
from kivymd.uix.list import (OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget)
from modules.helpers.constants import marker_prefix_for_setlist
from kivy.animation import Animation

class SetlistView(MDSelectionList):
    def __init__(self, **kwargs):
        super(SetlistView, self).__init__(**kwargs)
        self.selected_mode = True
        self.icon = 'music'
    def populate(self, items: list) -> None:
        selected_items = self.get_selected_ids()
        self.clear_widgets()
        for song in items:
            self.add_widget(
                OneLineAvatarIconListItem(
                    IconLeftWidget(icon='music'),
                    IconRightWidget(icon=song.playing) if song.playing else None,
                    text=song.title,
                    id=f"{marker_prefix_for_setlist}{song.id}-{song.position}"
                )    
            )        
        for child in self.children:
            if child.children[1].id in selected_items:
                Animation(scale=1, d=0.01).start(child.instance_icon)
                child.selected = True
                child._progress_animation = False 
                child.owner.dispatch("on_selected", child)
    def on_unselected(self, *_) -> None:
        self.selected_mode = True
    def get_selected_ids(self) -> list:
        markers = [x.children[1].id for x in self.get_selected_list_items()]
        return markers