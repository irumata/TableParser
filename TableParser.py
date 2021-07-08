import pandas as pd


#class to store change 
class TableChange:
    def _init_(self, index, old_value, comment="", probability = 1):
        self.index=index
        seld.old_value = old_value
        self.comment = comment
        self.probability = probability

#class for on heuristic
class TableParserItem:
    def __init__(self):
        pass
    def parse(self, series: pd.Series):
        pass
        
    
#Class to apply all heuristic    
class TableParser:
    def __init__(self, table_parsers):
        if (table_parsers) != list:
            table_parsers = [table_parsers]
        self.table_parsers = table_parsers
    
    def parse(self, series: pd.Series):
        result = [series,[]]
        for table_parser in self.table_parsers:
            new_series, new_changes = table_parser.parse(series)
            result[0] = new_series
            result[1]+=(new_changes)
        return result
            