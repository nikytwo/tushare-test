# -*- coding:utf-8 -*-
import datetime
import os
import time
import ConfigParser

import sys
import tushare as ts


# 加载配置
config = ConfigParser.ConfigParser()
config.read("realTimeQuotes.conf")
try:
    codes = config.get("global", "codes")
except:
    codes = '000001'
try:
    show_only_codes = config.get("global", "show_codes")
except:
    show_only_codes = 'sh'
try:
    col_names = config.get("global", "col_names")
except:
    col_names = 'code,price,high,low,bid,ask,time'
show_only_codes = show_only_codes.split(',')
codes = codes.split(',')
col_names = col_names.split(',')


def save_real_time(df, last_df=None):
    df2 = df.copy()
    if last_df is not None:
        # 去重
        idx = df[df['volume'].isin(last_df['volume'])].index
        df.drop(idx, inplace=True)

    for index, row in df.iterrows():
        if row['time'] > '15:10:00':
            continue
        if row['time'] < '09:25:00':
            continue
        volume = row['volume']
        if volume == 0:
            continue
        code = row['code']
        d = row['date']
        path = 'realtime_quotes/%s' % (code)
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = '%s/%s_quote_%s.csv' % (path, code, d)
        tmp = df.copy()
        tmp.drop(tmp.index, inplace=True)
        tmp = tmp.append(row, ignore_index=True)
        if os.path.exists(file_name):
            tmp.to_csv(file_name, header=False, mode='a+')
        else:
            tmp.to_csv(file_name, mode='a+')

    return df2

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    df2 = None
    while True:
        df = ts.get_realtime_quotes(show_only_codes)
        print df.loc[:, col_names]

        cur_hour = datetime.datetime.now().hour
        if cur_hour < 9:
            print 'stock not start'
            time.sleep(3)
            continue
        if cur_hour > 14:
            print 'stock end'
            time.sleep(3)
            continue
        df = ts.get_realtime_quotes(codes)
        print df[col_names]
        df2 = save_real_time(df, df2)
        time.sleep(3)