import pandas as pd
import numpy as np

def summarizeECG(data):
    """Create txt file summarizing ECG analysis

    :param data: pandas dataframe {'Heartrate', 'B\T', 'time'}
    """

    maxTime = data['time'].iget(-1)

    printStr = ("This program will summarize the ECG data.\n
    Data recorded from 0s to {}s. \n
    Enter a start and stop time in that range to get an instantaneous \n
    heart rate at those times, an average rate over that period, \n
    and any bradycardia or tachycardia events between those times.".format(maxTime))

    #Get user specified period for averaging heartrate
    startTimestr = 'Start time (in seconds): '
    startTime = input(startTimestr)
    
    #Error messages for possible errors
    errmsg_max =('The time you selected is longer than the recorded data!\n
        Please choose between 0s and {}s'.format(maxTime))
    errmsg_notint = ('Not an integer! Please choose a time between 0s and {}s'.format(maxTime))
    
    #Check for errors
    if startTime > maxTime:
        print(errmsg_max)
        startTime = input(startTimestr)
    elif ~startTime.isnumeric():
        print(errmsg_notint)
        startTime = input(startTimestr)

    #Get user specified stop time
    stopTimestr = 'Stop time (in seconds): '
    stopTime = input(stopTimestr)
    if stopTime > maxTime:
    #If user inputs stop time that's passed max time just set to max time
        stopTime = maxTime
    elif ~stopTime.isnumer():
        print(errmsg_notint)
        stopTime = input(stopTimestr) 

    printStr = "ECG data will be summarized from {}s to {}s'".format(startTime,stopTime)
    print(printStr)

    startInd = floor(startTime/5)
    stopInd = floor(stopTime/5)

    
    
    #Writes the output of the ECG analysis to an output file named ecgOutput.txt
    with open('ecgOutput.txt','w') as ecgResults:
        instHRStartstr = "Estimated instantaneous heart rate at {}s: {}BPM".format(startTime,data[startInd,'HeartRate'])
        instHRStopstr = "Estimated instaneous heart rate at {}s: {}BPM".format(stopTime,data[stopInd,'HeartRate'])
        avgHR = data[startInd:stopInd,'HeartRate'].mean()
        avgHRstr = "Estimated average heart rate from {}s to {}s: {}BPM".format(startTime,stopTime,avgHR)

        for j in range(startInd,stopInd):
            bradyTimes = []
            tachyTimes = []
            if data[j,'B/T']=='Bradycardia Detected':
                bradyTimes.append(data[j,'time'])
            elif data[j,'B/T']=='Tachycardia Detected':
                tachyTimes.append(data[j,'time'])

        if bradyTimes is None:
            bradystr = "Bradycardia never occurred."
        else:
            bradystr = "Bradycardia occurred at the following times (seconds): {}".format(bradyTimes)
        if tachyTimes is None:
            tachystr = "Tachycardia never occurred."
        else:
            tachystr = "Tachycardia occurred at the following times (seconds): {}".format(tachyTimes)

        ecgResults.write(instHRStartstr + '\n' + instHRStopstr + '\n' avgHRstr + '\n' + bradystr + '\n' + tachystr)

if __name__ == '__main__':
    summarizeECG(data)
    
