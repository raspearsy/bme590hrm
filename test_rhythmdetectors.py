import pandas as pd
import tachydetector.py

# need test dataframe test_hr1 that has 3 columns and 3 rows, where each successive row will
# be tagged as no arrythmia, bradycardia, and tachycardia

hr_b = bradydetector(test_hr1, 30)
# need to identify Garren's bradycardia threshold
def test_brady_b():
    assert hr.B/T[0] == 'Bradycardia Detected'

def test_tachy_b():
    assert hr.B/T[2] == 'Healthy... for now'

def test_noarrythmia_b():
    assert hr.B/T[1] == 'Healthy... for now'


hr_t = tachydetector(test_hr1, 100)
#need to identify Garren's tachycardia threshold
def test_tachy_t():
    assert hr.B/T[2]=='Tachycardia Detected'

def test_brady_t():
    assert hr.B/T[0]=='Healthy... for now'

def test_noarrythmia_t():
    assert hr.B/T[1]=='Healthy... for now'


hr_bt = tachydetector(hr_b, 100)
def test_brady_bt():
    assert hr.B/T[0] == 'Bradycardia Detected'

def test_tachy_bt():
    assert hr.B/T[2] == 'Tachycardia Detected'

def test_noarrythmia_bt():
    assert hr.B/T[1] == 'Healthy... for now'



hr_b2 = bradydetector(test_hr1, 0)
def test_brady_b2():
    assert hr.B/T[0] == 'Healthy... for now'

hr_t2 = tachydetector(test_hr1, 1000)
def test_tachy_t2():
    assert hr.B/T[2] == 'Healthy... for now'