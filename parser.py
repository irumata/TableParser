import pandas as pd
import tempfile, zipfile
import os
import numpy as np
from collections import Counter


class TestTableParser:

    def __init__(self, IsVerticalOrientation=False, index_rows=[], columns_types={}, mistake_fix=[], start_point=0):
        self.IsVerticalOrientation = IsVerticalOrientation
        self.index_rows = index_rows
        self.columns_types = columns_types
        self.mistake_fix = mistake_fix
        self.start_point = start_point

    def parse(self, series: pd.Series):
        mistake = {
            "00:00:00": '', '0:00': '',
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sept': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
            'o': '0', 'l': '1', 'b': '6', 'g': '9', 'q': '9', 't': '7', 'v': '5', 'G': '6', 'F': '7', 'Z': '2',
            'Q': '2', 'B': '8', 'O': '0', 'D': '0', 'E': '3', 'A': '4', 'S': '5',
            r'[ -/]|[:-@]|[\[-_]|[{-~]': '-',
        }
        for key, val in mistake.items():
            series = series.str.strip().str.replace(key, val, regex=True)
#             coerce
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

    def orientation_determine(self, df):
        list_columns = []
        for j in range(df.shape[1]):
            list_columns.append(pd.to_numeric(df.iloc[:, j], errors='coerce').dropna())
        clear_df = pd.concat(list_columns, axis=1)
        if clear_df.shape[0] > clear_df.shape[1]:
            self.IsVerticalOrientation = True
            return self.IsVerticalOrientation
        else:
            self.IsVerticalOrientation = False
            return self.IsVerticalOrientation

    def find_start_point(self, clear_df):
        for i in range(clear_df.shape[0]):
            if len(clear_df.iloc[i, :].dropna()) > 2:
                self.start_point = i
                break
        return self.start_point

    def define_type_of_cell(self, clear_df, df_data, start_point):
        for j in range(clear_df.shape[1]):
            baff = clear_df.iloc[:, j].dropna()
            if baff.sum() != 0:
                if baff.dtype == pd.Float64Dtype():
                    self.columns_types[j] = 'float'
                else:
                    self.columns_types[j] = 'int'
            else:
                if type(self.parse(df_data.iloc[:, j].astype(str))[0][start_point]) == type(pd.to_datetime('31.01.2002')):
                    self.columns_types[j] = 'date'
                elif baff.dtype == pd.BooleanDtype():
                    self.columns_types[j] = 'bool'
                else:
                    self.columns_types[j] = 'str'
        return self.columns_types

    def define_breakline(self, clear_df, columns_types):
        null_list, index_list = [], []
        for j in range(clear_df.shape[1]):
            if columns_types[j] == 'int':
                null_list.append(clear_df.iloc[:, j])
        int_df = pd.concat(null_list, axis=1)
        count = Counter(columns_types.values())
        for i in range(int_df.shape[0]):
            if int_df.iloc[i, :].isnull().sum() == count.get('int'):
                index_list.append(i)

        return index_list

    def create_list_of_table(self, df, break_line, start_point):
        self.index_rows = [df.iloc[:break_line[0] + start_point, :], df.iloc[break_line[0] + start_point:, :]]
        return self.index_rows

    def create_header(self, df, start_point, df_data):
        cols = []
        count = 1
        topic = df.iloc[:start_point, :].fillna(method='ffill', axis=1)
        list_topic = []
        for i in range(topic.shape[1]):
            list_topic.append("__".join(list(topic.iloc[:, i].astype(str))).replace("__nan", "").replace("nan__", ""))
        for column in list_topic:
            if column in cols:
                cols.append("{0}_{1}".format(str(column), str(count)))
                count += 1
                continue
            cols.append(column)
        df_data.columns = cols
        return df_data

    def to_numeric_func(self, df):
        list_columns = []
        for j in range(df.shape[1]):
            list_columns.append(pd.to_numeric(df.iloc[:, j], errors='coerce').convert_dtypes())
        clear_df = pd.concat(list_columns, axis=1)
        return clear_df

    def json_creator(self, df, mistake, orientation, columns_types, break_line, index):
        if len(break_line) == 0:
            self.index_rows = [df.index.tolist()]
            return {"IsVerticalOrientation,": orientation,
                    "Index rows": self.index_rows,
                    "columns types": columns_types,
                    "mistake fix": mistake
                    }
        else:
            return {"IsVerticalOrientation,": orientation,
                    "Index rows": index,
                    "columns types": columns_types,
                    "mistake fix": mistake
                    }

    def find_errorss(self, s, j):
        mistake = {'o': '0', 'l': '1', 'b': '6', 'g': '9', 'q': '9', 't': '7', 'v': '5', 'f': '7', 'z': '2', 'e': '3',
                   's': '5'}
        for key, val in mistake.items():
            if len(s[s.astype(str).str.contains(key).dropna()].index.to_list()) != 0:
                for i in range(len(s[s.astype(str).str.contains(key)].index.to_list())):
                    self.mistake_fix.append({'row': s[s.astype(str).str.contains(key)].index.to_list()[i],
                                         'column': j,
                                         'new value': val,
                                         'old value': key,
                                         'probability': 99.9,
                                         'user approve': False,
                                         'comment': False
                                         })
                s = s.astype(str).str.strip().str.replace(key, val, regex=True)
            else: continue 
        return [s, self.mistake_fix]

    def change_valuee(self, df, columns_types):
        df = df.copy()
        mistake_index_list = []
        for j in range(df.shape[1]):
            if columns_types[j] == 'int' or columns_types[j] == 'float':
                buff = self.find_errorss(df.iloc[:, j], j)
                df.iloc[:, j] = pd.to_numeric(buff[0], errors='coerce')
                mistake_index_list.append(buff[1])
        return [df, np.concatenate(np.array(mistake_index_list), axis=None).tolist()]

    def all_action(self, df):  # <-----    drive method
        orientation = self.orientation_determine(df)

#         print(orientation)
        if orientation == False:
            df = df.T

        clear_df = self.to_numeric_func(df)
        start_point = self.find_start_point(clear_df)
        columns_types = self.define_type_of_cell(clear_df.iloc[start_point:, :], df.iloc[start_point:, :], start_point)
        break_line = self.define_breakline(clear_df.iloc[start_point:, :], columns_types)
        if len(break_line) == 0:
            df_data_and_mistake = self.change_valuee(df.iloc[start_point:, :], columns_types)
            done_df = self.create_header(df, start_point, df_data_and_mistake[0])
            json = self.json_creator(df, df_data_and_mistake[1], orientation, columns_types, break_line, [])
            return [done_df, json]
        else:
            list_df = self.create_list_of_table(df, break_line, start_point)
            answer_df = []
            mistake = []
            index_list = []
            for i in range(len(list_df)):
                clear_df = self.to_numeric_func(list_df[i])
                start_point = self.find_start_point(clear_df)
                df_data_and_mistake = self.change_valuee(list_df[i].iloc[start_point:, :], columns_types)
                done_df = self.create_header(list_df[i], start_point, df_data_and_mistake[0])
                answer_df.append(done_df)
                mistake.append(df_data_and_mistake[1])
                index_list.append(list_df[i].index.tolist())
            json = self.json_creator(df, mistake, orientation, columns_types, break_line, index_list)
            return [answer_df, json]




