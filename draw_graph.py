import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import graph
import os
import copy

charater = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']

figure_base_dir = "./output/figures/"
result_base_dir = "./output/results/"
compared_dir = "./output/compared/"

def make_nessary_folder(index=0):
    figure_dir = figure_base_dir + "{}_figure".format(index)
    result_dir = result_base_dir + "{}_result".format(index)
    os.makedirs(figure_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)
    
    return figure_dir, result_dir


def read_pickles(index, agent_nums):
    records = []
    for i in range(agent_nums):
        file_path = './records/{}_data_{}.pkl'.format(index, i)
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
            # if item['time'] > 2.25:
            #     continue
            estimate = []
            time.append(item['time'])

            agent_status.append(item['status_vector'][str(id)][0])
            for i in range(agent_nums):
                estimate.append(item['estimate_vector'][str(i)])
            agent_estimate.append(estimate)

        status_vector.append(agent_status)
        estimate_vector.append(agent_estimate)
    
    return np.array(time), np.array(status_vector), np.array(estimate_vector)

def get_settle_result(time, optimal_value, status_vector, abs_error, result_dir):

    with open(result_dir + '/results.txt', 'w') as f:
        for i in range(len(status_vector)): 
            value = optimal_value[i]
            value_low = value * (1 - abs_error)
            value_high = value * (1 + abs_error)
            time_high = [0]
            time_low = [0]
        
            for j in range(len(status_vector[i])-1):
                if (value_low - status_vector[i][j]) * (value_low - status_vector[i][j+1]) <= 0:
                    time_low.append(time[j])
                if (value_high - status_vector[i][j]) * (value_high - status_vector[i][j+1]) <= 0:
                    time_high.append(time[j])


            f.write("player {}:\n".format(i))
            f.write("final results:" + str(status_vector[i][-1])+"\n")
            f.write("max_time_low: {}\n".format(max(time_low)))
            f.write("max_time_high: {}\n".format(max(time_high)))
            f.flush()

def plot_status_graph(time, status_vector, opt_value, figure_dir):

    plt.clf()

    colors = list(mcolors.TABLEAU_COLORS.keys())
    for i in range(len(status_vector)):
        plt.plot(time, status_vector[i],
                    color=mcolors.TABLEAU_COLORS[colors[i]], label="x{}".format(charater[i+1]))
        plt.plot(time, [opt_value[i]]*len(time), '--', color="black")

    plt.legend(loc='lower left', bbox_to_anchor=(0.85, 0))
    plt.xlim(0, 1.5)
    plt.ylim(0, max(opt_value)+10)
    
    plt.xlabel('time(sec)')
    plt.ylabel('Action')
    plt.savefig(figure_dir + "/status.jpeg")
    

def plot_estimation_graph(time, status_vector, estimate_vector, opt_value, figure_dir):

    agent_nums = len(status_vector)
    colors = list(mcolors.TABLEAU_COLORS.keys())
    for i in range(agent_nums):
        plt.clf()
        plt.plot(time, status_vector[i],
                    color=mcolors.TABLEAU_COLORS[colors[i]], label="x {}".format(charater[i+1]))
        for j in range(agent_nums):
            plt.plot(time, estimate_vector[j, : , i],
                color=mcolors.TABLEAU_COLORS[colors[(i+j)%(len(colors))]], label="z{}{}".format(charater[j+1], charater[i+1]))
        plt.plot(time, [opt_value[i]]*len(time), '--', label="x{}*".format(charater[i+1]))
        plt.annotate(str(opt_value[i]), xy=(1.5, opt_value[i]), xytext=(1.75, opt_value[i]+4),arrowprops=dict(arrowstyle="->", facecolor='blue', edgecolor='blue'))
        plt.legend()
        plt.xlabel('time(sec)')
        plt.ylim(0, opt_value[i]+10)
        plt.ylabel("x{} and its estimates from other players".format(charater[i+1]))
        plt.savefig(figure_dir+"/estimation_{}.jpeg".format(i+1))

def plot_error_graph(time, status_vector, opt_value, figure_dir):

    agent_nums = len(status_vector)
    colors = list(mcolors.TABLEAU_COLORS.keys())
    estimation_error = copy.deepcopy(status_vector)
    for i in range(agent_nums):
        for j in range(len(status_vector[i])):
            estimation_error[i, j] = np.fabs(status_vector[i, j] - opt_value[i])

    for i in range(agent_nums):
        plt.clf()
        plt.plot(time, estimation_error[i], color=mcolors.TABLEAU_COLORS[colors[i]])

        # plt.legend()
        # plt.title("Absolute Error between Player {}'s action and it's optimal value".format(i+1))
        plt.plot(time, [0]*len(time), '--', color="black")
        plt.xlabel('time(sec)')
        plt.ylabel("|x{} - x{}*|".format(charater[i+1], charater[i+1]))
        plt.savefig(figure_dir + "/error_{}.jpeg".format(i+1))

def plot_assemble_error_graph(time, status_vector, opt_value, figure_dir):
    plt.clf()
    agent_nums = len(status_vector)
    colors = list(mcolors.TABLEAU_COLORS.keys())
    estimation_error = copy.deepcopy(status_vector)
    for i in range(agent_nums):
        for j in range(len(status_vector[i])):
            estimation_error[i, j] = status_vector[i, j] - opt_value[i]

    for i in range(agent_nums):
        plt.plot(time, estimation_error[i], color=mcolors.TABLEAU_COLORS[colors[i]], label=("|x{} - x{}*|".format(charater[i+1], charater[i+1])))
        plt.legend(loc='lower left', bbox_to_anchor=(0.75, 0))
        plt.xlabel('time(sec)')
        plt.xlim(left=0, right=1.5)
        plt.ylabel("Error between Player's Action and Nash Equilibrium".format(charater[i+1], charater[i+1]))
        plt.savefig(figure_dir + "/assemble_error.jpeg")
    

def plot_assembl_estimate_graph(time, status_vector, estimate_vector, opt_value, figure_dir):
    plt.clf()
    agent_nums = len(status_vector)
    colors = list(mcolors.TABLEAU_COLORS.keys())
    estimate_error = copy.deepcopy(estimate_vector)
    for i in range(agent_nums):
        for j in range(agent_nums):
            for k in range(len(time)):
                estimate_error[j, k, i] = estimate_vector[j, k, i] - status_vector[i, k]

    for i in range(agent_nums):
        for j in range(agent_nums):
            plt.plot(time, estimate_error[j, :, i],
                color=mcolors.TABLEAU_COLORS[colors[(i+j)%(len(colors))]], label="z{}{} - x{}".format(charater[j+1], charater[i+1],  charater[i+1]))
            plt.legend(loc='lower left', bbox_to_anchor=(0.51, 0), ncol=3, prop={'size': 7, 'weight': 'bold'})

    plt.xlabel('time(sec)')
    plt.xlim(0, 1.5)
    plt.ylabel("Error between Player's Action and Estimation from Others".format(charater[i+1]))
    plt.savefig(figure_dir+"/assemble_estimation.jpeg".format(i+1))

def plt_algoritmn_graph(index, opt_value):
    records = read_pickles(index, len(matrix))
    figure_dir, result_dir = make_nessary_folder(index)
    time, status_vector, estimate_vector = extract_records(records)
    plot_status_graph(time, status_vector, opt_value, figure_dir)
    # plot_estimation_graph(time, status_vector, estimate_vector, opt_value, figure_dir)
    # plot_error_graph(time, status_vector, opt_value, figure_dir)
    plot_assemble_error_graph(time, status_vector, opt_value, figure_dir)
    plot_assembl_estimate_graph(time, status_vector, estimate_vector, opt_value, figure_dir)
    # get_settle_result(time, opt_value, status_vector, abs_error, result_dir)


def plot_compared_graph(labels, opt_value, matrix, margin=0.7):
    plt.clf()
    colors = list(mcolors.TABLEAU_COLORS.keys())
    for key in labels.keys():
        index = int(key)
        records = read_pickles(index, len(matrix))
        time, status_vector, _ = extract_records(records)
        norm_error = copy.deepcopy(time)
        for i in range(len(norm_error)):
            norm_error[i] = np.linalg.norm(status_vector[:,i] - opt_value)
        plt.plot(time, norm_error, color=mcolors.TABLEAU_COLORS[colors[index%(len(colors))]], label=labels[key])
    plt.legend(loc='lower left', bbox_to_anchor=(margin, 0))
    plt.xlim(0, 1.5)
    plt.ylim(bottom=0)
    plt.xlabel('time(sec)')
    plt.ylabel("||x - x*||")
    plt.savefig(compared_dir+"/compared_{}.jpeg".format(str(labels)[:10]))





if __name__ == '__main__':

    matrix = [[1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [0, 1, 1, 1, 1], [1, 1, 1, 1, 0], [1, 1, 0, 1, 1]]
    my_graph = graph.Graph.load_matrix(matrix)
    my_graph.draw_graph()
    abs_error = 0.002
    opt_value=[26.0990, 31.0459, 36.0000, 40.9505, 45.9000]
    # plt_algoritmn_graph(11, opt_value)
    # labels = {"11": "Algorithms (12) ", "17": "C. Sun and G. Hu,\n et al. 2020"}
    # plot_compared_graph(labels, opt_value, matrix, margin=0.60)
    labels = {"11": "A", "12": "B", "13": "C", "14": "D", "7": "E"}
    plot_compared_graph(labels, opt_value, matrix, margin=0.85)

  