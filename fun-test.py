# -*- coding:utf-8 -*-

import os

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts

import sys


def load_stocks():
    """
    加载所有股票列表。
    若列表文件‘stock-list.csv’不存在，则下载
    
    :return:   
    :rtype: DataFrame
    """
    file_name = 'stock-list.csv'
    if os.path.exists(file_name):
        df_stocks = pd.read_csv(file_name)
    else:
        df_stocks = ts.get_stock_basics()
        df_stocks.to_csv(file_name)
    return df_stocks


def load_industry():
    """
    加载所有股票所属行业列表。
    若列表文件‘industry.csv’不存在，则下载
    
    :return:   
    :rtype: DataFrame
    """
    file_name = 'industry.csv'
    if os.path.exists(file_name):
        df_industry = pd.read_csv(file_name)
    else:
        df_industry = ts.get_industry_classified()
        df_industry.to_csv(file_name)
    return df_industry


def load_today_price():
    """
    加载所有股票当天的价格列表。
    若列表文件‘today-price201709.csv’不存在，则下载
    
    :return:   
    :rtype: DataFrame
    """
    file_name = 'today-price.csv'
    # 休息5秒
    if os.path.exists(file_name):
        df_today = pd.read_csv(file_name)
    else:
        df_today = ts.get_today_all()
        df_today.to_csv(file_name)
    return df_today


# fundamental
def load_report(year, quarter):
    """
    加载所有股票指定年份和季度的财务报告列表。
    若列表文件‘report-(year)-(quarter).csv’不存在，则下载
    
    :param year: 年份
    :param quarter: 季度(1,2,3,4)    
    :return:   
    :rtype: DataFrame
    """
    file_name = 'report-' + str(year) + '-' + str(quarter) + '.csv'
    if os.path.exists(file_name):
        df_reports = pd.read_csv(file_name)
    else:
        df_reports = ts.get_report_data(year, quarter)
        df_reports.to_csv(file_name)
    return df_reports


def load_profits(year, quarter):
    """
    加载所有股票指定年份和季度的盈利能力列表。
    若列表文件‘profits-(year)-(quarter).csv’不存在，则下载
    
    :param year: 年份
    :param quarter: 季度(1,2,3,4)    
    :return:   
        code,代码
        name,名称
        roe,净资产收益率(%)
        net_profit_ratio,净利率(%)
        gross_profit_rate,毛利率(%)
        net_profits,净利润(万元)
        eps,每股收益
        business_income,营业收入(百万元)
        bips,每股主营业务收入(元)
    :rtype: DataFrame
    """
    file_name = 'profits-' + str(year) + '-' + str(quarter) + '.csv'
    if os.path.exists(file_name):
        df_profits = pd.read_csv(file_name)
    else:
        df_profits = ts.get_profit_data(year, quarter)
        df_profits.to_csv(file_name)
    return df_profits


def load_operation(year, quarter):
    """
    未实现
    
    :param year: 年份
    :param quarter: 季度(1,2,3,4)    
    :return: 
    """
    file_name = 'operation-' + str(year) + '-' + str(quarter) + '.csv'


def load_growth(year, quarter):
    """
    未实现
    
    :param year: 年份
    :param quarter: 季度(1,2,3,4)    
    :return: 
    """
    file_name = 'growth-' + str(year) + '-' + str(quarter) + '.csv'


def load_debt_paying(year, quarter):
    """
    未实现
    
    :param year: 年份
    :param quarter: 季度(1,2,3,4)    
    :return: 
    """
    file_name = 'debt-paying-' + str(year) + '-' + str(quarter) + '.csv'


def load_cash_flow(year, quarter):
    """
    未实现
    
    :param year: 年份
    :param quarter: 季度(1,2,3,4)    
    :return: 
    """
    file_name = 'cash-flow-' + str(year) + '-' + str(quarter) + '.csv'


def save_industry(df_stocks, df_industry):
    """
        save industry to csv.
        s_industry_list.csv is 小类
        b_industry_list.csv is 大类
    """
    file_name = 's_industry_list.csv'
    new_industry = df_stocks.drop_duplicates(['industry'])
    s_small_industry = new_industry['industry']
    s_small_industry.to_csv(file_name)
    file_name = 'b_industry_list.csv'
    new_industry = df_industry.drop_duplicates(['c_name'])
    s_b_industry = new_industry['c_name']
    s_b_industry.to_csv(file_name)


def load_k_data(code='000001', year='2017'):
    file_name = code + 'd_qfq' + year + '.csv'
    if os.path.exists(file_name):
        k = pd.read_csv(file_name)
    else:
        s = year + '-01-01'
        e = year + '-12-31'
        k = ts.get_k_data(code, start=s, end=e, pause=5)
        k.to_csv(file_name)
    return k


def load_pe(code='000001', year=2016):
    """
    指定code的全年的 pe 数据
    """

    if datetime.datetime.now().year == year:
        stocks = load_stocks()
        s = stocks[stocks['code'].isin([code])].loc[:, ['pe', 'npr']]
        today = load_today_price()
        t = today[today['code'].isin([code])].loc[:, ['trade', 'mktcap']]
        trade = t.iloc[0, 0]
        pe = s.iloc[0, 0]
        eps = trade / pe
    else:
        report = load_report(year, 4)
        p = report[report['code'].isin([code])].loc[:, ['eps', 'net_profits', 'profits_yoy']]
        eps = p.iloc[0, 0]
    print eps

    k = load_k_data(code, str(year))
    return k.loc[:, ['high', 'low']].mean(1).apply(lambda x: x / eps)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #
    # code = '601326'
    # year = 2017
    # quarter = 3
    # df_stocks = load_stocks()
    # df_industry = load_industry()
    # save_industry(df_stocks, df_industry)
    # df_today = load_today_price()
    # df_reports = load_report(year, quarter)
    # df_profits = load_profits(year, quarter)
    #
    # tmp_df = df_stocks[df_stocks['code'].isin([code])]
    # industry = tmp_df['industry']
    # print industry
    #
    # tmp_df = df_stocks[df_stocks['industry'].isin(industry.tolist())]
    # print tmp_df['code'].tolist()

    codes = ['600507',
             '601222',
             '600522',
             '600549',
             '600703',
             '600309',
             '601012',
             '600409',
             '002636',
             '002185',
             '002171',
             '002460',
             '002466']

    code = '000001'
    years = ['2016', '2017']
    avgs = []
    for year in years:
        avg = load_pe(code, int(year))
        avgs.append(avg)

    avg = pd.concat(avgs, axis=1)
    avg.columns = years
    print avg
    stocks = load_stocks()
    name = stocks[stocks['code'].isin([code])].loc[:, ['name']].iloc[0, 0]
    print code, name

    fig, axes = plt.subplots(2, 2)
    avg.plot(ax=axes[0,0])
    axes[0, 0].set_title('pe')
    plt.show()


    # 实时
    # quotes = ts.get_realtime_quotes('sh')
    # print quotes.loc[:, ['price', 'high', 'low', 'volume', 'amount']]
