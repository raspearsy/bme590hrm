from HR_Measure.py import thresholdhr

# need to test what happens when have too little data to create a chunk
# need to throw an exception if have too little data

times = [x*0.1 for x in range(0, 10*50)]
voltages = []
for x in range(0, 10):
    for ii in range(0, 25+1):
        voltages.append(ii)
    for jj in range(24, 0, -1):
        voltages.append(jj)
raw_data = {'time': times, 'voltage': voltages}


def test_thresholdhr_unchanging(raw_data):
    thr = []
    for x in range(0, 10):
        thr.append(0.9*25)
    thresholds = {'Threshold': thr}
    chunk = 50
    num_chunks = 10
    assert thresholdhr(raw_data) == [thresholds, chunk, num_chunks]