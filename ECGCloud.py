from flask import Flask, request, jsonify
from ecgmeasure import ECGMeasure

app = Flask(__name__)

# probably not the most elegant way of doing this, but should work
# more ideal to use something innate to the post to increment the counter
request_counter = 0


@app.route("/api/requests")
def requests():
    return jsonify(request_counter)


@app.route("/api/heart_rate/summary", methods=['POST'])
def summary():
    global request_counter
    request_counter = request_counter + 1

    time = request.json['time']
    voltages = request.json['voltage']
    hr_rawdata = {'time': time, 'voltages': voltages}

    hr = ECGMeasure(rawdata=hr_rawdata)
    hr.hrdetector()
    hr.detect_rhythm()

    return jsonify(hr.data['HeartRate'].tolist())
    """
    return jsonify(time=time,
                   instantaneous_heart_rate=hr.data['HeartRate'].tolist(),
                   tachycardia_annotations=hr.data['tachycardia_annotations'].tolist(),
                   bradycardia_annotations=hr.data['bradycardia_annotations'].tolist())
    """


@app.route("/api/heart_rate/average", methods=['POST'])
def average():
    global request_counter
    request_counter = request_counter + 1

    averaging_period = request.json['averaging_period']
    time = request.json['time']
    voltages = request.json['voltage']
    hr_rawdata = {'time': time, 'voltages': voltages}

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
