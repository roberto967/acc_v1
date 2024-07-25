import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

# Método de estimativa por FT
# 1 - Encontra-se o menor valor de aceleração, que estará dentro do intervalo do tempo de voo
# 2 - Define-se o intervalo de interesse para encontrar o ponto de decolagem com início na primeira intersecção com o zero e o final no ponto de menor aceleração.
# 3 - Percorre-se o intervalo de interesse até encontrar o primeiro ponto em que a aceleração é inferior ao threshold e salva este ponto como instante de decolagem.
# 4 - Define-se o intervalo de interesse para encontrar o ponto de pouso como início no ponto de menor aceleração e final como a próxima intersecção da aceleração o zero.
# 5 - Percorre-se então o intervalo de interesse até encontrar o último ponto em que aceleração é inferior ao threshold e salva-se este ponto como instante de pouso.
# 6 - Calcula-se o tempo de voo como a diferença entre os instantes de pouso e decolagem.
# 7 - Calcula-se a altura do salto usando a equação do tempo de voo.

def ft(data, threshold = -0.5):
    # Encontra o menor valor de aceleração e o índice correspondente
    min_acc = min(data['gFz'])
    min_acc_index = data['gFz'].tolist().index(min_acc)
    
    # Intervalo de interesse para encontrar o ponto de decolagem
    takeoff_start_index = next(i for i in range(min_acc_index, -1, -1) if data['gFz'][i] >= 0)
    takeoff_end_index = min_acc_index
    
    # Encontra o instante de decolagem
    takeoff_index = next(i for i in range(takeoff_start_index, takeoff_end_index + 1) if data['gFz'][i] < threshold)
    
    # Define o intervalo de interesse para encontrar o ponto de pouso
    landing_start_index = min_acc_index
    landing_end_index = next(i for i in range(min_acc_index, len(data)) if data['gFz'][i] >= 0)
    
    # Encontra o instante de pouso
    landing_index = next(i for i in range(landing_start_index, landing_end_index + 1) if data['gFz'][i] < threshold)
    
    # Calcula o tempo de voo
    time_of_flight = data['time'][landing_index] - data['time'][takeoff_index]
    
    # Calcula a altura do salto usando a equação do tempo de voo
    # h = (g * t^2) / 8 -> Tá no artigo, mas deriva de v^2 = v0^2 + 2a * (y - y0)
    g = 9.81  # Aceleração da gravidade em m/s^2
    jump_height = (g * (time_of_flight ** 2)) / 8
    
    return {
        'takeoff_time': data['time'][takeoff_index],
        'landing_time': data['time'][landing_index],
        'time_of_flight': time_of_flight,
        'jump_height(m)': jump_height
    }
    

# Carrega o arquivo CSV
data = pd.read_csv('./teste.csv', sep=';')

# Converter colunas de string para float
data['time'] = data['time'].str.replace(',', '.').astype(float)
data['gFz'] = data['gFz'].str.replace(',', '.').astype(float)

# Extrair as colunas 'time' e 'gFz'
time = data['time'].values
gFz = data['gFz'].values - 1  # Subtrair 1g para obter a aceleração real

cs = CubicSpline(time, gFz)

# Calcular o intervalo total de tempo
time_min = time.min()
time_max = time.max()
total_time = time_max - time_min

# Calculo número de pontos para a frequência alvo (150 Hz)
sampling_frequency = 150 
num_points = int(total_time * sampling_frequency)

# Gerar novos pontos para interpolação
time_new = np.linspace(time_min, time_max, num_points)
gFz_new = cs(time_new)

# Criação e salvamento DataFrame com os dados gerados na interpolação
interpolated_data = pd.DataFrame({
    'time': time_new,
    'gFz': gFz_new
})

interpolated_data.to_csv('dados_interpolados.csv', index=False, sep=';')

resultFT = ft(interpolated_data)

print(resultFT)

# Plot dados originais e interpolados
plt.figure(figsize=(10, 6))
plt.plot(time, gFz, 'o', label='Dados originais', markersize=2)
plt.plot(time_new, gFz_new, '-', label='Interpolação por Splines')
plt.xlabel('Tempo (s)')
plt.ylabel('Acelerações (g) - Eixo Z')

# Intervalos do eixo x e y
plt.gca().xaxis.set_major_locator(MultipleLocator(0.5))
plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))

# Linha threshold
plt.axhline(y=-0.5, color='purple', linestyle='-', label='Linha do threshold', linewidth=0.5)

# Sombra na área do tempo de voo -> Só se considera metado do tempo, considerando que é um pulo e depois a queda
plt.axvspan(resultFT['takeoff_time'], resultFT['landing_time'], color='yellow', alpha=0.3, label='Tempo de voo')

plt.legend()
plt.title('Aceleração em relação ao tempo (g) - Eixo Z')
plt.show()
