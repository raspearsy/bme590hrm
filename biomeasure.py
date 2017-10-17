import pandas as pd
import numpy
import math
from bioinput import Bioinput
import sys


class BioMeasure:
    """ This is the main calling class

    __init__ sets the __hr_rawdata

    """
    def __init__(self, threshold=0.8, thr_brady=50, thr_tachy=140):
        self.__threshold = threshold
        self.__thr_brady = thr_brady
        self.__thr_tachy = thr_tachy
        inputfile = Bioinput()
        self.__hr_rawdata = inputfile.ecg_dataframe
        self.__data = self.thresholdhr()

    def thresholdhr(self):
        """ Will return a list of thresholds, as well as the number of chunks and data_chunk size

        :return: dataframe with column threshold_hr, and data chunk size and number of chunks for data
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
        return [threshold_hr, data_chunk, number_chunks]

    def hrdetector(self):
        """Use threshold detection to specify a heart beat (QRS height) and estimate both instantaneous and hr over delta_t

        :param
        """
        # delta_t = input('Enter how long you would like to average your heart rate over (in s): ')
        # Use delta_t, average the HR over that time
        # for i in hr_rawdata[1], find minimum and max locally, threshold on that (using a timing fxn)
        # Calls thresholdhr every so often
        [thresholds, data_chunk, number_chunks] = self.__data
        columns = ['HeartRate', 'B/T', 'time']
        hr = pd.DataFrame(numpy.empty(((len(thresholds)), 3)), columns=columns)
        hr['HeartRate'] = None
        hr['B/T'] = 'Healthy... for now'
        hr['time'] = list(range(0, number_chunks * 5, 5))
        hb_count = [0] * len(thresholds)

        for j in range(0, len(thresholds)):
            for i in range(1, data_chunk):
                if (self.__hr_rawdata['voltage'][i * (j + 1)] > thresholds['Threshold'][j]) and \
                        (self.__hr_rawdata['voltage'][(i * (j + 1)) - 1] < thresholds['Threshold'][j]):
                    hb_count[j] = hb_count[j] + 1
            hr.at[j, 'HeartRate'] = (hb_count[j] / 5) * 60
        return hr

    def change_threshold(self, threshold):
        self.__threshold = threshold
        # self.__init__(threshold)

    def change_brady_threshold(self, brady_threshold):
        self.__thr_brady = brady_threshold

    def change_tachy_threshold(self, tachy_threshold):
        self.__thr_tachy = tachy_threshold


    def detect_rhythm(self, hr):
        """Detects bradycardia & tachycardia based on threshold input and writes instances to hr DataFrame
        """

        bradycount = 0
        tachycount = 0
        for x in range(0, len(hr)):
            if hr['HeartRate'][x] < self.__thr_brady:
                bradycount += 1
                hr.at[x, 'B/T'] = 'Bradycardia Detected'
            elif hr['HeartRate'][x] > self.__thr_tachy:
                tachycount += 1
                hr.at[x, 'B/T'] = 'Tachycardia Detected'
            else:
                hr.at[x, 'B/T'] = 'Healthy... for now'
        print(hr)


def main(argv):
    hr_measure = BioMeasure()
    hr_measure.change_threshold(0.9)
    hr_measure.change_tachy_threshold(120)
    hr = hr_measure.hrdetector()
    hr_measure.detect_rhythm(hr)

if __name__ == "__main__":
    main(sys.argv[1:])

