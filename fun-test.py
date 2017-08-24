# -*- coding:utf-8 -*-

import os

import pandas as pd
import tushare as ts

import sys

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    fileName = 'stock-list.csv'
    if os.path.exists(fileName):
        df_stocks = pd.read_csv(fileName)
    else:
        df_stocks = ts.get_stock_basics()
        df_stocks.to_csv(fileName)

    fileName = 'industry.csv'
    if os.path.exists(fileName):
        df_industry = pd.read_csv(fileName)
    else:
        df_industry = ts.get_industry_classified()
        df_industry.to_csv(fileName)

    # save industry to csv
    # fileName = 's_industry_list.csv'
    # new_industry = df_stocks.drop_duplicates(['industry'])
    # s_small_industry = new_industry['industry']
    # s_small_industry.to_csv(fileName)
    # fileName = 'b_industry_list.csv'
    # new_industry = df_industry.drop_duplicates(['c_name'])
    # s_b_industry = new_industry['c_name']
    # s_b_industry.to_csv(fileName)

    fileName = 'today-price.csv'
    if os.path.exists(fileName):
        df_today = pd.read_csv(fileName)
    else:
        df_today = ts.get_today_all()
        df_today.to_csv(fileName)

    # fundamental
    year = 2017
    quarter = 2
    fileName = 'report-' + str(year) + '-' + str(quarter) + '.csv'
    if os.path.exists(fileName):
        df_reports = pd.read_csv(fileName)
    else:
        df_reports = ts.get_report_data(year, quarter)
        df_reports.to_csv(fileName)

    fileName = 'profits-' + str(year) + '-' + str(quarter) + '.csv'
    if os.path.exists(fileName):
        df_profits = pd.read_csv(fileName)
    else:
        df_profits = ts.get_profit_data(year, quarter)
        df_profits.to_csv(fileName)

    fileName = 'operation-' + str(year) + '-' + str(quarter) + '.csv'

    fileName = 'growth-' + str(year) + '-' + str(quarter) + '.csv'

    fileName = 'debt-paying-' + str(year) + '-' + str(quarter) + '.csv'

    fileName = 'cash-flow-' + str(year) + '-' + str(quarter) + '.csv'