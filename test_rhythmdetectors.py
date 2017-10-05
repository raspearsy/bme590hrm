from hr_measure import tachydetector
from hr_measure import bradydetector
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


# need to identify Garren's bradycardia threshold
def test_brady():
    """.. function:: test_brady()

    Test threshold for bradydetector() is 50.
    """
    test_hr1 = get_test_hr1()
    messages = ['Bradycardia Detected', 'Healthy... for now', 'Healthy... for now']
    hr_b = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert (bradydetector(test_hr1, 50)['B/T'] == hr_b['B/T']).all()


# need to identify Garren's tachycardia threshold
def test_tachy():
    """.. function:: test_tachy()

    Test threshold for tachydetector() is 140.
    """
    test_hr1 = get_test_hr1()
    messages = ['Healthy... for now', 'Healthy... for now', 'Tachycardia Detected']
    hr_t = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert (tachydetector(test_hr1, 140)['B/T'] == hr_t['B/T']).all()


def test_bradytachy():
    test_hr1 = get_test_hr1()
    messages = ['Bradycardia Detected', 'Healthy... for now', 'Tachycardia Detected']
    hr_bt = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    new_hr=bradydetector(test_hr1, 50)
    assert (tachydetector(new_hr, 100)['B/T'] == hr_bt['B/T']).all()


# hr_b2 = bradydetector(test_hr1, 0)
def test_brady2():
    test_hr1 = get_test_hr1()
    messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    hr_b2 = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert (bradydetector(test_hr1, 0)['B/T'] == hr_b2['B/T']).all()


# hr_t2 = tachydetector(test_hr1, 1000)
def test_tachy2():
    test_hr1 = get_test_hr1()
    messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    hr_t2 = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert (tachydetector(test_hr1, 1000)['B/T'] == hr_t2['B/T']).all()
