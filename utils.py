import scipy.special as sp
import numpy as np
from graph import Graph

def combine_dict(share, private):

    for key, value in share.items():
        for id, agent in private.items():
            agent[key] = value

    return private


def get_settle_time_2019(p, q, alpha, beta):

    k = 1
    
    mp = (1-k*p) / (q-p)
    mq = (k*q-1) / (q-p)

    gama = sp.gamma(mp)*sp.gamma(mq) / (np.power(alpha, k) * sp.gamma(k)* (q-p))

    gama = gama * np.power((alpha/beta), mp)
    
    settle_time = gama

    return gama


def get_settle_time2013(p, q, alpha, beta):
    
    settle_time = (1/(alpha*(1-p)) + 1/(beta*(q-1)))

    return settle_time


def get_settle_time_consesus():
    pass


def get_settle_time_equilibrium(p, q, delta, eta, m):
    
    p_hat = (p+1)/2
    q_hat = (q+1)/2
    alpha = np.power(2, p_hat)*delta*np.power(m, p)
    beta = np.power(2, q_hat)*eta*np.power(m, q)

    print(get_settle_time2013(p_hat, q_hat, alpha, beta))
    print(get_settle_time_2019(p_hat, q_hat, alpha, beta))

def get_eigenvalue_from_matrix(matrix):

    matrix = [[1, 1, 0, 0, 0], [0, 1, 1, 0, 0], [
        0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [1, 0, 0, 0, 1]]
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

    # graph.draw_graph()


# print(get_settle_time2013(0.5, 1.5, 2, 2))
get_settle_time_equilibrium(0.5, 1.5, 2, 2, 0.5)
get_eigenvalue_from_matrix(None)