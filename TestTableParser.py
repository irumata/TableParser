import TableParser
import pandas as pd
import tempfile, zipfile
import os

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
            'Sept':'09',
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
            'A': '4',
            'S': '5',
            r'[ -/]|[:-@]|[\[-_]|[{-~]': '-',
        }
        for key, val in mistake.items():
            series = series.str.strip().str.replace(key, val, regex=True)
        return (pd.to_datetime(series, errors="ignore"), [])

    def fix_xlsx(self, in_file):
        tmpfd, tmp = tempfile.mkstemp(dir=os.path.dirname(in_file))
        os.close(tmpfd)
        filename = '[Content_Types].xml'
        data = ''
        with zipfile.ZipFile(in_file, 'r') as zin:
            with zipfile.ZipFile(tmp, 'w') as zout:
                for item in zin.infolist():
                    if item.filename != filename:
                        zout.writestr(item, zin.read(item.filename))
                    else:
                        data = zin.read(filename).decode()
        os.remove(in_file)
        os.rename(tmp, in_file)
        data = data.replace('/xl/sharedStrings.xml', '/xl/SharedStrings.xml')
        with zipfile.ZipFile(in_file, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(filename, data)

    ###############################################
    # to find the x,y coordinate of row with date #
    def find_coordinate(self, x, y, df):
        for i in range(df.shape[0]):
            if df.iloc[i, 0] == 'Дата на начало периода':
                x = i
                break
        for j in range(1, df.shape[1]):
            if type(df.iloc[x, j]) == type('string'):
                y = j
                break
        return x, y

    def all_action(self,df):
        data_row_num, data_col_num = self.find_coordinate(0, 0, df)
        date = df.iloc[data_row_num, data_col_num:].reset_index(drop=True)  # <--- Series with date (01.03.2016;...)
        table = df.iloc[data_row_num:, data_col_num:].reset_index(drop=True)  # <--- all useful data
        date = self.parse(date) # < --- parse date for correction
        table.iloc[0] = date[0] # < --- set new call date to the table
        print(table.iloc[0].reset_index(drop=True))  # check of new date in data  ##(((JUST switch ON/OFF)))##
        table.columns = table.iloc[0] # <--- change column names
        table = table.iloc[1:, :] # <--- remove first row
        return table


# parserClass = TestTableParser()
# parserClass.fix_xlsx('file2.xlsx')
# df = pd.read_excel('file2.xlsx')
# parserClass.all_action()