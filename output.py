import pandas as pd
import numpy as np

def summarizeECG(data):
    """Create txt file summarizing ECG analysis

    :param data: dict{instHR, avgHR, brady, tachy}
    """

    print('This program will summarize the ECG data.\n
    Enter a start and stop time to get an instantaneous \n
    heart rate at those time, an average rate over that period, \n
    and any bradycardia or tachycardia events between those times.')

    #Get user specified period for averaging heartrate
    startTime = input('Start time (in min): ')
    startTime = (startTime*60)/5
    stopTime = input('Stop time (in min): ')
    stopTime = (stopTime*60)/5

    printStr = "ECG data will be summarized from {}s to {}s'".format(startTime,stopTime)
    print(printStr)
    
    #Writes the output of the ECG analysis to an output file named ecgOutput.txt
    with open('ecgOutput.txt','w') as ecgResults:
        instHRstr = "Estimated instantaneous heart rate: {}".format(data['HeartRate'])
        avgHRstr = "Estimated average heart rate after {}: {}".format(avgPeriod,avgHR)
        if data['brady'] is None:
            bradystr = "Bradycardia never occurred."
        else:
            bradystr = "Bradycardia occurred at: {}".format(data['brady'])
        tachystr = "Tachycardia occurred at: {}".format(data['tachy'])

        ecgResults.write(instHRstr + ' BPM\n' + avgHRstr + ' BPM\n' + bradystr + ' sec\n' + tachystr + ' sec')
