import numpy as np
import matplotlib.pyplot as plt
from waveform import Waveform

# Parameters for the Lissajous curve
A = 1         # amplitude in x
B = 1         # amplitude in y
a = 5         # frequency in x
b = 4         # frequency in y
delta = np.pi / 2  # phase shift

w = Waveform(1000)
# Time array
t = w.get_waveform('Celtic2')
x = t[:, 0]
y = t[:, 1]

# Parametric equations

# Plotting
plt.figure(figsize=(6, 6))
plt.plot(x, y, color='blue', lw=2)
plt.title("Lissajous Curve")
plt.xlabel("x(t)")
plt.ylabel("y(t)")
plt.axis('equal')
plt.grid(True)
plt.show()
