# models/equations.py

default_coeffs = {
    'eq1': [0.7009, 0.3332, -0.0186, -0.0280, 14.6689, -15.6335],
    'eq2': [2.0012, -0.9161, 0.0240, -0.0410, 232.4343, -234.2310],
    'eq3': [0.2011, 0.8826, 0.0259, 0.0212, -13.2861, 11.1789]
}

terms = {
    'eq1': ['HeadTemp1', 'HeadTemp2', 'Slope_HeadTemp1', 'Slope_HeadTemp2', 'Ratio_HeadTemp1_HeadTemp2', 'Intercept'],
    'eq2': ['HeadTemp1', 'HeadTemp2', 'Slope_HeadTemp1', 'Slope_HeadTemp2', 'Ratio_HeadTemp1_HeadTemp2', 'Intercept'],
    'eq3': ['HeadTemp1', 'HeadTemp2', 'Slope_HeadTemp1', 'Slope_HeadTemp2', 'Ratio_HeadTemp1_HeadTemp2', 'Intercept']
}
