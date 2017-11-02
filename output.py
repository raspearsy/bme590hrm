import numpy as np


def summarizeECG(data):
    """.. function:: summarizeECG(data)

    Create txt file summarizing ECG analysis

    :param data: pandas dataframe {'Heartrate', 'B\T', 'time'}
    :rtype: txt file
    :return: ecg_results.txt
    """

    # Finds the last time point in the data file
    max_time = data['time'].iat[-1]

    # Tells user the purpose of this program
    print_str = """This program will summarize the ECG data.
Data recorded from 0s to {}s.
Enter a start and stop time in that range to get an instantaneous 
heart rate at those times, an average rate over that period,
and any bradycardia or tachycardia events between those times.
"""
    print(print_str.format(max_time))

    # Error messages for possible errors
    errmsg_max = """\nThe time you selected is longer than the recorded data!
Please choose between 0s and {}s\n\n"""
    errmsg_notint = '\nNot an integer! Please choose a time between 0s and {}s\n\n'

    # Get user specified period for averaging heartrate
    start_time_str = 'Start time (in seconds): '

    # Check for valid input
    while True:
        try:
            start_time = int(input(start_time_str))
        except ValueError:
            print(errmsg_notint.format(max_time))
        else:
            if start_time > max_time:
                print(errmsg_max.format(max_time))
            else:
                start_time = int(start_time)
                break

    # Get user specified stop time
    stop_time_str = 'Stop time (in seconds): '

    # Check for valid input
    while True:
        try:
            stop_time = int(input(stop_time_str))
        except ValueError:
            print(errmsg_notint)
        else:
            break

    # If user gives time later than max_time just set stop_time to max_time
    if stop_time > max_time:
        stop_time = max_time

    # Tell user what is happening
    print_str = "ECG data will be summarized from {}s to {}s".format(
        start_time, stop_time)
    print(print_str)

    # Convert user input into indices - data is broken down
    # in the dataframe file in chunks of 5seconds
    start_ind = int(np.floor(start_time / 5))
    stop_ind = int(np.floor(stop_time / 5))

    # Writes the output of the ECG analysis
    # to an output file named ecgOutput.txt
    filename = "ecgData"
    filename_str = "{}_{}to{}.txt".format(filename, start_time, stop_time)

    with open(filename_str, 'w') as ecg_results:

        brady_times = []
        tachy_times = []
        for j in range(start_ind, stop_ind):
            if data['B/T'][j] == 'Bradycardia Detected':
                brady_times.append(data['time'][j])
            elif data['B/T'][j] == 'Tachycardia Detected':
                tachy_times.append(data['time'][j])

        if not brady_times:
            brady_str = "Bradycardia never occurred."
        else:
            brady_str = "Bradycardia occurred at the following times (seconds): {}".format(
                brady_times)
        if not tachy_times:
            tachy_str = "Tachycardia never occurred."
        else:
            tachy_str = "Tachycardia occurred at the following times (seconds): {}".format(
                tachy_times)

        hr_template = """Estimated instantaneous heart rate at {start_time}s: {start_hr} BPM
Estimated instantaneous heart rate at {stop_time}s: {stop_hr} BPM
Estimated average heart rate from {start_time}s to {stop_time}s: {avg_hr} BPM
"""
        hr_context = {
            "start_time": start_time,
            "stop_time": stop_time,
            "start_hr": data['HeartRate'][start_ind],
            "stop_hr": data['HeartRate'][stop_ind],
            "avg_hr":  data['HeartRate'][start_ind:stop_ind].mean()
        }

        write_str = '\n'.join([hr_template.format(**hr_context),
                               brady_str,
                               tachy_str])

        ecg_results.write(write_str)


if __name__ == '__main__':
    summarizeECG(hr_data3)