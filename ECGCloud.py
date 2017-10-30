from flask import Flask, request, jsonify
from ecgmeasure import ECGMeasure

app = Flask(__name__)



@app.route("/api/heart_rate/summary", methods=['POST'])
def summary():
    time = request.json['time']
    voltages = request.json['voltage']
    hr_rawdata = {'time': time, 'voltages': voltages}

    hr = ECGMeasure(rawdata=hr_rawdata)
    hr.hrdetector()
    hr.detect_rhythm()

    return jsonify(time=time,
                   instantaneous_heart_rate=hr.data['HeartRate'],
                   tachycardia_annotations=hr.data['tachycardia_annotations'],
                   bradycardia_annotations=hr.data['bradycardia_annotations'])


@app.route("/api/heart_rate/average", methods=['POST'])
def average():
    @app.route("/api/heart_rate/summary", methods=['POST'])
    def summary():
        averaging_period = request.json['averaging_period']
        time = request.json['time']
        voltages = request.json['voltage']
        hr_rawdata = {'time': time, 'voltages': voltages}

        hr = ECGMeasure(rawdata=hr_rawdata)
        hr.acquire_avgper(averaging_period=averaging_period)
        hr.average()
        hr.detect_rhythm()
        # NEED TO DEFINE HOW DETECT RHYTHM -- TAKING FROM NEW df INSTEAD
        # OF from self.data -- for now calling self.avg_data
        # either add to detect_rhythm *OR* add additional method detect_rhythm_average

        return jsonify(averaging_period=averaging_period,
                       time_interval=hr.avg_data['time'],
                       average_heart_rate=hr.avg_data['HeartRate'],
                       tachycardia_annotations=hr.avg_data['tachycardia_annotations'],
                       bradycardia_annotations=hr.avg_data['bradycardia_annotations'])
