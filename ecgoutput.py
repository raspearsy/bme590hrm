import pandas as pd
import numpy as np


class ECGOutput:
    """Output Class
    Outputs a text file containing the final heart rate data over a specified period of time
    """

    def __init__(self, hr_data, file):
        """.. function:: __init__(self, hr_data, file_name)

        :param hr_data: final hr_data from ECGMeasure that needs to be written to a text file
        :param file: name of the input file so a corresponding output file name can be derived
        """
        self.data = hr_data
        self.file = file

    def write_ecg(self):
        """.. function:: write_ecg(self)

        Create txt file summarizing ECG analysis

        :param self: instance of ECGOutput class
        """

        # Finds the last time point in the data file
        max_time = self.data['time'].iat[-1]

        # Tells user the purpose of this program
        print_str = """This program will summarize the ECG data.
        Data recorded from 0s to {}s.
        Enter a start and stop time in that range to get an instantaneous 
        heart rate at those times, an average rate over that period, 
        and any bradycardia or tachycardia events between those times.""".format(max_time)
        print(print_str)

        # Error messages for possible errors
        err_msg_max = ('\nThe time you selected is longer than the recorded data!\n\
        Please choose between 0s and {}s\n\n'.format(max_time))
        err_msg_not_int = ('\nNot an integer! Please choose a time between 0s and {}s\n\n'.format(max_time))

        # Get user specified period for averaging heartrate
        start_time_str = 'Start time (in seconds): '

        # Check for valid input
        while True:
            try:
                start_time = int(input(start_time_str))
            except ValueError:
                print(err_msg_not_int)
            else:
                if start_time > max_time:
                    print(err_msg_max)
                    continue
                start_time = int(start_time)
                break

        # Get user specified stop time
        stop_time_str = 'Stop time (in seconds): '

        # Check for valid input
        while True:
            try:
                stop_time = int(input(stop_time_str))
            except ValueError:
                print(err_msg_not_int)
                continue
            else:
                break

        # If user gives time later than maxTime just set stopTime to maxTime
        if stop_time > max_time:
            stop_time = max_time

        # Tell user what is happening
        print_str = "ECG data will be summarized from {}s to {}s'".format(start_time, stop_time)
        print(print_str)

        # Convert user input into indices - data is broken down in the dataframe file in chunks of 5 seconds
        start_ind = int(np.floor(start_time / 5))
        stop_ind = int(np.floor(stop_time / 5))

        # Writes the output of the ECG analysis to an output file named ecgOutput.txt
        with open("{}_{}_{}.txt".format(self.file[:-4], start_time, stop_time), 'w') as ecg_results:
            inst_hr_start_str = "Estimated instantaneous heart rate at {}s: {} BPM" \
                .format(start_time, self.data['HeartRate'][start_ind])
            inst_hr_stop_str = "Estimated instantaneous heart rate at {}s: {} BPM"\
                .format(stop_time, self.data['HeartRate'][stop_ind])
            avg_hr = self.data['HeartRate'][start_ind:stop_ind].mean()
            avg_hr_str = "Estimated average heart rate from {}s to {}s: {} BPM".format(start_time, stop_time, avg_hr)

            brady_times = []
            tachy_times = []
            for j in range(start_ind, stop_ind):
                if self.data['B/T'][j] == 'Bradycardia Detected':
                    brady_times.append(self.data['time'][j])
                elif self.data['B/T'][j] == 'Tachycardia Detected':
                    tachy_times.append(self.data['time'][j])

            if not brady_times:
                brady_str = "Bradycardia never occurred."
            else:
                brady_str = "Bradycardia occurred at the following times (seconds): {}".format(brady_times)
            if not tachy_times:
                tachy_str = "Tachycardia never occurred."
            else:
                tachy_str = "Tachycardia occurred at the following times (seconds): {}".format(tachy_times)

            ecg_results.write(inst_hr_start_str + '\n'
                              + inst_hr_stop_str + '\n' + avg_hr_str + '\n' + brady_str + '\n' + tachy_str)
