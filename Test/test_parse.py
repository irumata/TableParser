import pytest
import pandas as pd
from pparser import TestTableParser

def test_parse_res():
    verify=r"C:\Users\ganinby\Documents\TableParser-main\zero.xlsx"

    testTableParser = TestTableParser()
    xlsx = pd.ExcelFile(verify)
    names = xlsx.sheet_names
    sheet_to_df_map = {}
    for i in range(len(names)):
        data=pd.read_excel(open(verify, 'rb'), header=None, sheet_name=names[i])
        sheet_to_df_map[names[i]] = testTableParser.all_action(data)
    
    answer=sheet_to_df_map.get(names[0])[0]
    json=sheet_to_df_map.get(names[0])[1]
    t=True if ((data.shape[0]-1) == answer.shape[0] and data.shape[1] == answer.shape[1]) else False

    assert t==True, "Failed"

    if t == True:
        for j in range (0, answer.shape[1]):
            t = True if answer.iloc[:,j].equals(data.iloc[:,j]) else False
    
    assert t==True, "Not equal"