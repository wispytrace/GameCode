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

    return gama


def get_settle_time2013(p, q, alpha, beta):
    
    settle_time = (1/(alpha*(1-p)) + 1/(beta*(q-1)))

    return settle_time


def get_equilibrium_settle(p, q, alpha, beta, m=0.2):

    alpha = 2**((p+1)/2)*alpha*(m**p)
    beta = 2**((q+1)/2)*beta*(m**q)
    
    return p, q, alpha, beta


def get_settle_time_equilibrium(p, q, delta, eta, m):
    
    p_hat = (p+1)/2
    q_hat = (q+1)/2
    alpha = np.power(2, p_hat)*delta*np.power(m, p)
    beta = np.power(2, q_hat)*eta*np.power(m, q)

    print(get_settle_time2013(p_hat, q_hat, alpha, beta))
    print(get_settle_time_2019(p_hat, q_hat, alpha, beta))

def get_eigenvalue_from_matrix(matrix):

    N = len(matrix)
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
    eigenvalue, feature = np.linalg.eig((P+P.T))
    print('eigenvalue:', eigenvalue)
    return eigenvalue

def get_directed_consensus(p, q, alhpa, beta):
    
    matrix = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0]]
    N = len(matrix)
    min_eigenvalue = min(get_eigenvalue_from_matrix(matrix))

    k2 = (alpha/(p+1))**(2*p/(p+1)) + (beta/(q+1))**(2*p/(p+1)) + (2**((q-1)/(q+1)))*((alpha/(p+1))**(2*q/(q+1)))+ (2**((q-1)/(q+1)))*((beta/(q+1))**(2*q/(q+1)))
    k3 = min((alpha**2)*((N*N)**(1-2*p))/k2, (beta**2)*((N*N)**(1-2*q))/k2)
    print(min_eigenvalue, k2, k3)
    
    return 0.5*k3*min_eigenvalue


alpha = 2
beta = 2
p = 0.5
q = 1.5
answer = get_directed_consensus(p, q, alpha, beta)
print(answer)
t1 = get_settle_time2013(2*p/(p+1), 2*q/(q+1), answer, answer)
t2 = get_settle_time_2019(2*p/(p+1), 2*q/(q+1), answer, answer)
print(t1, t2)

p , q, alpha, beta = get_equilibrium_settle(0.5, 1.5, 2, 2)
print(p, q, alpha, beta)

t1 = get_settle_time_2019(p, q, alpha, beta)
t2 = get_settle_time2013(p, q, alpha, beta)

print(t1, t2)