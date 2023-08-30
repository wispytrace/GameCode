import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import graph

def read_pickles(agent_nums):
    records = []
    for i in range(agent_nums):
        file_path = './records/data_{}.pkl'.format(i)
        with open(file_path, 'rb') as f:
            record = pickle.load(f)
            records.append(record)
    
    return records

def extract_records(records):
    
    status_vector = []
    estimate_vector = []
    agent_nums = len(records)

    for id, record in enumerate(records):
        time = []
        agent_status = []
        agent_estimate = []
        for item in record:
            estimate = []
            time.append(item['time'])
            agent_status.append(item['status_vector'][str(id)][0])
            for i in range(agent_nums):
                estimate.append(item['estimate_vector'][str(i)])
            agent_estimate.append(estimate)

        status_vector.append(agent_status)
        estimate_vector.append(agent_estimate)
    
    return np.array(time), np.array(status_vector), np.array(estimate_vector)


def plot_status_graph(time, status_vector):

    plt.clf()
    colors = list(mcolors.TABLEAU_COLORS.keys())
    for i in range(len(status_vector)):
        plt.plot(time, status_vector[i],
                    color=mcolors.TABLEAU_COLORS[colors[i]], label="player {}'s action".format(i+1))
    
    plt.legend()
    plt.title("Players’ Energy Consumptions")
    plt.xlabel('time/s')
    plt.ylabel('status')
    plt.savefig("./figure/status.jpeg")

def plot_estimation_graph(time, status_vector, estimate_vector, opt_value):

    agent_nums = len(status_vector)
    colors = list(mcolors.TABLEAU_COLORS.keys())
    for i in range(agent_nums):
        plt.clf()
        plt.plot(time, status_vector[i],
                    color=mcolors.TABLEAU_COLORS[colors[i]], label="player {}'s action".format(i+1))
        for j in range(agent_nums):
            plt.plot(time, estimate_vector[j, : , i],
                color=mcolors.TABLEAU_COLORS[colors[(i+j)%(len(colors))]], label="player {}'s  estimation on {}".format(j+1, i+1))
        plt.plot(time, [opt_value[i]]*len(time), '--', label="player {}'s optimal value".format(i+1))

        plt.legend()
        plt.title("Player {}' Action and Its Estimation from Other Players".format(i+1))
        plt.xlabel('time/s')
        plt.ylabel("")
        plt.savefig("./figure/estimation_{}.jpeg".format(i+1))

def plot_error_graph(time, status_vector, opt_value):

    agent_nums = len(status_vector)
    colors = list(mcolors.TABLEAU_COLORS.keys())

    for i in range(agent_nums):
        for j in range(len(status_vector[i])):
            status_vector[i, j] = np.fabs(status_vector[i, j] - opt_value[i])

    for i in range(agent_nums):
        plt.clf()
        plt.plot(time, status_vector[i], color=mcolors.TABLEAU_COLORS[colors[i]])

        # plt.legend()
        plt.title("Absolute Error between Player {}'s action and it's optimal value".format(i+1))
        plt.xlabel('time/s')
        plt.ylabel("|x{} - x{}*|".format(i+1, i+1))
        plt.savefig("./figure/error_{}.jpeg".format(i+1))

if __name__ == '__main__':

    matrix = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0]]
    my_graph = graph.Graph.load_matrix(matrix)
    my_graph.draw_graph()

    opt_value=[26.0990, 31.0459, 36, 40.9505, 45.90]
    records = read_pickles(5)
    time, status_vector, estimate_vector = extract_records(records)
    plot_status_graph(time, status_vector)
    plot_estimation_graph(time, status_vector, estimate_vector, opt_value)
    plot_error_graph(time, status_vector, opt_value)
