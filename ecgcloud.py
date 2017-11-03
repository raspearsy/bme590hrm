from flask import Flask, request, jsonify, abort
from ecgmeasure import ECGMeasure
import pandas as pd

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
# probably not the most elegant way of doing this, but should work
# more ideal to use something innate to the post to increment the counter
request_counter = 0


@app.route("/api/requests")
def requests():
    """.. function:: requests()

    Provides the number of requests

    """
    global request_counter
    request_counter = request_counter + 1

    return jsonify(request_counter)


@app.route("/api/heart_rate/summary", methods=['POST'])
def summary():
    """.. function:: summary()

    Provides a summary of heart rate data

    """
    global request_counter
    request_counter = request_counter + 1

    try:
        time = request.json['time']
        voltages = request.json['voltage']
        if len(time) == 0:
            raise Exception("No input data")
        if len(time) != len(voltages):
            raise Exception("Mismatched input data")
        hr_rawdata = pd.DataFrame.from_dict({'time': time, 'voltage': voltages})
        hr_rawdata['time'] = pd.to_numeric(hr_rawdata['time'], errors='coerce')
        hr_rawdata['voltage'] = pd.to_numeric(hr_rawdata['voltage'], errors='coerce')
        hr_rawdata = hr_rawdata.dropna(axis=0, how="any")
        hr_rawdata = hr_rawdata[abs(hr_rawdata['voltage']) <= 300]
        hr_rawdata = hr_rawdata.reset_index()
        if len(hr_rawdata) == 0:
            raise Exception("No valid input data")
    except Exception as e:
            abort(400, str(e))

    try:
        hr = ECGMeasure(rawdata=hr_rawdata)
        hr.hrdetector()
        hr.detect_rhythm()
    except Exception as e:
        abort(500)

    return jsonify(time=hr.data['time'].tolist(),
                   instantaneous_heart_rate=hr.data['HeartRate'].tolist(),
                   tachycardia_annotations=hr.data['tachycardia_annotations'].tolist(),
                   bradycardia_annotations=hr.data['bradycardia_annotations'].tolist())


@app.route("/api/heart_rate/average", methods=['POST'])
def average():
    """.. function:: average()

    Provides average heart rate data

    """
    global request_counter
    request_counter = request_counter + 1

    averaging_period = request.json['averaging_period']
    time = request.json['time']
    voltages = request.json['voltage']
    hr_rawdata = {'time': time, 'voltage': voltages}

    hr = ECGMeasure(rawdata=hr_rawdata)
    hr.acquire_avgper(averaging_period=averaging_period)
    hr.hrdetector_avg()
    hr.detect_rhythm_avg()
    # as of writing, the above methods and below attribute avg_data have not been created

    return jsonify(averaging_period=averaging_period,
                   time_interval=hr.avg_data['time'].tolist(),
                   average_heart_rate=hr.avg_data['HeartRate'].tolist(),
                   tachycardia_annotations=hr.avg_data['tachycardia_annotations'].tolist(),
                   bradycardia_annotations=hr.avg_data['bradycardia_annotations'].tolist())


@app.errorhandler(400)
def not_found(error):
    """.. function:: not_found(error)

    Bad Format Error

    :param: error: Error Message
    """
    return str(error), 400


@app.errorhandler(500)
def not_found(error):
    """.. function:: not_found(error)

    Unknown Error

    :param: error: Error Message
    """
    return "Unknown error", 500
