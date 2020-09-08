from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import threading

class ComputeDialog(FloatLayout):
    text_output = ObjectProperty(None)
    cancel = ObjectProperty(None)
    loading_method = ObjectProperty(None)
    callback = ObjectProperty(None)
    thread = ObjectProperty(None)

    def compute(self, instance):
        self.thread = threading.Thread(target=self.method)
        self.thread.start()

    def method(self):
        from datetime import datetime
        for step in self.loading_method():
            self.container.text += f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ' + step + '\n' 
        self.continue_btn.disabled = False
        self.callback()
