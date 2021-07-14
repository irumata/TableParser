import TableParser
import SimpleTableParser
import TestTableParser
import pandas as pd

simpleTableParser = SimpleTableParser.SimpleTableParser()
testTableParser =  TestTableParser.TestTableParser()

tableParser = TableParser.TableParser(testTableParser)

series = pd.Series(["09 01!2021", "07-02-2021", "07.02.2O21", "O7.02.2O21","O7/02/2O21",'O7@02@2O21','O7]02[2O21','O7~02|2O21'])
print(series)

print(tableParser.parse(series))