from ecgmeasure import ECGMeasure
import pandas as pd
# need test dataframe test_hr1 that has 3 columns and 3 rows, where each successive row will
# be tagged as no arrythmia, bradycardia, and tachycardia


def get_test_hr1():
    """.. function:: get_test_hr1()

    Create test dataframe.
    """
    initial_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    test_hr1 = pd.DataFrame({'B/T': initial_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]})
    return test_hr1


def test_detect_rhythm_brady():
    """.. function:: test_detect_rhythm_brady()

    Test output of bradydetector when threshold is set to 50.
    """
    bm_b = ECGMeasure()
    hr_b = get_test_hr1()
    bm_b.detect_rhythm(hr_b)

    output_messages = ['Bradycardia Detected', 'Healthy... for now', 'Healthy... for now']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 60]}

    assert (hr_b == output_hr)


def test_detect_rhythm_brady2():
    """.. function:: test_detect_rhythm_brady2()

    Test bradydetector when threshold is set to 100.
    """
    bm_b3 = ECGMeasure()
    hr_b3 = get_test_hr1()
    bm_b3.change_brady_threshold(brady_threshold=100)
    bm_b3.detect_rhythm(hr_b3)

    output_messages = ['Bradycardia Detected', 'Bradycardia Detected', 'Bradycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 60]}

    assert (hr_b3 == output_hr)


def test_detect_rhythm_brady3():
    """.. function:: test_detect_rhythm_brady3()

    Test bradydetector when threshold is set to 100.
    """
    bm_b2 = ECGMeasure()
    hr_b2 = get_test_hr1()
    bm_b2.change_brady_threshold(brady_threshold=0)
    bm_b2.detect_rhythm(hr_b2)

    output_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 60]}

    assert (hr_b2 == output_hr)


def test_detect_rhythm_tachy():
    """.. function:: test_tachy()

    Test output of tachydetector when threshold is set to 140.
    """
    bm_t = ECGMeasure()
    hr_t = get_test_hr1()
    bm_t.detect_rhythm(hr_t)

    output_messages = ['Healthy... for now', 'Healthy... for now', 'Tachycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [60, 60, 200]}

    assert (hr_t == output_hr)


def test_detect_rhythm_tachy2():
    """.. function:: test_detect_rhythm_tachy2()

    Test tachydetector when threshold is set to 1000.
    """
    bm_t2 = ECGMeasure()
    hr_t2 = get_test_hr1()
    bm_t2.change_tachy_threshold(tachy_threshold=1000)
    bm_t2.detect_rhythm(hr_t2)

    output_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 60]}

    assert (hr_t2 == output_hr)


def test_detect_rhythm_tachy3():
    """.. function:: test_detect_rhythm_tachy3()

    Test tachydetector when threshold is set to 0.
    """
    bm_t3 = ECGMeasure()
    hr_t3 = get_test_hr1()
    bm_t3.change_tachy_threshold(tachy_threshold=0)
    bm_t3.detect_rhythm(hr_t3)

    output_messages = ['Tachycardia Detected', 'Tachycardia Detected', 'Tachycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 60]}

    assert (hr_t3 == output_hr)


def test_bradytachy():
    """.. function:: test_bradytachy()

    Test output of tachy/bradydetector when brady threshold is set to 50 and tachy to 100.
    """
    bm_bt = ECGMeasure()
    hr_bt = get_test_hr1()
    bm_bt.detect_rhythm(hr_bt)

    output_messages = ['Bradycardia Detected', 'Healthy... for now', 'Tachycardia Detected']
    output_hr = {'B/T': output_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}

    assert (hr_bt == output_hr)
