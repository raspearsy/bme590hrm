def summarizeECG(instHR, avgHR, brady, tachy):
    """Create txt file summarizing ECG analysis

    :param instHR: (int)
    :param avgHR: (int)
    :param brady: (int)
    :param tachy: (int)
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
        instHRstr = "Estimated instantaneous heart rate: {}".format(instHR)
        avgHRstr = "Estimated average heart rate: {}".format(avgHR)
        bradystr = "Bradycardia occurred at: {}".format(brady)
        tachystr = "Tachycardia occurred at: {}".format(tachy)

        ecgResults.write(instHRstr + ' BPM\n' + avgHRstr + ' BPM\n' + bradystr + ' sec\n' + tachystr + ' sec')
