# -*- coding:utf-8 -*-

import os

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import time

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
        try:
            df_reports = ts.get_report_data(year, quarter)
            df_reports.to_csv(file_name)
        except Exception as ex:
            print ex
            df_reports = load_report(year - 1, quarter)
            df_reports.drop(df_reports.index, inplace=True)
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
        try:
            df_profits = ts.get_profit_data(year, quarter)
            df_profits.to_csv(file_name)
        except Exception as ex:
            print ex
            df_profits = load_profits(year - 1, quarter)
            df_profits.drop(df_profits.index, inplace=True)
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


def load_concept():
    file_name = 'concept_classified.csv'
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        df = ts.get_concept_classified()
        df.to_csv(file_name)
    return df


def load_k_data(code='000001', year='2017'):
    i_year = int(year)
    file_name = 'k_data/%sd_qfq%d.csv' % (code, i_year)
    if os.path.exists(file_name):
        k = pd.read_csv(file_name)
    else:
        s = '%d-01-01' % i_year
        e = '%d-12-31' % i_year
        k = ts.get_k_data(code, start=s, end=e, pause=5)
        k.to_csv(file_name)
    return k


def load_tick_data(code, date):
    file_name = 'tick_data/%s/%s_tick_data_%s.csv' % (code, code, date)
    path = os.path.split(file_name)[0]
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        df = ts.get_tick_data(code, date, pause=5)
        df.to_csv(file_name)

    return df



def load_pe(code='000001', years=None):
    """
    指定code的全年的 pe 数据
    """
    if years is None:
        years = [2016, 2017]

    avgs = []
    for year in years:
        avg = _load_pe(code, year)
        avgs.append(avg)
    avg = pd.concat(avgs, axis=1)
    avg.columns = years

    return avg


def _load_pe(code, year):
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
        p = report[report['code'].isin([code])].loc[:, ['eps', 'net_profits']]
        eps = p.iloc[0, 0]
    print eps

    k = load_k_data(code, str(year))
    return k.loc[:, ['high', 'low']].mean(1).apply(lambda x: x / eps)


def load_profits_analysis(code='000001', years=None):
    if years is None:
        years = [2016, 2017]
    df = pd.DataFrame()
    for year in years:
        p_obj = {}
        for quarter in range(1, 5):
            report = load_profits(year, quarter)
            p = report[report['code'].isin([code])].loc[:, ['net_profits', 'business_income']]
            if len(p.index) == 0:
                p_obj.setdefault(str(quarter), 0)
            else:
                p_obj.setdefault(str(quarter), p.iloc[0, 0])
        tmp = pd.DataFrame(data=p_obj, index=['%dp' % year])
        df = df.append(tmp)

    for year in years:
        bi_obj = {}
        for quarter in range(1, 5):
            report = load_profits(year, quarter)
            p = report[report['code'].isin([code])].loc[:, ['net_profits', 'business_income']]
            if len(p.index) == 0:
                bi_obj.setdefault(str(quarter), 0)
            else:
                bi_obj.setdefault(str(quarter), p.iloc[0, 1] / 5)
        tmp = pd.DataFrame(data=bi_obj, index=['%dbi' % year])
        df = df.append(tmp)

    print df
    return df


def load_volume(code, date):
    source = load_tick_data(code, date)
    df = source.loc[:, ['type', 'volume']]
    df = df.replace({'卖盘': -1, '中性盘': 0, '买盘': 1})
    df = df.groupby(['type']).sum()
    df['date'] = date
    return df


def show_plot(code, ):
    stocks = load_stocks()
    name = stocks[stocks['code'].isin([code])].loc[:, ['name']].iloc[0, 0]
    print code, name
    fig, axes = plt.subplots(2, 2)

    years = [2016, 2017]
    avg = load_pe(code, years)
    avg.plot(ax=axes[0, 0])
    title = '%s pe' % code
    axes[0, 0].set_title(title)

    yoy = load_profits_analysis(code, years)
    yoy.T.plot.bar(ax=axes[1, 0])
    title = '%s profits' % code
    axes[1, 0].set_title(title)

    # k = load_k_data(code)
    # volume_b = pd.DataFrame()
    # volume_s = pd.DataFrame()
    # for index, row in k.iterrows():
    #     date = row['date']
    #     tmp = load_volume(code, date)
    #     volume_b = volume_b.append(tmp.loc[[1], :])
    #     volume_s = volume_s.append(tmp.loc[[-1], :])
    # volume_b = volume_b.set_index(['date'])
    # volume_b.columns = ['B']
    # volume_s = volume_s.set_index(['date'])
    # volume_s.columns = ['S']
    # volume = volume_b.sub(volume_s['S'], axis='index')
    # k = load_k_data(code)
    # k = k.set_index(['date']).loc[:, ['low']].apply(lambda x: x * 50000)
    # b_p = pd.concat([volume, k], axis=1)
    # print b_p
    # b_p.plot(ax=axes[0, 1])

    plt.show()


def show_date_p(code, date='2017-12-01'):
    source = load_tick_data(code, date)
    times = source['time'].apply(lambda x: '%s:00' % x[:5])
    dfs = [source, times]
    source = pd.concat(dfs, axis=1)
    source.columns = ['0', 'time', 'price', 'change', 'volume', 'amount', 'type', 'T']
    print source
    fig, axes = plt.subplots(2, 2)

    # show price
    title = '%s price' % code
    axes[0, 0].set_title(title)
    source = source.set_index(['time']).sort_index()
    df = source.loc[:, ['price']]
    df.plot(ax=axes[0, 0])

    # title = '%s day' % code
    # axes[0, 1].set_title(title)
    # df = source.loc[:, ['type', 'volume']]
    # df = df.replace({'卖盘': -1, '中性盘': 0, '买盘': 1})
    # df = df.groupby(['type']).sum()
    # df.plot.bar(ax=axes[0, 1])

    # show volume
    # title = '%s price' % code
    # axes[1, 0].set_title(title)
    # df = source.replace({'卖盘': -1, '中性盘': 0, '买盘': 1})
    # df = df['volume'] * df['type']
    # df.plot(ax=axes[1, 0])

    # show volume
    title = '%s B' % code
    axes[1, 0].set_title(title)
    df = source.loc[:, ['T', 'type', 'volume']]
    df = df.replace({'卖盘': -1, '中性盘': 0, '买盘': 1})
    b = df[df.type == 1].loc[:, ['T', 'volume']]
    b = b.groupby(['T']).sum()
    z = df[df.type == 0].loc[:, ['T', 'volume']]
    z = z.groupby(['T']).sum()
    s = df[df.type == -1].loc[:, ['T', 'volume']]
    s = s.groupby(['T']).sum()
    df = pd.concat([s, b], axis=1)
    df.columns = ['S', 'B']
    df = df.sub(df['S'], axis='index').loc[:, ['B']]
    print df
    df.plot.bar(ax=axes[1, 0])

    # show volume
    # title = '%s B' % code
    # axes[1, 1].set_title(title)
    # df = source.loc[:, ['T', 'type', 'volume']]
    # df = df.replace({'卖盘': -1, '中性盘': 0, '买盘': 1})
    # df = df[df.type == -1]
    # df = df.groupby(['T', 'type']).sum()
    # print df
    # df.plot.bar(ax=axes[1, 1])

    plt.show()


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

    codes = [
        # '600507',  # 方大
        '601222',  # 林洋
        # '601012',  # 隆基
        '600309',  # 万化
        '600409',  # 三友
        # '600703',  # 三安
        '002636',  # 金安
        # '002171',  # 楚江
        '600549',  # 夏门
        '002460',  # 赣锋
        # '600522',  # 中天
        # '002185',  # 华天
        # '002745',  # 木林森
        # '600703',  # 三安
        # '002019',  # 亿帆
        '000338',  # 潍柴
        '603369',  # 今世缘
        # '002749',  # 国光
        # '002136',  # 安 纳 达
        # '002195'   # 2345
        # '002466'  # 天齐
    ]
    code = '000338'
    # show_plot(code)

    # for code in codes:
    #     show_plot(code)

    # 历史分笔
    today = datetime.datetime.now()
    date = today.strftime("%Y-%m-%d")
    date = '2017-12-04'
    # for code in codes:
    #     show_date_p(code, date)

    # 实时
    df = ts.get_realtime_quotes('sh')
    quotes = ts.get_realtime_quotes(codes)
    df = df.append(quotes)
    print df.loc[:, ['code', 'price', 'high', 'low']]
    # print df.loc[:, ['code', 'price', 'high', 'low', 'volume', 'amount']]

    # 筛选

    # df = load_concept()
    # param = df[df['code'].isin(['002136'])].iloc([0,1])
    # print param
