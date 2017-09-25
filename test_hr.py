from hr_measure import thresholdhr
from hr_measure import hrdetector

# need to test what happens when have too little data to create a chunk
# need to throw an exception if have too little data


def get_raw_data():
    times = [x*0.1 for x in range(0, 10*50)]
    voltages = []
    for x in range(0, 10):
        for ii in range(0, 25+1):
            voltages.append(ii)
        for jj in range(24, 0, -1):
            voltages.append(jj)
    raw_data = {'time': times, 'voltage': voltages}
    return raw_data


def test_thresholdhr_unchanging():
    raw_data = get_raw_data()
    thr = []
    for x in range(0, 10):
        thr.append(0.9*25)
    thresholds = {'Threshold': thr}
    chunk = 50
    num_chunks = 10
    assert thresholdhr(raw_data) == [thresholds, chunk, num_chunks]


def get_test_hr1():
    initial_messages = []
    hrs = []
    for ii in range(0, 10):
        hrs.append(1/5*60)
        initial_messages.append('Healthy... for now')
    test_hr1 = {'B/T': initial_messages, 'time': list(range(0, 51, 5)), 'HeartRate': hrs}
    return test_hr1


def test_hrdetector():
    raw_data = get_raw_data()
    test_hr1 = get_test_hr1()
    assert hrdetector(raw_data) == test_hr1
