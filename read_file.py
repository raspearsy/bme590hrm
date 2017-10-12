import pandas as pd
# Input file as a Pandas DataFrame


def input_dataframe(file="ecg_data.csv"):
    """.. function :: input_dataframe(file="ecg_data.csv")
    
    Read in a CSV file and convert it into a DataFrame with the columns being time and voltage"

    :param file: A CSV file containing ECG Data with time (s) in the first column and voltage (mV) in the
    second column.
    :return: An DataFrame for the time and voltage ecg data
    """

    try:
        ecg_dataframe = pd.read_csv(file, names=['time', 'voltage'], skiprows=1)
        if len(ecg_dataframe) == 0:
            print("No data found")
            return ecg_dataframe
        pd.to_numeric(ecg_dataframe['time'])
        pd.to_numeric(ecg_dataframe['voltage'])
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")
    except ValueError:
        raise ValueError("Invalid data, Non-Numeric types present")
    else:
        return ecg_dataframe

if __name__ == "__main__":
    print(input_dataframe())
