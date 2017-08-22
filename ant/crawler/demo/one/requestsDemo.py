# -*- coding: utf-8 -*-
import tushare as ts

if __name__=='__main__':
    while True:
        df = ts.get_sina_dd('002350', date='2017-08-11')

        print(df)