import matplotlib.pyplot as plt

def ft(data, threshold = 0):
    # Encontra o menor valor de aceleração e o índice correspondente
    min_acc = min(data['acc'])
    min_acc_index = data['acc'].tolist().index(min_acc)
    
    # Intervalo de interesse para encontrar o ponto de decolagem
    takeoff_start_index = next(i for i in range(min_acc_index, -1, -1) if data['acc'][i] >= 0)
    takeoff_end_index = min_acc_index
    
    # Encontra o instante de decolagem
    takeoff_index = next(i for i in range(takeoff_start_index, takeoff_end_index + 1) if data['acc'][i] < threshold)
    
    # Define o intervalo de interesse para encontrar o ponto de pouso
    landing_start_index = min_acc_index
    landing_end_index = next(i for i in range(min_acc_index, len(data)) if data['acc'][i] >= 0)
    
    # Encontra o instante de pouso
    landing_index = next(i for i in range(landing_start_index, landing_end_index + 1) if data['acc'][i] < threshold)
    
    # Calcula o tempo de voo
    time_of_flight = data['time'][landing_index] - data['time'][takeoff_index]
    
    # Calcula a altura do salto usando a equação do tempo de voo
    # h = (g * t^2) / 8 -> Tá no artigo, mas deriva de v^2 = v0^2 + 2a * (y - y0)
    g = 9.81  # Aceleração da gravidade em m/s^2
    jump_height = ((g * (time_of_flight ** 2)) / 8) * 100  # Convertendo para centímetros
    
    # Plot do gráfico com destaque no tempo de voo
    plt.figure(figsize=(10, 6))
    plt.plot(data['time'], data['acc'], label='Aceleração')
    plt.axvspan(data['time'][takeoff_index], data['time'][landing_index], color='yellow', alpha=0.3, label='Tempo de Voo')
    plt.axvline(data['time'][takeoff_index], color='green', linestyle='--', label='Decolagem')
    plt.axvline(data['time'][landing_index], color='red', linestyle='--', label='Pouso')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (m/s²)')
    plt.title('Análise do Salto Vertical')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return {
        'takeoff_time': data['time'][takeoff_index],
        'landing_time': data['time'][landing_index],
        'time_of_flight': time_of_flight,
        'jump_height': jump_height
    }
    