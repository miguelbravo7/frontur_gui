from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class FileManagerLoad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loadfile = ObjectProperty(None)
        self.savefile = ObjectProperty(None)
        self.text_input = ObjectProperty(None)
        self.keyword = StringProperty("None")

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.ids.text_input.text = filename[0]
        self.dismiss_popup()

    def save_on_dictionary(self, dictionary):
        dictionary[self.keyword] = self.ids.text_input.text

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)