import pandas as pd

class Bioinput():
    """Input Class

    """

    def __init__(self, file="ecg_data.csv"):
        self.file = file

    def read_input(self):
        """Read in a CSV file and convert it into a DataFrame with the columns being time and voltage"

        :param file: A CSV file containing ECG Data with time (s) in the first column and voltage (mV) in the
        second column.
        :return: An DataFrame for the time and voltage ecg data
        """

        try:
            ecg_dataframe = pd.read_csv(self.file, names=['time', 'voltage'], skiprows=1)
            if len(ecg_dataframe) == 0:
                print("No data found")
                return ecg_dataframe
            ecg_dataframe['time'] = pd.to_numeric(ecg_dataframe['time'], errors = 'coerce')
            ecg_dataframe['voltage'] = pd.to_numeric(ecg_dataframe['voltage'], errors = 'coerce')
            ecg_dataframe = ecg_dataframe.dropna()

        except FileNotFoundError:
            raise FileNotFoundError("File Not Found")
        except ValueError:
            raise ValueError("Invalid data, Non-Numeric types present")
        else:
            return ecg_dataframe
