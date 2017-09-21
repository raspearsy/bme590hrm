def summarizeECG(data):
    """Create txt file summarizing ECG analysis

    :param data: dict{instHR, avgHR, brady, tachy}
    """
    #Calls hrdetector() to get instantaneous heart rate
    #instHR = findInstHR()

    #Calls findAvgHR() to get average heart rate
    #avgHR = findAvgHR()
    #Calls bradyTimes() to get times when bradycardia occurred
    #brady = bradyTimes()
    #Calls tachtimes() to get times when tachycardia occurred
    #tachy = tachyTimes()
    
    #Writes the output of the ECG analysis to an output file named ecgOutput.txt
    with open('ecgOutput.txt','w') as ecgResults:
        instHRstr = "Estimated instantaneous heart rate: {}".format(data['instHR'])
        avgHRstr = "Estimated average heart rate: {}".format(data['avgHR'])
        if data['brady'] is None:
            bradystr = "Bradycardia never occurred."
        else:
            bradystr = "Bradycardia occurred at: {}".format(data['brady'])
        tachystr = "Tachycardia occurred at: {}".format(data['tachy'])

        ecgResults.write(instHRstr + ' BPM\n' + avgHRstr + ' BPM\n' + bradystr + ' sec\n' + tachystr + ' sec')
