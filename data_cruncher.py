import pandas as pd

class DataCruncher:
    __df__ = None

    def __init__(self):
        self.__df__ = pd.DataFrame(columns=['bass', 'mid', 'treble', 'frequency'])


    def AddRow(self,time,bass,mid,treble,frequency):
        new_row = {'bass': bass, 'mid': mid, 'treble': treble,'frequency':frequency}
        self.__df__ = pd.concat([self.__df__, pd.DataFrame([new_row])], ignore_index=True)
 
    def AddMultipleRows(self,tbmdf):
        new_rows = pd.DataFrame(tbmdf, columns=['bass', 'mid', 'treble', 'frequency'])
        self.__df__ = pd.concat([self.__df__, new_rows], ignore_index=True)

    @property
    def Dataframe(self):
        return self.__df__

        