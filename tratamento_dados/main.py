from collect_data import read_csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.interpolate import CubicSpline
from ft import ft
from tov import tov
from scipy.fft import fft, fftfreq
import pandas as pd

# Leitura dos dados do CSV
data = read_csv('./teste.csv', ",")

# Dados de aceleração e tempo
acc = data['gFz'].values
time = data['time'].values
n = len(acc)

# Estimando a frequência de amostragem a partir dos dados de tempo
dt_array = np.diff(time)
dt = np.mean(dt_array)
fs = 1 / dt
print(f"Frequência de amostragem estimada do sensor: {fs:.2f} Hz")

# fft
acc_fft = fft(acc)
frequencies = fftfreq(n, dt)

positive_frequencies = frequencies[:n // 2]
positive_magnitudes = 2.0 / n * np.abs(acc_fft[:n // 2])

plt.figure(figsize=(8, 6))
plt.bar(positive_frequencies, positive_magnitudes,
        width=0.1, color='black')
plt.plot(positive_frequencies, positive_magnitudes, 'go', markersize=3)
plt.axvline(x=15, color='r', linestyle='--', label='fc = 15 Hz')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.title('Espectro de Fourier do sinal de aceleração')
plt.legend()
plt.grid(True)
plt.show()

# Butterworth passa-baixas
fc = 15
order = 4
nyquist = 0.5 * fs
normal_cutoff = fc / nyquist

b, a = butter(order, normal_cutoff, btype='low', analog=False)

acc_filtered = filtfilt(b, a, acc)

plt.figure(figsize=(10, 6))

plt.plot(time, acc, label='Sinal original', alpha=0.6)

plt.plot(time, acc_filtered, label='Sinal filtrado (fc = 15 Hz)', linewidth=2)

plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (g)')
plt.title('Sinal original e sinal filtrado')
plt.legend()
plt.grid(True)
plt.show()

acc = acc_filtered

# Passo 1: Agrupar os dados por intervalos de tempo (binar os dados)
n_bins = n // 8
t_min = time.min()
t_max = time.max()
bin_edges = np.linspace(t_min, t_max, n_bins + 1)

# Atribuir cada ponto de dados a um bin
bin_indices = np.digitize(time, bin_edges)

# Inicializar arrays para armazenar os dados binados
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
acc_binned = np.zeros(n_bins)
counts = np.zeros(n_bins)

# Acumular os valores de aceleração em cada bin
for i in range(n):
    bin_idx = bin_indices[i] - 1  # Ajuste para indexação baseada em zero
    if 0 <= bin_idx < n_bins:
        acc_binned[bin_idx] += acc[i]
        counts[bin_idx] += 1

# Passo 2: Calcular a média da aceleração em cada bin
with np.errstate(divide='ignore', invalid='ignore'):
    acc_binned = np.divide(acc_binned, counts, out=np.zeros_like(
        acc_binned), where=counts != 0)

# Rm bins com contagem zero
valid_bins = counts > 0
bin_centers_valid = bin_centers[valid_bins]
acc_binned_valid = acc_binned[valid_bins]

print(f"Número de bins válidos: {len(bin_centers_valid)}")

# Frequência de amostragem desejada
fs_new = 200
dt_new = 1 / fs_new

uniform_time_new = np.arange(t_min, t_max, dt_new)

print(f"Número de pontos depois da interpolação: {len(uniform_time_new)}")

# Passo 3
cs = CubicSpline(bin_centers_valid, acc_binned_valid)
acc_interpolated_new = cs(uniform_time_new)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(time, acc, '-', label=f'Dados Originais filtrados ({fs:.2f} Hz)')
plt.plot(bin_centers_valid, acc_binned_valid, 's', label='bins')
plt.plot(uniform_time_new, acc_interpolated_new, 'r-',
         label='Interpolação Cúbica (200 Hz)')
plt.legend()
plt.xlabel('Tempo')
plt.ylabel('Aceleração')
plt.title('Sinal de aceleração pós filtragem, interpolação e binagem')
plt.grid(True)
plt.show()


# resultado ft
print(f"Resultado do cálculo do salto vertical: {
      ft(pd.DataFrame({'time': uniform_time_new, 'acc': acc_interpolated_new}))}")
# tov
print(f"Resultado do cálculo do tempo de voo: {
      tov(uniform_time_new, acc_interpolated_new)}")
