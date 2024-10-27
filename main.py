from ctypes import alignment
from genericpath import isdir
import glob
import os
import shutil


from kivy.config import Config
Config.set("graphics", "resizable", False)
Config.set("graphics", "width", 650)
Config.set("graphics", "height", 600)

from kivy.app import App
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label


Chapters = dict[str, dict[str, list[str]] | list[str]]


CHAPTERS: Chapters = {
    "1 - Summer": {
        "Chapter 1": [],
        "Chapter 2": [],
        "Chapter 3": [],
        "Chapter 4": [],
    },
    "2 - Fall": {
        "Chapter 1": [],
        "Chapter 2": [],
        "Chapter 3": [],
        "Chapter 4": [],
        "Chapter 5": [],
        "Chapter 6": [],
    },
    "3 - Winter": {
        "Chapter 1": [],
        "Chapter 2": [],
        "Chapter 3": [],
        "Chapter 4": [],
        "Chapter 5": [],
    },
    "4 - Spring": [],
}

ROOT_DIR = r"resources\saves"
USER_PROFILE_PATH = os.getenv("USERPROFILE")
if not USER_PROFILE_PATH:
    exit()
NEVA_SAVE_LOCATION = os.path.join(USER_PROFILE_PATH, "AppData", "LocalLow", "nomada studio", "Neva")


def get_all_save_file_names(path: str) -> list[str]:
    return [s[:-4] for s in glob.glob(root_dir=path, pathname="*.png")]


def get_all_chapters() -> Chapters:
    for season in CHAPTERS:
        if isinstance(CHAPTERS[season], list):
            CHAPTERS[season] = get_all_save_file_names(os.path.join(ROOT_DIR, season))
            continue
        for chapter in CHAPTERS[season]:
            CHAPTERS[season][chapter] = get_all_save_file_names(os.path.join(ROOT_DIR, season, chapter))

    return CHAPTERS


class SaveTreeNode(TreeViewLabel):
    def __init__(self, *args, image_path: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_path: str = image_path

    def on_touch_down(self, touch):
        self.parent.parent.parent.children[0].source = self.image_path
        
        return super().on_touch_down(touch)


def build_tree() -> TreeView:
    tree_view = TreeView(root_options={"text": "Seasons"}, size_hint=(.3, None))

    chapters = get_all_chapters()
    for season in chapters:
        tree_season = tree_view.add_node(TreeViewLabel(text=season))
        if isinstance(chapters[season], list):
            for save_file in chapters[season]:
                tree_view.add_node(SaveTreeNode(text=save_file, image_path=os.path.join(ROOT_DIR, season, save_file + ".png")), tree_season)
            continue
        for chapter in chapters[season]:
            tree_chapter = tree_view.add_node(TreeViewLabel(text=chapter), tree_season)
            for save_file in chapters[season][chapter]:
                tree_view.add_node(SaveTreeNode(text=save_file, image_path=os.path.join(ROOT_DIR, season, chapter, save_file + ".png")), tree_chapter)

    return tree_view


def load_save(instance, value):
    node = instance.parent.children[-1].children[0].selected_node
    if node is None or not isinstance(node, SaveTreeNode):
        instance.parent.children[-2].text = "No Save File Selected."
        instance.parent.children[-2].color = (1, 0, 0)
        return
    
    # Find Neva folder in case its not always the same name
    neva_folder_content = os.listdir(NEVA_SAVE_LOCATION)
    for folder in neva_folder_content:
        if folder == "Unity":
            continue
        save_folder = os.path.join(NEVA_SAVE_LOCATION, folder, "Save01")
        shutil.copy(node.image_path[:-4] + ".gs", os.path.join(save_folder, "Progress.gs"))
        instance.parent.children[-2].text = "Done."
        instance.parent.children[-2].color = (0, 1, 0)




class NevaSaveManagerApp(App):
    def build(self):
        float_layout = FloatLayout(size=(650, 600))

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        tree_view = build_tree()
        tree_view.bind(minimum_height=tree_view.setter("height"))

        scroll_view.add_widget(tree_view)

        
        image = Image(size=(384, 216), size_hint=(.59, .36), pos=(230, 350))

        label = Label(size=(300, 100), size_hint=(.1, .3), pos=(370, 50), halign="left", valign="middle")
        label.text_size = label.size

        load_button = Button(text="Load", size_hint=(.2, .08), pos=(250, 50))
        load_button.bind(state=load_save)
        exit_button = Button(text="Exit", size_hint=(.2, .08), pos=(480, 50))
        exit_button.bind(state=lambda i, v: self.stop())

        float_layout.add_widget(scroll_view)
        float_layout.add_widget(label)
        float_layout.add_widget(load_button)
        float_layout.add_widget(exit_button)
        float_layout.add_widget(image)

        return float_layout


if __name__ == '__main__':
    NevaSaveManagerApp().run()
