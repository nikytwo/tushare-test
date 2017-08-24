# -*- coding:utf-8 -*-

import os

import pandas as pd
import tushare as ts

import sys


def load_stocks():
    file_name = 'stock-list.csv'
    if os.path.exists(file_name):
        df_stocks = pd.read_csv(file_name)
    else:
        df_stocks = ts.get_stock_basics()
        df_stocks.to_csv(file_name)
    return df_stocks


def load_industry():
    file_name = 'industry.csv'
    if os.path.exists(file_name):
        df_industry = pd.read_csv(file_name)
    else:
        df_industry = ts.get_industry_classified()
        df_industry.to_csv(file_name)
    return df_industry


def load_today_price():
    file_name = 'today-price.csv'
    if os.path.exists(file_name):
        df_today = pd.read_csv(file_name)
    else:
        df_today = ts.get_today_all()
        df_today.to_csv(file_name)
    return df_today


# fundamental
def load_report(year, quarter):
    file_name = 'report-' + str(year) + '-' + str(quarter) + '.csv'
    if os.path.exists(file_name):
        df_reports = pd.read_csv(file_name)
    else:
        df_reports = ts.get_report_data(year, quarter)
        df_reports.to_csv(file_name)
    return df_reports


def load_profits(year, quarter):
    file_name = 'profits-' + str(year) + '-' + str(quarter) + '.csv'
    if os.path.exists(file_name):
        df_profits = pd.read_csv(file_name)
    else:
        df_profits = ts.get_profit_data(year, quarter)
        df_profits.to_csv(file_name)
    return df_profits


def load_operation(year, quarter):
    file_name = 'operation-' + str(year) + '-' + str(quarter) + '.csv'


def load_growth(year, quarter):
    file_name = 'growth-' + str(year) + '-' + str(quarter) + '.csv'


def load_debt_paying(year, quarter):
    file_name = 'debt-paying-' + str(year) + '-' + str(quarter) + '.csv'


def load_cash_flow(year, quarter):
    file_name = 'cash-flow-' + str(year) + '-' + str(quarter) + '.csv'


def save_industry():
    """
        save industry to csv
    """
    file_name = 's_industry_list.csv'
    new_industry = df_stocks.drop_duplicates(['industry'])
    s_small_industry = new_industry['industry']
    s_small_industry.to_csv(file_name)
    file_name = 'b_industry_list.csv'
    new_industry = df_industry.drop_duplicates(['c_name'])
    s_b_industry = new_industry['c_name']
    s_b_industry.to_csv(file_name)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    code = '601326'
    year = 2017
    quarter = 2
    df_stocks = load_stocks()
    df_industry = load_industry()
    df_today = load_today_price()
    df_reports = load_report(year, quarter)
    df_profits = load_profits(year, quarter)

    tmp_df = df_stocks[df_stocks['code'].isin([code])]
    industry = tmp_df['industry']

    tmp_df = df_stocks[df_stocks['industry'].isin(industry.tolist())]
    print tmp_df['code'].tolist()