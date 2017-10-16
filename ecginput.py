import pandas as pd

class ECGInput():
    """Input Class

    """

    def __init__(self, file="ecg_data.csv"):
        self.file = file
        self.ecg_dataframe = self.read_input()

    def read_input(self):
        """Read in a CSV file and convert it into a DataFrame with the columns being time and voltage"

        :return: An DataFrame for the time and voltage ecg data
        """

        try:
            self.ecg_dataframe = pd.read_csv(self.file, names=['time', 'voltage'], skiprows=1)
            if len(self.ecg_dataframe) == 0:
                raise Exception("No data found")
            self.ecg_dataframe['time'] = pd.to_numeric(self.ecg_dataframe['time'], errors = 'coerce')
            self.ecg_dataframe['voltage'] = pd.to_numeric(self.ecg_dataframe['voltage'], errors = 'coerce')
            self.ecg_dataframe = self.ecg_dataframe.dropna()

        except FileNotFoundError:
            raise FileNotFoundError("File Not Found")
        except ValueError:
            raise ValueError("Invalid data, Non-Numeric types present")
        else:
            return self.ecg_dataframe
