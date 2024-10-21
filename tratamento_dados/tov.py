import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt


def filter_signal(acc, fs, cutoff=0.94, order=4):
    """
    Aplica um filtro Butterworth passa-altas para remover deriva do sinal.

    :param acc: Série de aceleração
    :param fs: Frequência de amostragem
    :param cutoff: Frequência de corte para o filtro passa-altas
    :param order: Ordem do filtro Butterworth
    :return: Sinal filtrado
    """
    nyquist = 0.5 * fs
    normalized_cutoff = cutoff / nyquist
    b, a = butter(order, normalized_cutoff, btype='high', analog=False)
    acc_filtered = filtfilt(b, a, acc)
    return acc_filtered


def calculate_velocity(acc, time):
    """
    Calcula a velocidade através da integração numérica do sinal de aceleração.

    :param acc: Série de aceleração filtrada
    :param time: Série de tempo correspondente
    :return: Série de velocidade
    """
    velocity = cumulative_trapezoid(acc, time, initial=0)
    return velocity


def calculate_height(velocity):
    """
    Calcula a altura do salto usando a velocidade de propulsão (velocidade máxima).

    :param velocity: Série de velocidade corrigida
    :return: Altura do salto
    """
    propulsive_velocity = np.max(velocity)

    g = 9.81  # Aceleração da gravidade 
    height = (propulsive_velocity ** 2) / (2 * g)
    return height * 100  # Convertendo para centímetros


def tov(time, acc, fs=200):
    time = time
    acc = acc * 9.81

    velocity = calculate_velocity(acc, time)

    velocity_corrected = filter_signal(velocity, fs)

    # FFT
    freqs = np.fft.rfftfreq(len(velocity), d=1/fs)
    vel_fft = np.fft.rfft(velocity)  
    magnitude = np.abs(vel_fft)  

    plt.bar(freqs, magnitude, width=0.05,
            color='black', alpha=0.6, label='Magnitude')
    plt.plot(freqs, magnitude, 'g.', label='Magnitude (Pontuada)')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Espectro de Frequência do sina de velocidade')
    plt.grid(True)
    # Freq corte
    plt.axvline(x=0.94, color='red', linestyle='--', label='fc=0.94')
    plt.legend()
    plt.show()

    # Plot da velocidade e da velocidade filtrada ao longo do tempo
    plt.figure(figsize=(12, 6))
    plt.plot(time, velocity, label='Velocidade Original (m/s)',
             color='r', linestyle='--')
    plt.plot(time, velocity_corrected,
             label='Velocidade Filtrada (m/s)', color='b')
    plt.title('Velocidade ao Longo do Tempo - Original vs Filtrada (TOV)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Velocidade (m/s)')
    plt.grid(True)
    plt.legend()
    plt.show()

    height = calculate_height(velocity_corrected)

    return height
