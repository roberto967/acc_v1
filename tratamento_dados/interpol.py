import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Dados iniciais
x = np.arange(6)
y = np.array([3, 1, 4, 1, 5, 9])

# spline com s=0 (sem suavização)
spl = UnivariateSpline(x, y, s=0)

x_fine = np.linspace(0, 5, 100)
y_fine = spl(x_fine)

plt.figure(figsize=(12, 6))

# Antes (dados originais)
plt.subplot(1, 2, 1)
plt.plot(x, y, 'ro', label='Dados Originais')
plt.title('Antes')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)

# Depois (spline interpolada)
plt.subplot(1, 2, 2)
plt.plot(x, y, 'ro', label='Dados Originais')
plt.plot(x_fine, y_fine, 'bo', label='Spline Interpolada')
plt.title('Depois')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
