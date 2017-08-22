__author__ = 'hh'

import  tushare as ts
from datetime import datetime
import time
if __name__=='__main__':
    print("----")

    start = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    print(ts.get_k_data(code='600755',ktype='D',end=start,start='2017-08-21'))
