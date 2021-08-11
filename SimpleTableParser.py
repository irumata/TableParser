import TableParser
import pandas as pd
class SimpleTableParser(TableParser.TableParserItem):
    def __init__(self):
        pass
    def parse(self, series: pd.Series):
#         return (pd.to_datetime(series, errors = "ignore"), [])
        return "pukaaaa"
        