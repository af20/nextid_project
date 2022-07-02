import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from datetime import date, datetime
from dateutil.relativedelta import relativedelta as rd
import numpy as np
import pandas as pd


class cl_stats:
  def __init__(self, df, v_d_trades, starting_capital, trade_cost):
    self.v_d_trades = v_d_trades
    self.v_times = sorted(list(df['time'].apply(lambda x: x.strftime('%Y-%m-%d')).tolist()))
    
    self.v_closes = list(df['close'].tolist())
    df['rets'] = df.close.pct_change()  
    df['rets'] = np.log(1 + df.close.pct_change())
    df['rets_adj'] = df['rets'] * df['direction']
    df['rets_adj_net'] = df['rets_adj'] - df['trade_cost']
    df['capital'] = self.get_wealth(df['rets_adj_net'].tolist(), starting_capital) #(1+df['rets_adj']).cumprod()
    self.equity = list(df['capital'].tolist())

    df_long = df.copy()
    df_short = df.copy()
    df_long['rets_adj_net'] = np.where(df_long['direction'] == -1, 0, df_long['rets_adj_net'])
    df_short['rets_adj_net'] = [x['rets_adj_net'] if x['direction']==-1 else 0 for i,x in df.iterrows()] # df_short.loc[df_short['direction'] == 1, 'rets_adj_net'] = 0 

    self.equity_long = self.get_wealth(df_long['rets_adj_net'].tolist(), starting_capital) #self.get_wealth(df[df['direction'] == 1]['rets_adj_net'].tolist(), starting_capital)
    self.equity_short = self.get_wealth(df_short['rets_adj_net'].tolist(), starting_capital) #self.get_wealth(df[df['direction'] == -1]['rets_adj_net'].tolist(), starting_capital)

    self.total_r = self.get_total_return_from_equity()
    self.total_r_long = self.get_total_return_from_equity(1)
    self.total_r_short = self.get_total_return_from_equity(-1)

    self.avg_r = self.get_measure('avg')
    self.avg_r_long = self.get_measure('avg', 1)
    self.avg_r_short = self.get_measure('avg', -1)

    self.std = self.get_measure('std')
    self.std_long = self.get_measure('std', 1)
    self.std_short = self.get_measure('std', -1)

    self.std_neg = self.get_measure('std_neg')
    self.std_neg_long = self.get_measure('std_neg', 1)
    self.std_neg_short = self.get_measure('std_neg', -1)


    self.rr = self.get_RR(self.avg_r, self.std)
    self.rr_long = self.get_RR(self.avg_r_long, self.std_long)
    self.rr_short = self.get_RR(self.avg_r_short, self.std_short)

    self.rr_neg = self.get_RR(self.avg_r, self.std_neg)
    self.rr_neg_long = self.get_RR(self.avg_r_long, self.std_neg_long)
    self.rr_neg_short = self.get_RR(self.avg_r_short, self.std_neg_short)

    self.avg_duration = self.get_measure('avg', kind='duration') #get_average_duration()
    self.avg_duration_long = self.get_measure('avg', direction=1, kind='duration')
    self.avg_duration_short = self.get_measure('avg', direction=-1, kind='duration')

    self.std_duration = self.get_measure('std', kind='duration')
    self.std_duration_long = self.get_measure('std', direction=1, kind='duration')
    self.std_duration_short = self.get_measure('std', direction=-1, kind='duration')


    #print(self.avg_r, self.avg_r_long, self.avg_r_short)
    #print(self.std, self.std_long, self.std_short)
    #print(self.rr, self.rr_long, self.rr_short)
    #print(self.rr_neg, self.rr_neg_long, self.rr_neg_short)
    #print(self.avg_duration, self.avg_duration_long, self.avg_duration_short)
    
    #import matplotlib.pyplot as plt #plt.plot(self.v_times, self.equity_long)    #plt.show()


  def get_wealth(self, v_returns, starting_capital):
    CAPITAL = starting_capital
    v_returns = np.nan_to_num(v_returns, copy=False)
    v_wealth = [CAPITAL]
    for x in v_returns:
      if np.isnan(x):
        v_wealth.append(CAPITAL)
      else:
        we = round(v_wealth[-1] * (1+x),2)
        v_wealth.append(we)
    return v_wealth[1:]


  def get_total_return_from_equity(self, direction=None):
    assert direction in [None, 1, -1], 'erorr in direction'
    if direction == None:
      eq = self.equity
    else:
      eq = self.equity_long if direction == 1 else self.equity_short
    if len(eq) == 0:
      return None
    return round(eq[-1] / eq[0] -1, 4)


  def get_measure(self, measure, direction=None, kind=None):
    assert measure in ['avg', 'median', 'std', 'std_neg'], 'errror in measure'
    assert direction in [None, 1, -1], 'erorr in direction'
    assert kind in [None, 'returns', 'duration'], 'erorr in kind'

    if kind in [None,'returns']:
      field = 'return_directional_net'
      n_round = 4
    elif kind == 'duration':
      field = 'n_periods'
      n_round = 2
    
    if direction == None:
      v_values = [x[field] for x in self.v_d_trades]
    else:
      v_values = [x[field] for x in self.v_d_trades if x['direction'] == direction]

    if len(v_values) == 0:
      return None

    if measure == 'avg':
      result = np.mean(v_values)
      #print('direction',direction, '  ', v_values, '   mean', result)
    elif measure in 'median':
      result = np.median(v_values)
    elif 'std' in measure:
      if measure == 'std_neg':
        v_values = [x for x in v_values if x < 0]
      if len(v_values) <= 1:
        return None
      result = np.std(v_values)
    
    return round(result, n_round)



  def get_RR(self, avg_r, std):
    if avg_r == None or std in [None, 0]:
      return None
    return round(avg_r / std,2)


  def get_average_duration(self, direction=None):
    assert direction in [None, 1, -1], 'erorr in direction'

    if direction == None:
      v_periods = [x['n_periods'] for x in self.v_d_trades]
    else:
      v_periods = [x['n_periods'] for x in self.v_d_trades if x['direction'] == direction]
    
    if len(v_periods) == 0:
      return None
    return round(np.mean(v_periods),2)


