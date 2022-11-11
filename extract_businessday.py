# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 14:57:55 2022

@author: jasmi
"""

import datetime
import numpy as np

def month_str(month_int):
    month_str = str(month_int)
    if len(month_str) == 1:
        month_str = "0"+str(month_str)
    return month_str

year = 2023
month = 1
first_day = datetime.datetime(year,month,1)

    
start = str(year)+"-"+month_str(month)
end = str(year)+"-"+str(month_str(month+1))
print(np.busday_offset(start, 0, roll='forward'))
print(np.busday_offset(end, -1, roll='forward'))
 
from datetime import datetime
print('Weekday is:', first_day.isoweekday())


