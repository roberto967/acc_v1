from collect_data import read_csv
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from tov import tov
from di import di
from ft import ft
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.fft import fft, fftfreq
from scipy.interpolate import UnivariateSpline

def pb_ord_4_ctt_6(signal, fs, cutoff=6, order=4):
  nyquist = 0.5 * fs
  normalized_cutoff = cutoff / nyquist
  b, a = butter(order, normalized_cutoff, btype='low', analog=False)
  filtered_signal = filtfilt(b, a, signal)
  return filtered_signal

def calculate_frequency(time):
    # Calcula as diferenças entre os tempos consecutivos para encontrar o período de amostragem
    time_diffs = np.diff(time)
    
    # Calcula o período médio de amostragem
    average_period = np.mean(time_diffs)
    
    # Calcula a frequência de amostragem como o inverso do período médio
    frequency = 1 / average_period
    
    return frequency

data = read_csv('./teste.csv', ",")

acc = data['gFz']
time = data['time']

freq = calculate_frequency(time)
print("Frequência de amostragem: ", freq)

acc = pb_ord_4_ctt_6(acc, freq)

target_freq = 200
spl = UnivariateSpline(time, acc, s = 0)
time_spl =  np.linspace(time.min(), time.max(), target_freq)
acc_spl = spl(time_spl)

plt.figure(figsize=(12, 6))
plt.plot(time, acc, 'r-', label='Dados Originais')
plt.plot(time_spl, acc_spl, 'b-', label='Spline Interpolada')
plt.title('Antes')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s²)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

tov_result = tov(time_spl, acc_spl, target_freq)
di_result = di(time_spl, acc_spl, target_freq)

print("TOV: ", tov_result)
print("DI: ", di_result)

# ft_data = {
#     'time': time_spl,
#     'acc': acc_spl
# }

# data = pd.DataFrame(ft_data)

# ft_result = ft(data)
# print("FT: ", ft_result["jump_height"])