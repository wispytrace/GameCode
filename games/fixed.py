from games.base import Game
import numpy as np


class FixTimeGame(Game):

    def get_memory(self, agent, init_memory=None):

        memory = {}

        if init_memory is not None:
            for parameter, value in init_memory.items():
                memory[parameter] = value

        memory['status'] = {agent.id: np.zeros(
            self.get_memory_format()['status'])}
        memory['estimate'] = {agent.id: np.zeros(
            self.get_memory_format()['estimate'])}

        return memory

    def get_memory_format(self):

        memory_format = {}
        memory_format['status'] = 1
        memory_format['estimate'] = 1
        memory_format['p'] = 1
        memory_format['q'] = 1
        memory_format['delta'] = 1
        memory_format['eta'] = 1
        memory_format['epsilon'] = 1
        memory_format['gama'] = 1

        return memory_format

    def cost_function(self, agent):
        p = 1
        q = 10.5
        s = 1
        f = 10

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status

        cost = p*((agent.memory['estimate'][agent.id]-q)**2) + \
            (s*status_sum + f) * agent.memory['estimate'][agent.id]

        return cost

    def cost_function(self, agent):
        p = 1
        q = 10.5
        s = 1
        f = 10

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status

        cost = p*((agent.memory['estimate'][agent.id]-q)**2) + \
            (s*status_sum + f) * agent.memory['estimate'][agent.id]

        return cost

    def partial_cost(self, agent):

        p = agent.memory['p']
        q = agent.memory['q']
        s = 1
        f = 10

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status

        partial = 2*p*(agent.memory['estimate'][agent.id]-q) + \
            s*status_sum + f + s*agent.memory['estimate'][agent.id]

        return partial

    def status_update_function(self, agent):
        p = 0.5
        q = 1.5

        delta = agent.memory['delta']
        eta = agent.memory['eta']
        epsilon = agent.memory['epsilon']
        epsilon = 0

        partial_value = self.partial_cost(agent)[0]

        sign = None
        if partial_value > 0:
            sign = 1
        else:
            sign = -1

        partial_value_fabs = np.fabs(partial_value)

        update_value = -(sign*delta*np.power(partial_value_fabs, p) + sign *
                         eta*np.power(partial_value_fabs, q) + sign*epsilon*partial_value_fabs)

        return update_value

    def estimation_update_function(self, agent):

        p = 0.5
        q = 1.5

        update_value = {}
        for in_edge in agent.in_edges:
            in_agent = in_edge.start_node
            for id, value in in_agent.memory['estimate'].items():
                if id not in update_value.keys():
                    update_value[id] = 0

                if id in agent.memory['estimate'].keys():
                    update_value[id] += agent.memory['estimate'][id] - value
                else:
                    update_value[id] += -value
                    agent.memory['estimate'][id] = 0

            update_value[in_agent.id] += agent.memory['estimate'][in_agent.id] - \
                in_agent.memory['status'][in_agent.id]

        delta = agent.memory['delta']
        eta = agent.memory['eta']
        gama = agent.memory['gama']

        for id, value in update_value.items():

            update_value_fabs = np.fabs(value)
            sign = None

            if update_value[id] > 0:
                sign = 1
            else:
                sign = -1

            update_value[id] = -1*sign*(delta*np.power(update_value_fabs, p) + eta*np.power(
                update_value_fabs, q) + gama*update_value_fabs)

        return update_value

    # def batch_update(graph, time_delta, epochs, is_debug=True):

    #     id_index = {}
    #     n = len(graph.nodes)
    #     status_vector = np.zeros(n, FixTime.get_memory_format['status'])
    #     estimation_vector = np.zeros(n*n, FixTime.get_memory_format['estimate'])
    #     for i, id in enumerate(graph.nodes.keys()):
    #         id_index[id] = i

    #     for id, agent in graph.nodes.items():
    #         status_vector[id_index[id], 0] = agent.memory['status'][id]
    #         for agent_id, value in agent.memory['estimate']:
    #             estimation_vector[id_index[id]*n + id_index[agent_id], 0] = value

    #     laplapian_matrix = graph.export_laplapian_matrix()
    #     M_matrix = np.zeros(n*n, n*n)
    #     for i in range(n):
    #         for j in range(n):
    #             M_matrix[i*n+j, i*n+j] = laplapian_matrix[i, j]
