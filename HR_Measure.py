# import random
# import sys
# import os

import math
import numpy
import pandas as pd
from read_file import input_dataframe
# Maybe hr (passed in vector) should be three columns so that I can always pass it in, and just fill as needed

def thresholdhr(hr_rawdata):
    """Will create a threshold array (in mV) on which to return the heart rate
    :param hr_rawdata: raw data input (time first column, voltage second column)
    :return: will return a dataframe of numbers for thresholding whether a heart beat has occured
    """

    # time, voltage
    threshold = 0.9  # %90 percent of max
    time_step = hr_rawdata['time'][2]-hr_rawdata['time'][1]
    data_chunk = int(math.floor(5/time_step))
    number_chunks = int(math.floor((len(hr_rawdata)/data_chunk)))

    # Gives a number of data points per to look at, will miss at worst 100 points
    threshold_hr = [None] * number_chunks

    for j in range(0, number_chunks):
        # minhr_data = min(hr_rawdata[timestamp:timestamp+time_interval])
        maxhr_data = max(hr_rawdata['voltage'][(j * data_chunk):(j * data_chunk) + data_chunk])
        # maxhr_data = max([row[0] for row in hr_rawdata[j*time_interval:(j*time_interval)+time_interval]])
        threshold_hr[j] = threshold * maxhr_data
    threshold_hr = pd.DataFrame(numpy.array(threshold_hr), columns=['Threshold'])
    return [threshold_hr, data_chunk, number_chunks]


def hrdetector(hr_rawdata):
    """Use threshold detection to specify a heart beat (QRS height) and estimate both instanteous and hr over delta_t
    :param hr_rawdata: raw data (after minor I/O filtering)
    """
    # delta_t = input('Enter how long you would like to average your heart rate over (in s): ')
    # Use delta_t, average the HR over that time
    # for i in hr_rawdata[1], find minimum and max locally, threshold on that (using a timing fxn)
    # Calls thresholdhr every so often
    [thresholds, data_chunk, number_chunks] = thresholdhr(hr_rawdata)
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
            if (hr_rawdata['voltage'][i*(j+1)] > thresholds['Threshold'][j]) and \
                    (hr_rawdata['voltage'][(i*(j+1))-1] < thresholds['Threshold'][j]):
                hb_count[j] = hb_count[j] + 1
        hr.at[j, 'HeartRate'] = (hb_count[j]/5)*60
    return hr


def bradydetector(hr, hr_threshold_brady):
    """Detects bradycardia based on threshold input
    :param hr:
    :param hr_threshold_brady:
    :returns: Number of instances of Bradycardia, time stamp for Bradycardia, return HR list with added colomns
    """

    # n = len(hr)
    bradycount = 0
    for x in range(0, len(hr)):
        # timestamp = x * delta_t
        if hr['HeartRate'][x] < hr_threshold_brady:
            bradycount += 1
            hr.at[x, 'B/T'] = 'Bradycardia Detected'
    return hr


def tachydetector(hr, hr_threshold_tachy):
    """detects tachycardia

    :param hr: list of Heart Rates
    :param hr_threshold_tachy: threshold HR for detection
    :return: Number of instances of Bradycardia, time stamp for Bradycardia, return HR list with added colomns
    """

    tachycount = 0
    for x in range(0, len(hr)):
        if hr['HeartRate'][x] > hr_threshold_tachy:
            tachycount += 1
            hr.at[x, 'B/T'] = 'Tachycardia Detected'
    return hr

if __name__ == '__main__':
    hr_rawdata_new = input_dataframe()
    # print(hr_rawdata_new)
    hr_data = hrdetector(hr_rawdata_new)
    hr_data2 = bradydetector(hr_data, 50)
    print(hr_data2)
    hr_data3 = tachydetector(hr_data2, 140)
    print(hr_data3)


