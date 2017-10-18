from ecgmeasure import ECGMeasure
import pandas as pd
# need test dataframe test_hr1 that has 3 columns and 3 rows, where each successive row will
# be tagged as no arrythmia, bradycardia, and tachycardia


def get_test_hr1(a=60, b=60, c=60):
    """.. function:: get_test_hr1()

    Create test dataframe.
    """
    initial_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    test_hr1 = pd.DataFrame({'B/T': initial_messages, 'time': [0, 5, 10], 'HeartRate': [a, b, c]})
    return test_hr1


def test_detect_rhythm_brady():
    """.. function:: test_detect_rhythm_brady()

    Test output of bradydetector when threshold is set to 50.
    """
    bm_b = ECGMeasure()
    bm_b.data = get_test_hr1(a=20)
    bm_b.detect_rhythm()

    output_messages = ['Bradycardia Detected', 'Healthy... for now', 'Healthy... for now']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 60]}

    assert (bm_b.data['B/T'] == output_hr['B/T']).all()


def test_detect_rhythm_brady2():
    """.. function:: test_detect_rhythm_brady2()

    Test bradydetector when threshold is set to 100.
    """
    bm_b2 = ECGMeasure()
    bm_b2.data = get_test_hr1()
    bm_b2.change_brady_threshold(brady_threshold=100)
    bm_b2.detect_rhythm()

    output_messages = ['Bradycardia Detected', 'Bradycardia Detected', 'Bradycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [60, 60, 60]}

    assert (bm_b2.data['B/T'] == output_hr['B/T']).all()


def test_detect_rhythm_brady3():
    """.. function:: test_detect_rhythm_brady3()

    Test bradydetector when threshold is set to 0.
    """
    bm_b3 = ECGMeasure()
    bm_b3.data = get_test_hr1()
    bm_b3.change_brady_threshold(brady_threshold=0)
    bm_b3.detect_rhythm()

    output_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [60, 60, 60]}

    assert (bm_b3.data['B/T'] == output_hr['B/T']).all()


def test_detect_rhythm_tachy():
    """.. function:: test_detect_rhythm_tachy()

    Test output of tachydetector when threshold is set to 140.
    """
    bm_t = ECGMeasure()
    bm_t.data = get_test_hr1(c=200)
    bm_t.detect_rhythm()

    output_messages = ['Healthy... for now', 'Healthy... for now', 'Tachycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [60, 60, 200]}

    assert (bm_t.data['B/T'] == output_hr['B/T']).all()


def test_detect_rhythm_tachy2():
    """.. function:: test_detect_rhythm_tachy2()

    Test tachydetector when threshold is set to 1000.
    """
    bm_t2 = ECGMeasure()
    bm_t2.data = get_test_hr1()
    bm_t2.change_tachy_threshold(tachy_threshold=1000)
    bm_t2.detect_rhythm()

    output_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [60, 60, 60]}

    assert (bm_t2.data['B/T'] == output_hr['B/T']).all()


def test_detect_rhythm_tachy3():
    """.. function:: test_detect_rhythm_tachy3()

    Test tachydetector when threshold is set to 0.
    """
    bm_t3 = ECGMeasure()
    bm_t3.data = get_test_hr1()
    bm_t3.change_tachy_threshold(tachy_threshold=0)
    bm_t3.detect_rhythm()

    output_messages = ['Tachycardia Detected', 'Tachycardia Detected', 'Tachycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [60, 60, 60]}

    assert (bm_t3.data['B/T'] == output_hr['B/T']).all()


def test_detect_rhythm_bradytachy():
    """.. function:: test_detect_rhythm_bradytachy()

    Test output of tachy/bradydetector when brady threshold is set to 50 and tachy to 100.
    """
    bm_bt = ECGMeasure()
    bm_bt.data = get_test_hr1(a=20, c=200)
    bm_bt.detect_rhythm()

    output_messages = ['Bradycardia Detected', 'Healthy... for now', 'Tachycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}

    assert (bm_bt.data['B/T'] == output_hr['B/T']).all()
