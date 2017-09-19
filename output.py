#Calls findInstHR() to get instantaneous heart rate
instHR = findInstHR()

#Calls findAvgHR() to get average heart rate
avgHR = findAvgHR()
#Calls bradyTimes() to get times when bradycardia occurred
brady = bradyTimes()
#Calls tachtimes() to get times when tachycardia occurred
tachy = tachyTimes()
#Writes the output of the ECG analysis to an output file named ecgOutput.txt
ecgResults = open('ecgOutput.txt','w')
instHRstr = "Estimated instantaneous heart rate: %s" % str(instHR)
avgHRstr = "Estimated average heart rate: %s" % str(avgHR)
bradystr = "Bradycardia occurred at: %s" % str(brady)
tachystr = "Tachycardia occurred at: %s" % str(tachy)

ecgResults.write(instHRstr + '\n' + avgHRstr + '\n' + bradystr + '\n' + tachystr)
ecgResults.close()
