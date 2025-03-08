#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/1/7 17:02
Desc: 东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
https://data.eastmoney.com/xg/xg/sbqy.html
"""
import pandas as pd
import requests

from akshare.utils import demjson
from akshare.utils.tqdm import get_tqdm


def stock_ipo_declare() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
    https://data.eastmoney.com/xg/xg/sbqy.html
    :return: 首发申报企业信息
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "END_DATE,SECURITY_CODE",
		"sortTypes":"-1,-1",
        "pageSize": "50",
        "pageNumber": "1",
        "reportName": "RPT_IPO_DECORGNEWEST",
        "columns": "DECLARE_ORG,STATE,REG_ADDRESS,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,IS_SUBMIT,PREDICT_LISTING_MARKET,END_DATE,INFO_CODE,SECURITY_CODE,ORG_CODE,IS_REGISTER,STATE_CODE,DERIVE_SECURITY_CODE,ORG_CODE_OLD",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page_num + 1), leave=False):
        params.update(
            {
                "pageNumber": page,
            }
        )
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.rename(
        columns={
            "index": "序号",
            "ACCOUNT_FIRM": "会计师事务所",
            "DECLARE_ORG": "申报企业",
            "DERIVE_SECURITY_CODE": "-",
            "END_DATE": "更新日期",
            "INFO_CODE": "-",
            "IS_REGISTER": "-",
            "IS_SUBMIT": "-",
            "LAW_FIRM": "律师事务所",
            "ORG_CODE": "-",
            "ORG_CODE_OLD": "-",
            "PREDICT_LISTING_MARKET": "拟上市地",
            "RECOMMEND_ORG": "保荐机构",
            "REG_ADDRESS": "注册地",
            "SECURITY_CODE": "-",
            "STATE": "最新状态",
            "STATE_CODE": "-",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "序号",
            "申报企业",
            "最新状态",
            "注册地",
            "保荐机构",
            "律师事务所",
            "会计师事务所",
            "拟上市地",
            "更新日期",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_ipo_declare_df = stock_ipo_declare()
    print(stock_ipo_declare_df)
