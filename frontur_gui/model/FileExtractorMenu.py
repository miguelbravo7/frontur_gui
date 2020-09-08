from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from frontur_gui.controller.ExtractorController import ExtractorController
from frontur_gui.model.FileManagerLoad import FileManagerLoad
from frontur_gui.model.ComputeDialog import ComputeDialog
import frontur_utilities.constants as const
import os
import json

class FileExtractorMenu(BoxLayout):    
    extracted_df = ObjectProperty(None)   
    save_btn = ObjectProperty(None)   
    
    def __init__(self, **kwargs):
        super(FileExtractorMenu, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.set_label_values())

    @property
    def is_save_disabled(self): 
        return not self.extracted_df.fully_loaded

    def set_label_values(self):        
        data = vars(const)
        for child in reversed(self.container.children):
            if isinstance(child, TextInput):
                child.text = str(data[child.keyword])
            elif isinstance(child, FileManagerLoad):
                child.ids.text_input.text = str(data[child.keyword])

    def get_dict_values(self):
        self.interface_values = {}
        mapped_results = {}
        aliases = { 'FRONTUR_FILE_PATH': 'frontur', 'DAYS_FILE_PATH': 'available_days', 'SUBSTITUTIONS_FILE_PATH': 'aliases', 'PLANES_DATA_FILE_PATH': 'planes', 'airport': 'airport'}
        for child in reversed(self.container.children):
            if isinstance(child, TextInput) or isinstance(child, FileManagerLoad):
                self.interface_values[child.keyword] = child.text
                mapped_results[aliases[child.keyword]] = child.text
        return mapped_results
    
    def save_configuration(self):
        import frontur_utilities
        dir_path = os.path.dirname(frontur_utilities.__file__)
        data = {}
        with open(dir_path + '/data/config.json') as f:
            data = json.load(f)
        with open(dir_path + '/data/config.json', 'w') as f:
            modified_data = {**data, **self.interface_values}
            f.write(json.dumps(modified_data, indent=4, sort_keys=False))

    def run_extractor(self):
        a = self.get_dict_values()
        self.extracted_df = ExtractorController(**a)
        content = ComputeDialog(loading_method=self.extracted_df.run, cancel=self.dismiss_popup,
                            callback=self.callback)
        self._popup = Popup(title="Extracting file information", content=content,
                            size_hint=(0.9, 0.9), auto_dismiss=False)
        self._popup.bind(on_open=self._popup.content.compute)
        self._popup.open()        
        
    def dismiss_popup(self):
        self.save_configuration()
        self._popup.dismiss()
        
    def callback(self):
        self.save_btn.disabled = self.is_save_disabled
        if not self.is_save_disabled:
            self.save_btn.data_frame = self.extracted_df.data_frame
