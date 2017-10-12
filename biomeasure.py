import pandas as pd
import numpy
import math
from bioinput import Bioinput
import sys


class Biomeasure:
    """ This is the main calling class

    __init__ sets the __hr_rawdata

    """
    def __init__(self, threshold=0.9, thr_brady=50, thr_tachy=140):
        self.__threshold = threshold
        self.__thr_brady = thr_brady
        self.__thr_tachy = thr_tachy
        self.hr = self.hrdetector()
        inputfile = Bioinput()
        self.ecg_file = inputfile.file
        self.__hr_rawdata = inputfile.read_input()

    def thresholdhr(self):
        """ Will return a list of thresholds, as well as the number of chunks and data_chunk size

        :return: dataframe with column threshold_hr, and data chunk size and number of chunks for data
        """

        time_step = self.__hr_rawdata['time'][2] - self.__hr_rawdata['time'][1]
        data_chunk = int(math.floor((5 / time_step)))
        number_chunks = int(math.floor((len(self.__hr_rawdata) / data_chunk)))

        threshold_hr = [None] * number_chunks

        for j in range(0, number_chunks):
            maxhr_data = max(self.__hr_rawdata['voltage'][(j * data_chunk):(j * data_chunk) + data_chunk])
            threshold_hr[j] = self.__threshold * maxhr_data
        threshold_hr = pd.DataFrame(numpy.array(threshold_hr), columns=['Threshold'])
        print(threshold_hr)
        return [threshold_hr, data_chunk, number_chunks]

    def hrdetector(self):
        """Use threshold detection to specify a heart beat (QRS height) and estimate both instanteous and hr over delta_t

        :param
        """
        # delta_t = input('Enter how long you would like to average your heart rate over (in s): ')
        # Use delta_t, average the HR over that time
        # for i in hr_rawdata[1], find minimum and max locally, threshold on that (using a timing fxn)
        # Calls thresholdhr every so often
        [thresholds, data_chunk, number_chunks] = self.thresholdhr()
        # DataFrame, thresholds, data_chunk (# of points per 5 seconds), number_chunks
        columns = ['HeartRate', 'B/T', 'time']
        # index = [None] * len(thresholds)
        hr = pd.DataFrame(numpy.empty(((len(thresholds)), 3)), columns=columns)
        hr['HeartRate'] = None
        hr['B/T'] = 'Healthy... for now'
        hr['time'] = list(range(0, number_chunks * 5, 5))

        hb_count = [0] * len(thresholds)

        # time_step = hr_rawdata['time'][2]-hr_rawdata['time'][1]  # find time step
        for j in range(0, len(thresholds)):
            for i in range(1, data_chunk):
                if (self.__hr_rawdata['voltage'][i * (j + 1)] > thresholds['Threshold'][j]) and \
                        (self.__hr_rawdata['voltage'][(i * (j + 1)) - 1] < thresholds['Threshold'][j]):
                    hb_count[j] = hb_count[j] + 1
            hr.at[j, 'HeartRate'] = (hb_count[j] / 5) * 60
        return hr

    def change_threshold(self, threshold):
        self.__init__(threshold)

    def change_brady_thresohld(self, brady_threshold):
        self.__init__(thr_brady=brady_threshold)

    def change_tachy_threshold(self, tachy_threshold):
        self.__init__(thr_tachy=tachy_threshold)

    def rhythmdetector(self):
        """Detects bradycardia & tachycardia based on threshold input and writes instances to hr DataFrame
        """

        bradycount = 0
        tachycount = 0

        for x in range(0, len(self.hr)):
            if self.hr['HeartRate'][x] < self.__thr_brady:
                bradycount += 1
                self.hr.at[x, 'B/T'] = 'Bradycardia Detected'
            elif self.hr['HeartRate'][x] > self.__thr_tachy:
                tachycount += 1
                self.hr.at[x, 'B/T'] = 'Tachycardia Detected'
            else:
                self.hr.at[x, 'B.T'] = 'Healthy... for now'


def main(threshold):
    hr_measure = Biomeasure(threshold)
    # hr_rawdata_new = Bioinput().read_input()
    hr_measure.change_threshold(0.5)
    hr_measure.hrdetector()


if __name__ == "__main__":
    main(sys.argv)
