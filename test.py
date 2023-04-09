import numpy as np
import matplotlib.pyplot as plt	
p = 1.5
q = 0.5

x = [0.5 * i for i in range(100)]
y = [np.power(1+i, p) - np.power(i, p) for i in x]

plt.plot(x, y)
plt.show()
