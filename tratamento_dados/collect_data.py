import pandas as pd

def read_csv(data_path, _sep=';', is_float=True):
  data = pd.read_csv(data_path, sep=_sep)
  
  print(data.__len__())
  
  data.drop_duplicates(subset=['time'], keep='first', inplace=True)
  
  print(data.__len__())
  
  if(not is_float):
    data['time'] = data['time'].str.replace(',', '.').astype(float)
    data['gFz'] = data['gFz'].str.replace(',', '.').astype(float)
  
  data['gFz'] = data['gFz'] - 1

  return data