import click
from frontur_gui.model.MainApp import MainApp

@click.group()
def cli():
    """Method that can be called my other modules to use the commands on this file"""
    pass

@cli.command('gui', short_help='graphical user frontur_gui', context_settings={"ignore_unknown_options": True})
def frontur_gui():
    r"""
·______   ______     ______     __   __     ______   __  __     ______    
/\  ___\ /\  == \   /\  __ \   /\ "-.\ \   /\__  _\ /\ \/\ \   /\  == \   
\ \  __\ \ \  __<   \ \ \/\ \  \ \ \-.  \  \/_/\ \/ \ \ \_\ \  \ \  __<   
·\ \_\    \ \_\ \_\  \ \_____\  \ \_\\"\_\    \ \_\  \ \_____\  \ \_\ \_\ 
··\/_/     \/_/ /_/   \/_____/   \/_/ \/_/     \/_/   \/_____/   \/_/ /_/ 
                                                                          
    
Program that processes various information from files giving a dataframe with concrete information about flights.
    """
    MainApp().run()