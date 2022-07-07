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

def get_wealth(v_returns):
  v_returns = np.nan_to_num(v_returns, copy=False)
  v_wealth = [CAPITAL]
  for x in v_returns:
    if np.isnan(x):
      v_wealth.append(CAPITAL)
    else:
      we = v_wealth[-1] * (1+x)
      v_wealth.append(we)
  return v_wealth[1:]



class cl_stats:
  def __init__(self, df, v_d_trades):
    self.v_rets = df['rets'].tolist()
    self.v_rets_adj = v_rets_adj = df['rets_adj'].tolist()
    # TODO aggiungi colonna costo e net

    self.median_r = round(np.median(v_rets_adj),4)
    self.mean_r = round(np.mean(v_rets_adj),4)
    self.std = round(np.std(v_rets_adj),4)
    self.rr = round(self.mean_r / self.std,2)
    v_duration = [x['periods'] for x in v_d_trades]
    self.avg_duration = np.mean(v_duration)
    self.avg_duration_long = np.mean([x['periods'] for x in v_d_trades if x['direction'] == 1])
    self.avg_duration_short = np.mean([x['periods'] for x in v_d_trades if x['direction'] == -1])

  def get_return_measure(v_rets, measure):
    if len(v_rets) == 0:
      return None
    assert measure in ['mean', 'median', 'std']
    if measure == 'mean':
      result = np.mean(v_rets)
    elif measure == 'median':
      result = np.median(v_rets)
    elif measure == 'std':
      if len(v_rets) <= 1:
        return None
    return round(result, 4)

  #def get_duration()







CAPITAL = 100
MIN = 15
ShiftNC = 'shift_after'


df = get_bitcoin_data()
df[ShiftNC] = df['close'].shift(periods=-MIN) #df['shift_before'] = df['close'].shift(periods=MIN)
df = df[df[ShiftNC].notna()]  # if np.isnan(x[ShiftNC]): break


x = df.iloc[0]
if x[ShiftNC] >= x.close:
  direction = 1
else:
  direction = -1
v_d_trades = [{'i': 0, 'direction': direction}] # d_trades {'id': id, 'direction': 1 (long) oppure -1 (short)}


v_direction = []

for i,x in df.iterrows():
  last_direction = v_d_trades[-1]['direction']
  days_elapsed = i - v_d_trades[-1]['i']

  if i == 0 or days_elapsed < MIN:
    pass
  else:
    if x[ShiftNC] > x.close:
      if last_direction in [-1, None]:
        v_d_trades.append({'i': i, 'direction': 1})
        last_direction = 1
    else:
      if last_direction in [1, None]:
        v_d_trades.append({'i': i, 'direction': -1})
        last_direction = -1
  v_direction.append(last_direction)


df['rets'] = df.close.pct_change()
df['direction'] = v_direction
df['rets_adj'] = df['rets'] * df['direction']
#df['log_return'] = np.log(1 + df.pct_ch)
df['capital'] = get_wealth(df['rets_adj'].tolist()) #(1+df['rets_adj']).cumprod()



for i,x in enumerate(v_d_trades):
  if i == len(v_d_trades)-1:
    x['periods'] = df.index[-1] - x['i']
    x['from'] = df.iloc[x['i']].time#.date()
    x['to'] = df.iloc[df.index[-1]].time#.date()
    x['pfrom'] = df.iloc[x['i']].close
    x['pto'] = df.iloc[df.index[-1]].close
  else:
    x['periods'] = v_d_trades[i+1]['i'] - x['i']
    x['from'] = df.iloc[x['i']].time#.date()
    x['to'] = df.iloc[v_d_trades[i+1]['i']].time#.date()
    x['pfrom'] = df.iloc[x['i']].close
    x['pto'] = df.iloc[v_d_trades[i+1]['i']].close

  print(x['i'], '  ', x['direction'], '   ', x['periods'], '   ', x['from'], '-', x['to'], '   ', x['pfrom'], '-', x['pto'])


print(df[0:50])


import matplotlib.pyplot as plt
df.plot(x='time', y='capital')
#plt.show()
a=9283/0





x = v_d_trades[0]
for i,x in enumerate(v_d_trades):
  df.loc[    df['time'].between(x['from'], x['to']),    ['direction']] = '-1'
  print(df)
  a=987/0



# Get the 'id' column indexed by the 'start'/'end' intervals.
s = pd.Series(df.index.values, pd.IntervalIndex.from_arrays(x['from'], x['to']))

# Map based on the date of df_a.
df['direction'] = df.index.map(s)
print(df)



a=933/0
#mask = (df['time'] > x['from']) & (df['time'] <= x['to'])#print(df.loc[mask])

LOC = df[df['time'].between(x['from'], x['to'])]


'''
for i,x in enumerate(v_d_trades):


  df = pd.DataFrame(np.random.random((200,3)))
  df['date'] = pd.date_range('2000-1-1', periods=200, freq='D')
  mask = (df['date'] > '2000-6-1') & (df['date'] <= '2000-6-10')
  print(df.loc[mask])'''