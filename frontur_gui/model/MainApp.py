from kivy.app import App
from kivy.lang import Builder
import frontur_gui.model.ScreenManagement

class MainApp(App):
    def build(self):
        return Builder.load_file("frontur_gui/view/MainScreen.kv")