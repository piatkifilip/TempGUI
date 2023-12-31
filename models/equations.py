# models/equations.py
current_equation_set = 1

default_coeffs = {
    'eq1': [0.7009, 0.3332, -0.0186, -0.0280, 14.6689, -15.6335],
    'eq2': [2.0012, -0.9161, 0.0240, -0.0410, 232.4343, -234.2310],
    'eq3': [0.2011, 0.8826, 0.0259, 0.0212, -13.2861, 11.1789],
    'eq4' : [-0.0047, 1.6232, 0.0161, -0.0276, 36.0287, -51.6625],
    'eq5' : [-29.1131, 31.6457, 0.1707, -0.1534, 1002.0546, -1044.1504],
    'eq6' : [1.4088, 0.8131, 0.0745, -0.0071, -15.7530, -15.7515]
}

terms = {
    'eq1': ['EQ1 \nT1', 'T2', 'mT1', 'mT2', 'Ratio-T1/T2', 'Intercept'],
    'eq2': ['EQ2 \nT1', 'T2', 'mT1', 'mT2', 'Ratio-T1/T2', 'Intercept'],
    'eq3': ['EQ3 \nT1', 'T2', 'mT1', 'mT2', 'Ratio-T1/T2', 'Intercept'],
    'eq4': ['EQ4 \nT1', 'T2', 'mT1', 'mT2', 'Ratio-T1/T2', 'Intercept'],
    'eq5': ['EQ5 \nT1', 'T2', 'mT1', 'mT2', 'Ratio-T1/T2', 'Intercept'],
    'eq6': ['EQ6 \nT1', 'T2', 'mT1', 'mT2', 'Ratio-T1/T2', 'Intercept'],
}
