from pandas import DataFrame, pandas
import re
import json
import frontur_utilities.extract_methods as em
import frontur_utilities.utility_fileloader as df_fileloader

class ExtractorController() :
    fully_loaded = False
    execution_end = False
    def __init__(self, frontur, airport, available_days, planes, aliases=''):
        self.frontur = frontur
        self.airport = airport
        self.available_days = available_days
        self.planes = planes
        self.aliases = aliases

    def __str__(self):
        return self.data_frame.__str__()

    def run(self):
        try:
            yield 'Loading dataframe...'
            self.data_frame = df_fileloader.load_agenda(self.frontur)
            yield 'Selecting airport'
            self.data_frame = em.select_airport(self.data_frame, self.airport)
            if self.aliases: 
                yield 'Substituting values'     
                em.substitute_values(self.data_frame, self.aliases)
            yield 'Merging plane data'
            self.data_frame = em.add_plane_data(self.data_frame, self.planes)
            yield 'Formatting days'
            self.data_frame = em.format_dates(self.data_frame)
            yield 'Selecting days'
            self.data_frame = em.select_days(self.data_frame, self.available_days)
            self.fully_loaded = True
            yield 'Finished.'            
            import io
            buf = io.StringIO()
            self.data_frame.info(buf=buf)
            yield buf.getvalue()
        except Exception as err:
            yield str(err)
        finally: 
            self.execution_end = True
