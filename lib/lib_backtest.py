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

from lib.lib_data import get_bitcoin_data

from cl.cl_py import cl_stats



def get_expanded_v_d_trades(df, v_d_trades, trade_cost):
  for i,x in enumerate(v_d_trades):
    if i == len(v_d_trades)-1:
      x['n_periods'] = df.index[-1] - x['i']
      x['tfrom'] = df.iloc[x['i']].time#.date()
      x['tto'] = df.iloc[df.index[-1]].time#.date()
      x['pfrom'] = df.iloc[x['i']].close
      x['pto'] = df.iloc[df.index[-1]].close
    else:
      x['n_periods'] = v_d_trades[i+1]['i'] - x['i']
      x['tfrom'] = df.iloc[x['i']].time#.date()
      x['tto'] = df.iloc[v_d_trades[i+1]['i']].time#.date()
      x['pfrom'] = df.iloc[x['i']].close
      x['pto'] = df.iloc[v_d_trades[i+1]['i']].close
    x['return_directional'] = round(x['pto'] / x['pfrom'] - 1,4) * x['direction']
    x['return_directional_net'] = round(x['return_directional'] - trade_cost,6)
    #print(x['i'], '  ', x['direction'], '   ', x['n_periods'], '   ', x['tfrom'], '-', x['tto'], '   ', x['pfrom'], '-', x['pto'], '  ret:', x['return_directional'], '   net', x['return_directional_net'])
  return v_d_trades




def get_backtest_stats(starting_capital, date_from, date_to, trade_cost, min_days, ma_periods=None):
  assert min_days != None or ma_periods != None, 'Error' 
  modality = 'ma' if ma_periods != None else 'min_days'

  df = get_bitcoin_data(date_from, date_to)
  MIN = min_days

  if modality == 'min_days':
    col_1 = 'shift_after'
    col_2 = 'close'
    col_3 = 'close_after_half'
    df[col_1] = df['close'].shift(periods=-MIN) #df['shift_before'] = df['close'].shift(periods=MIN)
    half_Min = max(1,MIN//2)
    df[col_3] = df['close'].shift(periods=-half_Min)

  elif modality == 'ma':
    col_1 = 'ma'
    col_2 = 'close'
    df[col_1] = df[col_2].rolling(window=ma_periods).mean().tolist()


  df = df[df[col_1].notna()]  # if np.isnan(x[col_1]): break
  df = df[df[col_3].notna()]
  df.reset_index(inplace=True)

  x = df.iloc[0]
  if x[col_1] >= x[col_2]:
    direction = 1
  else:
    direction = -1
  v_d_trades = [{'i': 0, 'direction': direction}] # d_trades {'id': id, 'direction': 1 (long) oppure -1 (short)}


  v_direction, v_trade_cost = [], []

  for i,x in df.iterrows():
    last_direction = v_d_trades[-1]['direction']
    days_elapsed = i - v_d_trades[-1]['i']
    t_cost = 0

    if i == 0 or days_elapsed < MIN:
      pass
    else:
      if x[col_1] > x[col_2]:
        if last_direction in [-1, None]:
          if x[col_2] < x[col_3]: # voglio una salita progressiva
            v_d_trades.append({'i': i, 'direction': 1})
            last_direction = 1
            t_cost = trade_cost
      else: # close(col_2) > futuro15
        if last_direction in [1, None]:
          if x[col_2] > x[col_3]: # voglio una discesa progressiva
            v_d_trades.append({'i': i, 'direction': -1})
            last_direction = -1
            t_cost = trade_cost
    v_direction.append(last_direction)
    v_trade_cost.append(t_cost)
  
  df['direction'] = v_direction
  df['trade_cost'] = v_trade_cost

  v_d_trades = get_expanded_v_d_trades(df, v_d_trades, trade_cost)
  K = cl_stats(df, v_d_trades, starting_capital, trade_cost)

  return K

