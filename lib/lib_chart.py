import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.lib_general import libg_get_python_date_from_date
from dateutil.relativedelta import relativedelta as rd

N_DAYS = 1

def lib_produce_chart(x, Jinp):
  J = {
    'dataZoom': [
      {
        'type': 'inside',
        'start': 0,
        'end': 100
      },
      {
        'start': 0,
        'end': 100
      }
    ],
    'xAxis': {
      'type': 'category',
      'data': x.v_times
    },
    'yAxis': {'type': 'value'},
    'series': 
    [
      {
        'data': x.v_closes,
        'type': 'line',
        'markArea': {
              'itemStyle': {'color': 'red'},
              'data': []
          }
      },
      {'data': [None for y in x.v_closes],'type': 'line', 'markArea': {'itemStyle': {'color': 'green'}, 'data': []}}
    ]
  }
  for y in Jinp['trades']['v_max']:
    J['series'][0]['markArea']['data'].append([
      {'xAxis': y['time']},
      {'xAxis': str(libg_get_python_date_from_date(y['time']) + rd(days=N_DAYS))}
    ])
  for y in Jinp['trades']['v_min']:
    J['series'][1]['markArea']['data'].append([
      {'xAxis': y['time']},
      {'xAxis': str(libg_get_python_date_from_date(y['time']) + rd(days=N_DAYS))}
    ])

  return J