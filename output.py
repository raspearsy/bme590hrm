import pandas as pd
import numpy as np

def summarizeECG(data):
    """Create txt file summarizing ECG analysis

    :param data: dict{instHR, avgHR, brady, tachy}
    """

    #Get user specified period for averaging heartrate
    avgPeriod = input("How many minutes to average heartrate?")
    print("You selected to average over" + avgPeriod + " minutes")
    #Convert input into index number
    avgPeriod = (avgPeriod*60)/5
    #Create column of just the instantaneous heartrates
    instHR = data['HeartRate']
    #Average heartrate over period specified by user
    avgHR = instHR[0:avgPeriod].mean
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
