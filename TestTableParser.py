import TableParser
import pandas as pd
class TestTableParser(TableParser.TableParserItem):
    def __init__(self):
        pass
    def parse(self, series: pd.Series):
        return (pd.to_datetime(series.str.replace("O","0"), errors = "ignore"), [])
        