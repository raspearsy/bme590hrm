from hr_measure import tachydetector
from hr_measure import bradydetector

# need test dataframe test_hr1 that has 3 columns and 3 rows, where each successive row will
# be tagged as no arrythmia, bradycardia, and tachycardia

initial_messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
test_hr1 = {'B/T': initial_messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}

# need to identify Garren's bradycardia threshold
def test_brady(test_hr1):
    messages = ['Bradycardia Detected', 'Healthy... for now', 'Healthy... for now']
    hr_b = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert bradydetector(test_hr1, 30) == hr_b


#need to identify Garren's tachycardia threshold
def test_tachy(test_hr1):
    messages = ['Healthy... for now', 'Healthy... for now', 'Tachycardia Detected']
    hr_t = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert tachydetector(test_hr1, 100) == hr_t


def test_bradytachy(hr_b):
    messages = ['Bradycardia Detected', 'Healthy... for now', 'Tachycardia Detected']
    hr_bt = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert tachydetector(hr_b, 100) == hr_bt


hr_b2 = bradydetector(test_hr1, 0)
def test_brady2(test_hr1):
    messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    hr_b2 = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert bradydetector(test_hr1, 0) == hr_b2


hr_t2 = tachydetector(test_hr1, 1000)
def test_tachy2(test_hr1):
    messages = ['Healthy... for now', 'Healthy... for now', 'Healthy... for now']
    hr_t2 = {'B/T': messages, 'time': [0, 5, 10], 'HeartRate': [20, 60, 200]}
    assert tachydetector(test_hr1, 1000) == hr_t2
