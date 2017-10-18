import pandas as pd
import numpy
import math
from ecginput import ECGInput
from ecgoutput import ECGOutput
import sys


class ECGMeasure:
    """ This is the main calling class
    __init__ sets the __hr_rawdata
    """

    def __init__(self, argument="ecg_data.csv", threshold=0.9, thr_brady=50, thr_tachy=140):
        """.. function:: __init__(self, threshold=0.9, thr_brady=50, thr_tachy=140)

        :param argument: specifies the input file name
        :param threshold: specifies a heart beat
        :param thr_brady: indicates whether Bradycardia is detected
        :param thr_tachy: indicates whether Tachycardia is detected
        """

        self.__threshold = threshold
        self.__thr_brady = thr_brady
        self.__thr_tachy = thr_tachy
        inputfile = ECGInput(file=argument)
        self.file = inputfile.file
        self.__hr_rawdata = inputfile.ecg_dataframe
        self.data = None

    def thresholdhr(self):
        """ .. function:: thresholdhr(self)

        Will return a list of thresholds, as well as the number of chunks and data_chunk size

        :param: self: instance of the ECGMeasure class
        """

        # self.__hr_rawdata['voltage'] = list(range(0, 100, 10))
        # self.__hr_rawdata['time'] = list(range(0, 50, 5))
        time_step = self.__hr_rawdata['time'][2] - self.__hr_rawdata['time'][1]
        data_chunk = int(math.floor((5 / time_step)))
        number_chunks = int(math.floor((len(self.__hr_rawdata) / data_chunk)))

        threshold_hr = [None] * number_chunks

        for j in range(0, number_chunks):
            maxhr_data = max(self.__hr_rawdata['voltage'][(j * data_chunk):(j * data_chunk) + data_chunk])
            threshold_hr[j] = self.__threshold * maxhr_data
        threshold_hr = pd.DataFrame(numpy.array(threshold_hr), columns=['Threshold'])
        self.data = [threshold_hr, data_chunk, number_chunks]

    def hrdetector(self):
        """.. function:: hrdetector(self)

        Use threshold detection to specify a heart beat (QRS height) and estimate both instantaneous and hr over delta_t

        :param self: instance of ECGMeasure class
        """
        # delta_t = input('Enter how long you would like to average your heart rate over (in s): ')
        # Use delta_t, average the HR over that time
        # for i in hr_rawdata[1], find minimum and max locally, threshold on that (using a timing fxn)
        # Calls thresholdhr every so often
        self.thresholdhr()
        [thresholds, data_chunk, number_chunks] = self.data
        columns = ['HeartRate', 'B/T', 'time']
        hr = pd.DataFrame(numpy.empty(((len(thresholds)), 3)), columns=columns)
        hr['HeartRate'] = None
        hr['B/T'] = 'Healthy... for now'
        hr['time'] = list(range(0, number_chunks * 5, 5))
        hb_count = [0] * len(thresholds)

        for j in range(0, len(thresholds)):
            for i in range(1, data_chunk):
                if (self.__hr_rawdata['voltage'][i + (j * data_chunk)] > thresholds['Threshold'][j]) and \
                        (self.__hr_rawdata['voltage'][(i + (j * data_chunk) - 1)] < thresholds['Threshold'][j]):
                    hb_count[j] = hb_count[j] + 1
            hr.at[j, 'HeartRate'] = (hb_count[j] / 5) * 60
        print(hr)
        self.data = hr

    def change_threshold(self, threshold):
        """.. function:: change_threshold(self, threshold)

        Change the threshold that specifies a heart beat

        :param self: instance of ECGMeasure class
        :param threshold: new value that threshold will be changed to
        """
        self.__threshold = threshold
        # self.__init__(threshold)

    def change_brady_threshold(self, brady_threshold):
        """.. function:: change_brady_threshold(self, brady_threshold)

        Change the threshold that indicates whether Bradycardia is detected

        :param self: instance of ECGMeasure class
        :param brady_threshold: new value that the brady threshold will be changed to
        """
        self.__thr_brady = brady_threshold

    def change_tachy_threshold(self, tachy_threshold):
        """.. function:: change_tachy_threshold(self, tachy_threshold)

        Change the threshold that indicates whether Tachycardia is detected

        :param self: instance of ECGMeasure class
        :param tachy_threshold: new value that the tachy threshold will be changed to
        """
        self.__thr_tachy = tachy_threshold

    def detect_rhythm(self):
        """.. function:: detect_rhythm(self, hr)

        Detects bradycardia & tachycardia based on threshold input and writes instances to hr DataFrame

        :param self: instance of ECGMeasure class
        """

        bradycount = 0
        tachycount = 0
        for x in range(0, len(self.data)):
            if self.data['HeartRate'][x] < self.__thr_brady:
                bradycount += 1
                self.data.at[x, 'B/T'] = 'Bradycardia Detected'
            elif self.data['HeartRate'][x] > self.__thr_tachy:
                tachycount += 1
                self.data.at[x, 'B/T'] = 'Tachycardia Detected'
            else:
                self.data.at[x, 'B/T'] = 'Healthy... for now'


def main(arguments):
    for argument in arguments:
        hr_measure = ECGMeasure(argument)
        hr_measure.change_threshold(0.9)
        hr_measure.change_tachy_threshold(120)
        hr_measure.hrdetector()
        hr_measure.detect_rhythm()
        hr_output = ECGOutput(hr_measure.data, hr_measure.file)
        hr_output.write_ecg()


if __name__ == "__main__":
    main(sys.argv[1:])
