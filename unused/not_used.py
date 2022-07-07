

'''
class py_ticker_data:
  def __init__(self, time, open_:float, high:float, low:float, close_:float, volume:float, provider=None):
    self.time = time
    self.open = float(open_)
    self.high = float(high)
    self.low = float(low)
    self.close = float(close_)
    if volume != None:
      volume = int(float(volume)) if type(volume) == str else volume
      volume = None if np.isnan(volume) == True else volume
    self.volume = int(volume) if volume != None else 0
    self.provider = int(provider) if provider != None else None

    self.high = max(self.open, self.high, self.low, self.close)
    self.low = min(self.open, self.high, self.low, self.close)


def libg_finnhub_get_historical_data(api_symbol, timestamp_from, timestamp_to=None):
  import finnhub
  finhub_API_token = os.environ["FINHUB_API_TOKEN"]
  finnhub_client = finnhub.Client(api_key=finhub_API_token)

  timestamp_to = datetime.timestamp(datetime.now()) if timestamp_to == None else timestamp_to
  timestamp_from, timestamp_to = int(timestamp_from), int(timestamp_to)

  d_data = finnhub_client.crypto_candles(api_symbol, 'D', timestamp_from, timestamp_to)
  try: # se non ci sono dati nella risposta     {"c":null,"h":null,"l":null,"o":null,"s":"ok","t":null,"v":null}
    v_date = [datetime.fromtimestamp(x).date() for x in d_data['t']]
    v_open, v_high, v_low, v_close, v_volume = d_data['o'], d_data['h'], d_data['l'], d_data['c'], d_data['v']
  except:
    return []

  v_hd = []
  for i in range(len(v_open)):
    v_hd.append(py_ticker_data(v_date[i], v_open[i], v_high[i], v_low[i], v_close[i], v_volume[i], provider=15))

  return v_hd
'''