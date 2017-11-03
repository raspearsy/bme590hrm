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

    def __init__(self, file_bool=False, argument="ecg_data.csv", threshold=0.9, thr_brady=50, thr_tachy=140,
                 rawdata=None):
        """.. function:: __init__(self, threshold=0.9, thr_brady=50, thr_tachy=140)
        :param argument: specifies the input file name
        :param threshold: specifies a heart beat
        :param thr_brady: indicates whether Bradycardia is detected
        :param thr_tachy: indicates whether Tachycardia is detected
        """

        self.__threshold = threshold
        self.__thr_brady = thr_brady
        self.__thr_tachy = thr_tachy
        self.data = None
        self.avg_data = None
        self.averaging_period = None
        self.avg_hr = None
        self.file_bool = file_bool
        if self.file_bool:
            inputfile = ECGInput(file=argument)
            self.file = inputfile.file
            self.__hr_rawdata = inputfile.ecg_dataframe
        else:
            self.__hr_rawdata = rawdata

    def thresholdhr(self):
        """ .. function:: thresholdhr(self)
        Will return a list of thresholds, as well as the number of chunks and data_chunk size
        :param: self: instance of the ECGMeasure class
        """

        # self.__hr_rawdata['voltage'] = list(range(0, 100, 10))
        # self.__hr_rawdata['time'] = list(range(0, 50, 5))
        time_step = self.__hr_rawdata['time'][2] - self.__hr_rawdata['time'][1]
        data_chunk = int(math.floor((5 / time_step)))
        number_chunks = int(math.floor((len(self.__hr_rawdata['time']) / data_chunk)))
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

        if self.file_bool:
            columns = ['HeartRate', 'B/T', 'time']
            hr = pd.DataFrame(numpy.empty(((len(thresholds)), 3)), columns=columns)
            hr['B/T'] = 'Healthy... for now'
        else:
            columns = ['HeartRate', 'bradycardia_annotations', 'tachycardia_annotations', 'time']
            hr = pd.DataFrame(numpy.empty(((len(thresholds)), 4)), columns=columns)
            hr['bradycardia_annotations'] = False
            hr['tachycardia_annotations'] = False

        hr['HeartRate'] = None
        hr['time'] = list(range(0, number_chunks * 5, 5))
        hb_count = [0] * len(thresholds)

        for j in range(0, len(thresholds)):
            for i in range(1, data_chunk):
                if (self.__hr_rawdata['voltage'][i + (j * data_chunk)] > thresholds['Threshold'][j]) and \
                        (self.__hr_rawdata['voltage'][(i + (j * data_chunk) - 1)] < thresholds['Threshold'][j]):
                    hb_count[j] = hb_count[j] + 1
            hr.at[j, 'HeartRate'] = (hb_count[j] / 5) * 60
        # print(hr)
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
        if self.file_bool:
            for x in range(0, len(self.data)):
                if self.data['HeartRate'][x] < self.__thr_brady:
                    bradycount += 1
                    self.data.at[x, 'B/T'] = 'Bradycardia Detected'
                elif self.data['HeartRate'][x] > self.__thr_tachy:
                    tachycount += 1
                    self.data.at[x, 'B/T'] = 'Tachycardia Detected'
                else:
                    self.data.at[x, 'B/T'] = 'Healthy... for now'
        else:
            for x in range(0, len(self.data)):
                if self.data['HeartRate'][x] < self.__thr_brady:
                    bradycount += 1
                    self.data.at[x, 'bradycardia_annotations'] = True
                elif self.data['HeartRate'][x] > self.__thr_tachy:
                    tachycount += 1
                    self.data.at[x, 'tachycardia_annotations'] = True

    def acquire_avgper(self, averaging_period=5):
        """.. function:: acquire_avgper(self, averaging_period)
        Adds averaging_period attribute to self
        :param self: instance of ECGMeasure class
        :param averaging_period: period in seconds for averaging inst hr data
        """
        self.averaging_period = averaging_period

    def hrdetector_avg(self):
        """.. function:: hrdetector_average(self)
        Creates dataframe to contain average data and finds the average for each averaging period
        :param self: instance of ECGMeasure class
        """

        self.hrdetector()
        columns = ['HeartRate', 'time', 'bradycardia_annotations', 'tachycardia_annotations']
        num_avg_bins = int(math.floor(self.data['time'].iat[-1] / self.averaging_period))
        time_intervals = list(range(1, num_avg_bins + 1))

        avg_data = pd.DataFrame(numpy.empty(((len(time_intervals)), 4)), columns=columns)
        avg_data['time'] = time_intervals
        avg_data['HeartRate'] = None
        avg_data['bradycardia_annotations'] = False
        avg_data['tachycardia_annotations'] = False

        for i in range(0, num_avg_bins):
            start_ind = int(numpy.floor(i * self.averaging_period / 5))
            stop_ind = int(numpy.floor((i * self.averaging_period + self.averaging_period) / 5) - 1)
            avg_data.at[i, 'HeartRate'] = self.data['HeartRate'][start_ind:stop_ind].mean()

        self.avg_data = avg_data

    def detect_rhythm_avg(self):
        """.. function:: detect_rhythm_avg(self)
        Detects bradycardia & tachycardia from average data based on threshold input and writes instances to avgdata
        DataFrame
        :param self: instance of ECGMeasure class
        """

        for x in range(0, len(self.avg_data)):
            if self.avg_data['HeartRate'][x] < self.__thr_brady:
                self.avg_data.at[x, 'bradycardia_annotations'] = True
            elif self.avg_data['HeartRate'][x] > self.__thr_tachy:
                self.avg_data.at[x, 'tachycardia_annotations'] = True


def main(arguments):
    for argument in arguments:
        hr_measure = ECGMeasure(argument)
        hr_measure.change_threshold(0.9)
        hr_measure.change_tachy_threshold(120)
        hr_measure.hrdetector()
        hr_measure.detect_rhythm()
        # hr_output = ECGOutput(hr_measure.data, hr_measure.file)
        # hr_output.write_ecg()


if __name__ == "__main__":
    main(sys.argv[1:])
