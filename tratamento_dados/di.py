import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, savgol_filter
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt


def filter_signal(acc, fs, cutoff=0.35, order=4):
    """
    Aplica um filtro Butterworth passa-altas para remover componentes de baixa frequência da aceleração.

    :param acc: Sinal de aceleração (array)
    :param fs: Frequência de amostragem (Hz)
    :param cutoff: Frequência de corte do filtro (Hz)
    :param order: Ordem do filtro Butterworth
    :return: Sinal de aceleração filtrado
    """
    nyquist = 0.5 * fs
    normalized_cutoff = cutoff / nyquist
    b, a = butter(order, normalized_cutoff, btype='high', analog=False)
    acc_filtered = filtfilt(b, a, acc)
    return acc_filtered


def calculate_position(acc, time):
    """
    Integra o sinal de aceleração duas vezes para calcular a posição.

    :param acc: Sinal de aceleração (array)
    :param time: Sinal de tempo (array)
    :return: Posição calculada (array)
    """
    # Integração para calcular a velocidade
    int1 = cumulative_trapezoid(acc, time, initial=0)
    # Integração para calcular a posição
    int2 = cumulative_trapezoid(int1, time, initial=0)
    return int2


def di(time, acc, fs=200):
    """
    Calcula a posição corrigida a partir dos dados de aceleração.

    :param data: DataFrame com colunas 'time' e 'acc' para tempo e aceleração
    :param fs: Frequência de amostragem (Hz)
    :return: Posição corrigida (array)
    """
    # time = data['time']
    acc = acc * 9.81  # Converte aceleração de g para m/s²

    # Calcula a posição integrando duas vezes a aceleração filtrada
    position = calculate_position(acc, time)

    # Aplica filtro Butterworth para corrigir a deriva na posição
    position_corrected = filter_signal(position, fs, cutoff=0.5, order=2)

    # Altura máxima do salto em centímetros
    max_position = np.max(position_corrected) * 100

    # Plot da posição corrigida ao longo do tempo
    plt.figure(figsize=(12, 6))
    plt.plot(time, position, label='Posição Original (m)',
             color='r', linestyle='--')
    plt.plot(time, position_corrected,
             label='Posição Filtrada e Corrigida (m)', color='b')
    plt.title('Posição ao Longo do Tempo - Original vs Filtrada e Corrigida (DI)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.grid(True)
    plt.legend()
    plt.show()

    return max_position
