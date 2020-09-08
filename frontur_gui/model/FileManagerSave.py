from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from os.path import join, isdir
import frontur_utilities.utility_fileloader as df_fileloader

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
        
    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))


class FileManagerSave(Button):
    data_frame = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file",
                            content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        df_fileloader.dump_agenda(join(path, filename), self.data_frame)
        self.dismiss_popup()
