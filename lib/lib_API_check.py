import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from datetime import date, datetime

def validate_date_text(date_text):
  try:
    datetime.strptime(date_text, '%Y-%m-%d')
    return True
  except:
    return False



def API_backtest_get_right_values(request):

  from input_values import default_starting_capital, default_min_days, default_ma_periods

  v_args_API = request.args.to_dict(flat=False)

  # Default Values
  capital = default_starting_capital
  min_days = default_min_days
  trade_cost = 0
  ma_periods = default_ma_periods

  
  # CAPITAL, MIN DAYS, TRADE COST
  v_numerical_positive_metrics = ['capital', 'min_days', 'trade_cost', 'ma_periods']
  for field in v_numerical_positive_metrics:
    if field in v_args_API:
      value = request.args.get(field)
      try:
        value = int(value) if field in ['min_days', 'ma_periods'] else float(value)
      except:
        return {'error': field + ' must be a number'}
      if value <= 0:
        sign = '>=' if field == 'trade_cost' else '>'
        return {'error': field + ' must be ' + sign + ' 0'}

      if field == 'capital':
        capital = value
      elif field == 'min_days':
        min_days = value
      elif field == 'trade_cost':
        trade_cost = value
      elif field == 'ma_periods':
        ma_periods = value

  # DATE FROM
  if 'date_from' in v_args_API:
    date_from = request.args.get('date_from')
    if validate_date_text(date_from) == False:
      return {'error': "date_from format must be yyyy-mm-dd"}
    date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
  else:
    date_from = date(1900,1,1)
  date_from = max(date_from, date(1900,1,1))

  # DATE TO
  if 'date_to' in v_args_API:
    date_to = request.args.get('date_to')
    if validate_date_text(date_to) == False:
      return {'error': "date_to format must be yyyy-mm-dd"}
    date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
  else:
    date_to = date(2100,1,1)
  date_to = min(date_to, date(2100,1,1))
  
  if date_to <= date_from:
    return {'error': 'date_to must be > than date_from'}

  return {'capital': capital, 'min_days': min_days, 'date_from': date_from, 'date_to': date_to, 'trade_cost': trade_cost, 'ma_periods': ma_periods}


  capital = 100 if 'capital' not in v_args_API else capital
  search_str = request.args.get('q')
