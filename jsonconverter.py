import pandas as pd
from flask import jsonify, Flask

app = Flask(__name__)

@app.route("/check")
def converter():
    file = "ecg_data.csv"
    ecg_dataframe = pd.read_csv(file, names=['time', 'voltage'], skiprows=1)
    if len(ecg_dataframe) == 0:
        raise Exception("No data found")
    ecg_dataframe['time'] = pd.to_numeric(ecg_dataframe['time'], errors='coerce')
    ecg_dataframe['voltage'] = pd.to_numeric(ecg_dataframe['voltage'], errors='coerce')
    ecg_dataframe = ecg_dataframe[abs(ecg_dataframe['voltage']) <= 300]
    ecg_dataframe = ecg_dataframe.reset_index()
    return jsonify(time=ecg_dataframe['time'].tolist(), voltage=ecg_dataframe['voltage'].tolist())