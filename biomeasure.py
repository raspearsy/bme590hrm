import pandas as pd
import numpy

from bioinput import Bioinput

class Biomeasure:
    """

    """

    def __init__(self, threshold=0.9, thr_brady=50, thr_tachy=140):
        self.__hr_rawdata = pd.DataFrame(numpy.empty((10, 3))*numpy.nan, columns=['HeartRate', 'B/T', 'time'])
        self.__threshold = threshold
        self.__thr_brady = thr_brady
        self.__thr_tachy = thr_tachy
        self.hr = pd.DataFrame(numpy.empty((10, 3))*numpy.nan, columns=['HeartRate', 'B/T', 'time'])
        # need to create from others' work
        input = Bioinput()
        self.ecg_file = input.file

    def thresholdhr(self):
        print(self.__threshold)
        print(self.__hr_rawdata)
        print(self.ecg_file)

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

if __name__ == "__main__":
    hr_measure = Biomeasure()
    hr_measure.change_threshold(0.5)
    hr_measure.thresholdhr()
