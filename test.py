# import numpy as np
# import matplotlib.pyplot as plt	
# p = 1.5
# q = 0.5

# x = [0.5 * i for i in range(100)]
# y = [np.power(1+i, p) - np.power(i, p) for i in x]

# plt.plot(x, y)
# plt.show()
x = []
y = []
theta = []
varphi = []
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line_list = line.split()
        x.append(line_list[0])
        y.append(line_list[1])
        theta.append(line_list[2])
        varphi.append(line_list[4])

print(x)
print(len(x))