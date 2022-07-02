import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from datetime import date, datetime
from dateutil.relativedelta import relativedelta as rd
import time
import requests
import numpy as np
import pandas as pd


from dotenv import load_dotenv
load_dotenv()


def get_bitcoin_data(date_from=None, date_to=None):
  date_from = date(1000,1,1) if date_from == None else date_from
  date_to = date(3000,1,1) if date_to == None else date_to

  df = pd.read_csv('data/btc-1d.csv')[['time', 'close']]
  df['time'] =  pd.to_datetime(df['time'], infer_datetime_format=True)
  df = df[(df['time'] >= pd.to_datetime(date_from)) & (df['time'] <= pd.to_datetime(date_to))]
  df.sort_values(by=['time'])
  return df

