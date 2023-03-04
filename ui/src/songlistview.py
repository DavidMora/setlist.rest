from kivymd.uix.selection.selection import MDSelectionList
from kivymd.uix.list import (OneLineIconListItem, IconLeftWidget)
import modules.helpers.constants as constants

class SongListView(MDSelectionList):
    def __init__(self, **kwargs):
        super(SongListView, self).__init__(**kwargs)
        self.selected_mode = True
        self.icon = 'music'
        self.songs = None
    def populate(self):
        if not self.songs:
           return
        widgets = self.create_and_remove_widgets(self.children, self.songs, constants.marker_prefix_for_songlist)
        for widget in widgets['widgets_to_add']:
            self.add_widget(
                OneLineIconListItem(
                    IconLeftWidget(icon='music'),
                    None,
                    text=widget['title'],
                    id=widget['id']
                )    
            )
        for widget in widgets['widgets_to_remove']:
            self.remove_widget(widget)    
    def on_unselected(self, *_):
        self.selected_mode = True
    def arrow_right(self) -> list:
        markers = [x.children[1].id for x in self.get_selected_list_items()]
        self.unselected_all()
        self.on_unselected()
        return markers
    def create_and_remove_widgets(self,children: list, songs: list, prefix: str) -> dict:
        existing_children = {}
        widgets_to_add = []
        widgets_to_remove = []
        for child in children:
            existing_children[child.children[1].id] = {'child': child, 'checked': 0}
        if songs:
            for song in songs:
                id = f"{prefix}{song.position}" 
                if id in existing_children:
                    existing_children[id]['checked'] += 1 
                    existing_children[id]['child'].children[1].text = song.title
                if id not in existing_children:
                    widgets_to_add.append({'title': song.title, 'id': id})
        for child in existing_children:
            if not existing_children[child]['checked']:
                widgets_to_remove.append(existing_children[child]['child'])
        return {'widgets_to_add': widgets_to_add, 'widgets_to_remove': widgets_to_remove}