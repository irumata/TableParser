import TableParser
import pandas as pd


class TestTableParser(TableParser.TableParserItem):
    def __init__(self):
        pass
    
    def parse(self, series: pd.Series):
        mistake = {
            'Jan':'01',
            'Feb': '02',
            'Mar':'03',
            'Apr':'04',
            'May':'05',
            'Jun':'06',
            'Jul':'07',
            'Aug':'08',
            'Sep':'09',
            'Oct':'10',
            'Nov':'11',
            'Dec':'12',
            'o': '0',
            'l': '1',
            'b': '6',
            'g': '9',
            'q': '9',
            't': '7',
            'v': '5',
            'G': '6',
            'F': '7',
            'Z': '2',
            'Q': '2',
            'B': '8',
            'O': '0',
            'D': '0',
            'E': '3',
            'A': '4444',
            'S': '5',
            r'[ -/]|[:-@]|[\[-_]|[{-~]': '-',
        }
        for key, val in mistake.items():
            series = series.str.replace(key, val, regex=True)
            # print(series)
        return (pd.to_datetime(series, errors="ignore"), [])
