import numpy as np
import matplotlib.pyplot as plt
from graph import Graph
from config import constrained_config

def test1():

    p = 1.5
    q = 0.5

    x = [0.5 * i for i in range(100)]
    y = [np.power(1+i, p) - np.power(i, p) for i in x]

    plt.plot(x, y)
    plt.show()


def test2():

    matrix = [[1, 0, 0, 1, 0], [1, 0, 1, 1, 1], [
        0, 1, 1, 0, 1], [0, 1, 0, 1, 1], [1, 0, 1, 0, 1]]
    graph = Graph.load_matrix(matrix)
    laplapian_matrix = graph.export_laplapian_matrix()
    print(laplapian_matrix)
    eigenvalue, feature = np.linalg.eig(laplapian_matrix.T)
    print("laplabian:  ")
    print(eigenvalue)
    print(feature)
    n = len(graph.nodes)
    diga_matrix = np.zeros((n, n))
    for i in range(n):
        print(type(eigenvalue[i]))
        if np.abs(eigenvalue[i]) < 1e-4:
            for j in range(n):
                diga_matrix[j][j] = -feature[j, i]
    print("diagmatrix:   ")
    print(diga_matrix)
    EL_matrix = np.matmul(diga_matrix, laplapian_matrix)
    print(EL_matrix)
    eigenvalue, feature = np.linalg.eig(EL_matrix)
    print("EL:  ")
    print(eigenvalue)
    print(feature)

    graph.draw_graph()
