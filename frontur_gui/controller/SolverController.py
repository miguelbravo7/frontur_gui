from pandas import DataFrame, pandas
from ortools.linear_solver import pywraplp
from frontur_utilities.solver_df import df_solver
import re
import json
import frontur_utilities.utility_fileloader as df_fileloader

class SolverController() :
    fully_loaded = False
    execution_end = False
    def __init__(self, filename, solver_parameters):
        self.filename = filename
        self.solver_parameters = solver_parameters

    def __str__(self):
        return str(self.data_frame)

    def run(self):
        try:
            yield 'Dataframe load'
            self.data_frame = df_fileloader.load_agenda(self.filename)
            yield 'Calculating results... (this may take a few minutes)'
            self.data_frame = df_solver(self.data_frame, no_groups=True, parameters=self.solver_parameters)
            yield 'Finished'
            import io
            buf = io.StringIO()
            self.data_frame.info(buf=buf)
            yield buf.getvalue()
            self.fully_loaded = True
        except Exception as err:
            yield str(err)
        finally: 
            self.execution_end = True