import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.lib_backtest import get_backtest_stats
from lib.lib_chart import lib_produce_chart

from flask import *
from lib.lib_API_check import *

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/hello', methods=['GET'])
def hello():
  return {'response': 'ciao'}, 200


def create_response_json(x):
  for y in x.v_d_trades:
    y['tfrom'] = str(y['tfrom'].date())
    y['tto'] = str(y['tto'].date())

  
  J = {
    'metrics': {
      'all': {'total_r': x.total_r, 'avg_r': x.avg_r, 'std': x.std, 'rr': x.rr, 'std_neg': x.std_neg, 'rr_neg': x.rr_neg, 'duration_avg': x.avg_duration, 'duration_std': x.std_duration},
      'long': {'total_r': x.total_r_long, 'avg_r': x.avg_r_long, 'std': x.std_long, 'rr': x.rr_long, 'std_neg': x.std_neg_long, 'rr_neg': x.rr_neg_long, 'duration_avg': x.avg_duration_long, 'duration_std': x.std_duration_long},
      'short': {'total_r': x.total_r_short, 'avg_r': x.avg_r_short, 'std': x.std_short, 'rr': x.rr_short, 'std_neg': x.std_neg_short, 'rr_neg': x.rr_neg_short, 'duration_avg': x.avg_duration_short, 'duration_std': x.std_duration_short}
    },
    'equity_lines': {'all': x.equity, 'long': x.equity_long, 'short': x.equity_short, 'times': x.v_times},
    'trades': {
      'v_max': [{'time': y['tfrom'], 'price': y['pfrom']} for y in x.v_d_trades if y['direction'] == -1],
      'v_min': [{'time': y['tfrom'], 'price': y['pfrom']} for y in x.v_d_trades if y['direction'] == 1],
      'list': x.v_d_trades
    }
  }
  J['chart'] = lib_produce_chart(x, J)
  return J


@app.route('/backtest', methods=['GET'])
def API_get_backtest():

  J = API_backtest_get_right_values(request)
  if 'error' in J.keys():
    return J
  capital, min_days, date_from, date_to, trade_cost, ma_periods = J['capital'], J['min_days'], J['date_from'], J['date_to'], J['trade_cost'], J['ma_periods']
  x = get_backtest_stats(capital, date_from, date_to, trade_cost, min_days)
  J = create_response_json(x)
  return J


# def find_optimal_days (in base a una metrica, input date, commissione)
# def proiezione con MMobile N_periodi

app.run(host = '0.0.0.0', port = 5000)

