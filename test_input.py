import pandas as pd
import numpy as np
from read_file import input_dataframe

# requires test .csv file containing 2 columns w/ 1 row string header and all below rows float/int


def test_ecg_dataframe_size():
    """.. function:: test_ecg_dataframe_size()

    Test size of dataframe.

    """
    ecg_dataframe = input_dataframe("testfile1.csv")
    assert ecg_dataframe.shape[1] == 2


def test_ecg_dataframe_type():
    """.. function:: test_ecg_dataframe_type()

    Test type of dataframe.

    """
    ecg_dataframe = input_dataframe("testfile1.csv")
    assert isinstance(ecg_dataframe, pd.DataFrame)
    assert isinstance(ecg_dataframe.time[0], np.float64) or isinstance(ecg_dataframe.time[0], np.int64)
    assert isinstance(ecg_dataframe.voltage[0], np.float64) or isinstance(ecg_dataframe.voltage[0], np.int64)


def test_exception_nofile():
    """.. function:: test_exception_nofile()

    Test that file can be found.

    """
    try:
        input_dataframe("")
        assert False
    except FileNotFoundError:
        assert True


def test_exception_nonnumeric_values():
    """.. function:: test_exception_nonnumeric_values()

    Test for non-numeric values.
    """
    try:
        ecg_nonnumeric_dataframe = input_dataframe("test_non_numeric.csv")
        pd.to_numeric(ecg_nonnumeric_dataframe['time'])
        pd.to_numeric(ecg_nonnumeric_dataframe['voltage'])
        assert False
    except ValueError:
        assert True

def test_exception_empty_file():
    """.. function:: test_exception_empty_file()

    Test if dataframe is empty.
    """
    assert len(input_dataframe("test_data_empty.csv")) == 0
