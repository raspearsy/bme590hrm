# bme590hrm

Integration: https://travis-ci.org/raspearsy/bme590hrm.svg?branch=master

Group Members:
Ryan Spears
Garren Angacian
Nisarg Shah
Josh Khani

Collaborators:
Mark Palmeri
Suyash Kumar
Arjun Desai

Guidelines:
(1) frequent commits (with issue references)
(2) work on separate branches to then merge in
(3) Use github milestones, issues, & labels
(4) write unit tests prior to associated code
(5) associate a software license with project
(6) write a README.md that describes how to run the program
(7) use PyCharm
(8) use if __name__ == "__main__" conditionals for main file
(9) use py.test formatting for unit tests
(10) functions are accessible from a module
(11) no hard-coded vlaues within functions...use default values
(12) follow PEP8
(13) use try/except exception handling
(14) gracefully terminate when input file ends

Goals:
(1) read in .csv file named ecg_data.csv containing ECG data (header, time [s], voltage [mV]
(2) estimate instantaneous HR
(3) estimate average HR over user-specified timespan (in min)
(4) indicate when bradycradia occured
(5) indicate when tachycardia occured
(6) output (2-5) as a .txt file
(7) create an annotated tag titled v1.0rc1 when assignment completed and ready for grading

Desciription:
Run HR_Measure.py which uses the read_file.py module to read a CSV file and convert it into a DataFrame. This DataFrame is then used in the hrdetector, bradydector, and tachydector functions in HR_Measure.py. 

The hrdetector function uses threshold detection to specify a heart beat and estimate both instantaneous heart rate and heart rate over a user-specified number of minutes. 

The bradydetector function then takes the heart rate data and indicates whether bradycardia is present based on an input threshold value. This is displayed with an additional column titled B/T representing the disease that is present or if the patient is healthy. The tachydetector function then takes this new DataFrame and also indicates whether tachycardia is present based on an input threshold value. This is also displayed in the B/T column. 

Finally, the output.py module is called to convert this last DataFrame into a text file that gives a summary of the ECG analysis.