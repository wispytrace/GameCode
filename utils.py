import scipy.special as sp
import numpy as np
from graph import Graph
from sympy import symbols, diff
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

def get_eigenvalue_from_matrix():

    N = 3
    matrix = [[0, 1, 0], [1, 0, 1], [1, 0, 0]]
    graph = Graph.load_matrix(matrix)
    laplapian_matrix = graph.export_laplapian_matrix()
    print(laplapian_matrix)
    I_matrix = np.eye(N)
    L_otimics_I = np.kron(laplapian_matrix, I_matrix)
    M_matrix = np.zeros((N*N, N*N))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                    M_matrix[int(i*N+j)][int(i*N+j)] = 1
    
    P = L_otimics_I + M_matrix
    print(P)
    print(P.T)
    inv_p = np.linalg.inv(P.T)
    E = np.matmul(inv_p,P)
    print(E)
    eigenvalue, feature = np.linalg.eig((E+E.T)/2)
    print(eigenvalue)
    alhpa = 0.5
    x1,x2,x3,x4,x5,x6,x7,x8,x9 = symbols('x1,x2,x3,x4,x5,x6,x7,x8,x9')
    f = 
    # for epoch in range(1000):
    #     x = np.random.uniform(-1, 1, N*N)
    #     y = np.matmul(P, x)
    #     for i in range(N*N):
    #         if y[i] < 0:
    #             y[i] = - np.power(np.fabs(y[i]), 0.5)
    #         else:
    #             y[i] = np.power(np.fabs(y[i]), 0.5)
        
    #     x_T = np.matmul(P.T, x)

    #     print(x_T)
    #     print(y)
    #     results = np.matmul(x_T.T, y)
    #     results += np.matmul(np.matmul(P, x).T, y)
    #     print(results)
    #     if results < 0:
    #         print("find negative!")
    #         return


    # eigenvalue, feature = np.linalg.eig(laplapian_matrix.T)
    # print("laplabian:  ")
    # print(eigenvalue)
    # print(feature)
    # n = len(graph.nodes)
    # diga_matrix = np.zeros((n, n))
    # for i in range(n):
    #     print(type(eigenvalue[i]))
    #     if np.abs(eigenvalue[i]) < 1e-4:
    #         for j in range(n):
    #             diga_matrix[j][j] = -feature[j, i]
    # print("diagmatrix:   ")
    # print(diga_matrix)
    # EL_matrix = np.matmul(diga_matrix, laplapian_matrix)
    # print(EL_matrix)
    # eigenvalue, feature = np.linalg.eig(EL_matrix)
    # print("EL:  ")
    # print(eigenvalue)
    # print("feature")
    # print(feature)

    # graph.draw_graph()


def test_positive():
    L = [[1,0,0,-1],
         [-1,1,0,0],
         [0,-1,1,0],
         [0,0,-1,1]]
    L = np.matrix(L)
    matrix = np.matmul(L+L.T, L)
    matrix = [
        [3,-2,1,-2],
        [-2,3,-2,1],
        [1,-2,3,-2],
        [-2,1,-2,3]
    ]
    matrix = np.matrix(matrix)
    eigenvalue, feature = np.linalg.eig(matrix)
    print(eigenvalue)
    print(feature)


# print(get_settle_time2013(0.5, 1.5, 2, 2))
# get_settle_time_equilibrium(0.5, 1.5, 2, 2, 0.5)
# get_eigenvalue_from_matrix(None)
get_eigenvalue_from_matrix()