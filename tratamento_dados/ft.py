import matplotlib.pyplot as plt


def ft(data, threshold=-0.5):
    min_acc = min(data['acc'])
    min_acc_index = data['acc'].tolist().index(min_acc)

    takeoff_index = next(i for i in range(
        min_acc_index, -1, -1) if data['acc'][i] > threshold)

    takeoff_acc = data['acc'][takeoff_index]

    landing_index = min(
        range(takeoff_index + 1, len(data['acc'])),
        key=lambda i: abs(data['acc'][i] - threshold)
    )

    time_of_flight = data['time'][landing_index] - data['time'][takeoff_index]

    g = 9.81  
    jump_height = ((g * (time_of_flight ** 2)) / 8) * 100

    plt.figure(figsize=(10, 6))
    plt.plot(data['time'], data['acc'], label='Aceleração')

    plt.axvspan(
        data['time'][takeoff_index],
        data['time'][landing_index],
        color='yellow',
        alpha=0.3,
        label='Tempo de salto'
    )

    plt.axvline(data['time'][takeoff_index], color='green',
                linestyle='--', label='Decolagem')
    plt.axvline(data['time'][landing_index], color='red',
                linestyle='--', label='Pouso')

    plt.scatter(data['time'][takeoff_index], data['acc'][takeoff_index],
                color='green', marker='x', s=100, label='Ponto de Decolagem')
    plt.scatter(data['time'][landing_index], data['acc'][landing_index],
                color='red', marker='x', s=100, label='Ponto de Pouso')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (g)')
    plt.title('Análise FT')
    plt.legend()
    plt.grid(True)
    plt.show()

    return {
        'takeoff_time': data['time'][takeoff_index],
        'landing_time': data['time'][landing_index],
        'time_of_flight': time_of_flight,
        'jump_height (cm)': jump_height
    }
