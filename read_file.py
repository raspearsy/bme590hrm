import pandas as pd

# Input file as a Pandas DataFrame

def input_dataframe(file="ecg_data.csv"):
    """
    :return: An dataframe for the time and voltage ecg data
    """

    ecg_dataframe = pd.read_csv(file, names=['time', 'voltage'], skiprows=1)
    return ecg_dataframe

if __name__ == "__main__":
    input_dataframe()
