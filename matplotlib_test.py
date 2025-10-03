import matplotlib
matplotlib.use("Qt5Agg")   # force Qt backend for GUI
import matplotlib.pyplot as plt
import numpy as np

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot
plt.figure()
plt.plot(x, y, label="sine wave")
plt.title("Matplotlib Test Plot")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.legend()

# Show the plot
plt.show()
