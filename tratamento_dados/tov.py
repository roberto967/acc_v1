import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt

def filter_signal(acc, fs, cutoff=0.4, order=4):
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
    # Integração do sinal de aceleração para obter velocidade usando Regra dos Trapézios
    velocity = cumulative_trapezoid(acc, time, initial=0)
    return velocity

def calculate_height(velocity):
    """
    Calcula a altura do salto usando a velocidade de propulsão (velocidade máxima).
    
    :param velocity: Série de velocidade corrigida
    :return: Altura do salto
    """
    # Obtém a velocidade máxima durante a fase de voo
    propulsive_velocity = np.max(velocity)
    
    # Calcula a altura do salto usando a fórmula da cinemática: h = (v^2) / (2 * g)
    g = 9.81  # Aceleração da gravidade em m/s^2
    height = (propulsive_velocity ** 2) / (2 * g)
    return height * 100 # Convertendo para centímetros

def tov(time, acc, fs =150):
  time = time
  # g to m/s^2
  acc = acc * 9.81

  # Calculando a velocidade integrando a aceleração filtrada
  velocity = calculate_velocity(acc, time)

  # Corrigindo a deriva na velocidade com um filtro Butterworth
  velocity_corrected = filter_signal(velocity, fs, cutoff=0.4, order=2)
  
  # Plot da velocidade e da velocidade filtrada ao longo do tempo
  plt.figure(figsize=(12, 6))
  plt.plot(time, velocity, label='Velocidade Original (m/s)', color='r', linestyle='--')
  plt.plot(time, velocity_corrected, label='Velocidade Filtrada (m/s)', color='b')
  plt.title('Velocidade ao Longo do Tempo - Original vs Filtrada (TOV)')
  plt.xlabel('Tempo (s)')
  plt.ylabel('Velocidade (m/s)')
  plt.grid(True)
  plt.legend()
  plt.show()

  # Calculando a altura do salto usando a velocidade de propulsão
  height = calculate_height(velocity_corrected)

  return height
