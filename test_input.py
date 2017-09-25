import pandas as pd
from read_file.py import input_dataframe

ecg_dataframe=input_dataframe("testfile1.csv")

# requires test .csv file containing 2 columns w/ 1 row string header and all below rows float/int
def test_ecg_dataframe_size():
    assert ecg_dataframe.shape[0]==2

def test_ecg_dataframe_type():
    assert isinstance(ecg_dataframe, pd.DataFrame)
    assert isinstance(ecg_dataframe.time[0], float) or isinstance(ecg_dataframe.time[0], int)
    assert isinstance(ecg_dataframe.voltage[0], float) or isinstance(ecg_dataframe.time[0], int)

def test_exception_nofile():

def test_exception_emptyfile():

def test_exception_nonnumeric_values():
# need exceptions for file that doesn't exist; for empty file; for file w/ non-numeric values