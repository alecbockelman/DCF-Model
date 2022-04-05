# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:24:01 2022

@author: ajb5429
"""

import yfinance as yf
import pandas as pd
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

ticker = 'COP'

mkt = '^GSPC' #GSPC is the S&P 500 Index in yahoo finance

#Assumptions
taxrate= .25
rf = 2
mkt_risk_prm = 5.5


def BetaL(ticker,mkt_ticker):
    eqdata = yf.download(ticker,period = "2Y" )
    eqdata = eqdata['Close']
    mdata = yf.download(mkt_ticker,period = "2Y")
    mdata = mdata['Close']
    offset = pd.offsets.BusinessDay(-1)
    eqdata_week_ret = eqdata.resample('W',loffset=offset).last().pct_change()
    mdata_week_ret = mdata.resample('W',loffset=offset).last().pct_change()
    frames = [eqdata_week_ret,mdata_week_ret]
    df_concat = pd.concat(frames, axis =1)
    covar = df_concat.cov().iloc[1][0]
    var = mdata_week_ret.var()
    BetaL = covar/var
    std_dev_eqdata = eqdata_week_ret.std()
    std_dev_mdata = mdata_week_ret.std()
    r_sqrd = (covar/(std_dev_eqdata * std_dev_mdata))**2
    return BetaL

def revenue(ticker):
    rev = yf.Ticker(ticker).financials.loc['Total Revenue'][0]
    return rev

def COGS(ticker):
    cogs = yf.Ticker(ticker).financials.loc['Cost Of Revenue'][0]
    return cogs

def GrossProfit(ticker):
    rev = yf.Ticker(ticker).financials.loc['Total Revenue'][0]
    cogs = yf.Ticker(ticker).financials.loc['Cost Of Revenue'][0]
    grossprofit = rev-cogs
    return grossprofit

def opex(ticker):
    opex=yf.Ticker(ticker).financials.loc['Other Operating Expenses'][0] + yf.Ticker(ticker).financials.loc['Selling General and Administration'][0]
    return opex

def EBITDA(ticker):
    rev = yf.Ticker(ticker).financials.loc['Total Revenue'][0]
    cogs = yf.Ticker(ticker).financials.loc['Cost Of Revenue'][0]
    grossprofit = rev-cogs
    opex=yf.Ticker(ticker).financials.loc['Other Operating Expenses'][0] + yf.Ticker(ticker).financials.loc['Selling General and Administration'][0]
    ebitda = grossprofit - opex
    return ebitda

print(EBITDA(ticker))
rev2 = yf.Ticker(ticker).financials.loc['Total Revenue']
cogs2 = yf.Ticker(ticker).financials.loc['Cost Of Revenue']

