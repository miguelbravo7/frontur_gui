from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from pandas import Timedelta
from frontur_gui.model.ComputeDialog import ComputeDialog
from frontur_gui.model.FileManagerLoad import FileManagerLoad
from frontur_gui.controller.SolverController import SolverController
import frontur_utilities.constants as const
import os
import json

class FileSolverMenu(BoxLayout):
    container = ObjectProperty(None)
    save_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FileSolverMenu, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.set_label_values())

    @property
    def is_save_disabled(self):
        return not self.solver_df.fully_loaded

    def set_label_values(self):
        data = vars(const)
        for child in reversed(self.container.children):
            if isinstance(child, TextInput):
                child.text = str(data[child.keyword])
            elif isinstance(child, FileManagerLoad):
                child.ids.text_input.text = str(data[child.keyword]) if child.keyword in data else ''

    def get_dict_values(self):
        self.interface_values = {}
        for child in reversed(self.container.children):
            if isinstance(child, TextInput):
                self.interface_values[child.keyword] = float(child.text)
            elif isinstance(child, FileManagerLoad):
                self.interface_values[child.keyword] = child.text
        import json
        with open(self.interface_values['REQ_INTERVIEWS_FILE_PATH']) as jfile:
            data = json.load(jfile)
        return {
            "filename": self.interface_values['SOLVER_FILE_PATH'],
            'solver_parameters': {
                'workday_time': Timedelta(hours=float(self.interface_values['workday_time'])).seconds,
                'rest_time': Timedelta(minutes=float(self.interface_values['rest_time'])).seconds,
                'execution_time_limit': Timedelta(minutes=float(self.interface_values['execution_time_limit'])).seconds,
                'country_kwargs': {
                    'plane_kwargs': {
                        'seats_used': float(self.interface_values['seats_used']),
                        'poll_success': float(self.interface_values['poll_success']),
                        'poll_time': Timedelta(seconds=float(self.interface_values['poll_time'])).seconds
                    },
                    'interviews': data
                }
            }
        }
    
    def save_configuration(self):
        import frontur_utilities
        dir_path = os.path.dirname(frontur_utilities.__file__)
        data = {}
        with open(dir_path + '/data/config.json') as f:
            data = json.load(f)
        with open(dir_path + '/data/config.json', 'w') as f:
            modified_data = {**data, **self.interface_values}
            f.write(json.dumps(modified_data, indent=4, sort_keys=False))

    def run_solver(self):
        self.solver_df = SolverController(**self.get_dict_values())
        content = ComputeDialog(loading_method=self.solver_df.run, cancel=self.dismiss_popup,
                                callback=self.callback)
        self._popup = Popup(title="Solving file", content=content,
                            size_hint=(0.9, 0.9), auto_dismiss=False)
        self._popup.bind(on_open=self._popup.content.compute)
        self._popup.open()

    def dismiss_popup(self):
        self.save_configuration()
        self._popup.dismiss()

    def callback(self):
        self.save_btn.disabled = self.is_save_disabled
        if not self.is_save_disabled:
            self.save_btn.dataframe = self.solver_df.data_frame
