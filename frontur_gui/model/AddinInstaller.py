from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from frontur_gui.model.ComputeDialog import ComputeDialog

class AddinInstaller(BoxLayout):
    def run_installer():
        installer = AddinRun()
        content = ComputeDialog(loading_method=installer.run, cancel=AddinInstaller.dismiss_popup,
                            callback=AddinInstaller.callback)
        AddinInstaller._popup = Popup(title="Excel Addin Installer", content=content,
                            size_hint=(0.9, 0.9), auto_dismiss=False)
        AddinInstaller._popup.bind(on_open=AddinInstaller._popup.content.compute)
        AddinInstaller._popup.open()

    def dismiss_popup():
        AddinInstaller._popup.dismiss()
        
    def callback():
        pass

class AddinRun():
    fully_loaded = False
    execution_end = False

    def run(self):
        try:
            import subprocess
            child = subprocess.run(["xlwings", "addin", "install"],
                              universal_newlines = True,
                              stdout = subprocess.PIPE)
            for log in child.stdout.splitlines():
                yield log
            self.fully_loaded = True
            yield 'Finished.'
        except Exception as err:
            yield str(err)
        finally: 
            self.execution_end = True
