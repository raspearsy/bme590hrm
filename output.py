import pandas as pd
import numpy as np


def summarizeECG(data):
    """Create txt file summarizing ECG analysis

    :param data: pandas dataframe {'Heartrate', 'B\T', 'time'}
    :return ecgResults.txt
    """

    # Finds the last time point in the data file
    maxTime = data['time'].iat[-1]

    # Tells user the purpose of this program
    printStr = ("This program will summarize the ECG data.\n\
Data recorded from 0s to {}s.\n\
Enter a start and stop time in that range to get an instantaneous \n\
heart rate at those times, an average rate over that period, \n\
and any bradycardia or tachycardia events between those times.\n\n".format(maxTime))
    print(printStr)

    # Error messages for possible errors
    errmsg_max = ('\nThe time you selected is longer than the recorded data!\n\
Please choose between 0s and {}s\n\n'.format(maxTime))
    errmsg_notint = ('\nNot an integer! Please choose a time between 0s and {}s\n\n'.format(maxTime))
    
    # Get user specified period for averaging heartrate
    startTimestr = 'Start time (in seconds): '
    
    # Check for valid input
    while True:
        try:
            startTime = int(input(startTimestr))
        except ValueError:
            print(errmsg_notint)
        else:
            if startTime > maxTime:
                print(errmsg_max)
            else:
                startTime = int(startTime)
                break

    # Get user specified stop time
    stopTimestr = 'Stop time (in seconds): '

    # Check for valid input
    while True:
        try:
            stopTime = int(input(stopTimestr))
        except ValueError:
            print(errmsg_notint)
        else:
            break

    # If user gives time later than maxTime just set stopTime to maxTime
    if stopTime > maxTime:
        stopTime = maxTime

    # Tell user what is happening
    printStr = "ECG data will be summarized from {}s to {}s".format(startTime, stopTime)
    print(printStr)
    
    # Convert user input into indices - data is broken down in the dataframe file in chunks of 5seconds
    startInd = int(np.floor(startTime/5))
    stopInd = int(np.floor(stopTime/5))

    # Writes the output of the ECG analysis to an output file named ecgOutput.txt
    with open('ecgOutput.txt', 'w') as ecgResults:
        instHRStartstr = "Estimated instantaneous heart rate at {}s: {}BPM"\
            .format(startTime, data['HeartRate'][startInd])
        instHRStopstr = "Estimated instaneous heart rate at {}s: {}BPM".format(stopTime, data['HeartRate'][stopInd])
        avgHR = data['HeartRate'][startInd:stopInd].mean()
        avgHRstr = "Estimated average heart rate from {}s to {}s: {}BPM".format(startTime, stopTime, avgHR)
        
        bradyTimes = []
        tachyTimes = []
        for j in range(startInd, stopInd):
            if data['B/T'][j] == 'Bradycardia Detected':
                bradyTimes.append(data['time'][j])
            elif data['B/T'][j] == 'Tachycardia Detected':
                tachyTimes.append(data['time'][j])

        if not bradyTimes:
            bradystr = "Bradycardia never occurred."
        else:
            bradystr = "Bradycardia occurred at the following times (seconds): {}".format(bradyTimes)
        if not tachyTimes:
            tachystr = "Tachycardia never occurred."
        else:
            tachystr = "Tachycardia occurred at the following times (seconds): {}".format(tachyTimes)

        ecgResults.write(instHRStartstr + '\n' + instHRStopstr + '\n' + avgHRstr + '\n' + bradystr + '\n' + tachystr)
        

if __name__ == '__main__':
    summarizeECG(hr_data3)    
