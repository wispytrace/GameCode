import numpy as np
from graph import Node

class Game:

    @staticmethod
    def get_memory():
        pass
    
    @staticmethod
    def get_memory_format():
        pass
    
    @staticmethod
    def cost_function(agnet):
        pass

    @staticmethod
    def status_update_function(agent):
        pass

    @staticmethod
    def estimation_update_function(agent):
        pass

    @staticmethod
    def others_update_function(agent):
        pass

class PreTime(Game):


    @staticmethod
    def get_memory(agent, init_memory=None):
        
        memory = {}

        if init_memory is not None:
            for parameter, value in init_memory.items():
                memory[parameter] = value
        
        if 'status'  not in memory.keys():
            memory['status'] = {agent.id: np.zeros(PreTime.get_memory_format()['status'])}

        if 'estimate' not in memory.keys():
            memory['estimate'] = {}
            for id in init_memory['n']:
                memory['estimate'][id] = np.zeros(PreTime.get_memory_format()['estimate'])
        

        return memory
    
    @staticmethod
    def get_memory_format():
        
        memory_format = {}
        memory_format['status'] = 1
        memory_format['estimate'] = 1
        memory_format['alpha'] = 1
        memory_format['k'] = 1
        memory_format['n'] = 1

        memory_format['e1'] = 1
        memory_format['e2'] = 1
        memory_format['v'] = 1

        return memory_format

    @staticmethod
    def cost_function(agent):


        p = [10, 15, 20, 25, 30, 35]
        p_i = p[int(agent.id)]

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
        
        x_i = agent.memory['estimate'][agent.id]

        cost = (x_i - p_i)**2 + x_i*( 0.1*status_sum + 10)
        

        return cost
    

    @staticmethod
    def constrained_cost(agent):

        v = agent.memory['v']

        constrained_sum = -2

        constrained_cost = 0

        for id, status in agent.memory['estimate'].items():

            constrained_sum += v[id] * status
            
        if constrained_sum <= 0:
            constrained_cost = 0
        else:
            constrained_cost -= v[agent.id]
        
        if agent.memory['estimate']['3'] + agent.memory['estimate']['4'] >= 10:
            if agent.id == '3' or agent.id == '4':
                constrained_cost -= 1
        
        constrained_cost *= constrained_cost * agent.memory['alpha']

        return constrained_cost


    @staticmethod
    def partial_cost(agent):
        
        p = [10, 15, 20, 25, 30, 35]
        p_i = p[int(agent.id)]

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
        
        x_i = agent.memory['estimate'][agent.id]

        cost = (x_i - p_i)**2 + x_i*( 0.1*status_sum + 10)

        partial_cost = 2*(x_i - p_i) + (0.1*status_sum + 10) + x_i*1.1
        

        print(partial_cost)
        print(agent.memory['estimate'])
        return partial_cost

    @staticmethod
    def status_update_function(agent):

        
        k = 0.008
        # alpha = agent.memory['alpha']
        alpha = 0
        update_value = -k*PreTime.partial_cost(agent)
        
        return update_value
    

    @staticmethod
    def estimation_update_function(agent):
        

        update_value = {}

        for id in agent.memory['n']:
            update_value[id] = 0


        adj_id = []


        for in_edge in agent.in_edges:
            in_agent = in_edge.start_node
            adj_id.append(in_agent.id)

            for id, value in in_agent.memory['estimate'].items():

                update_value[id] += agent.memory['estimate'][id] - value

            
            update_value[in_agent.id] += agent.memory['estimate'][in_agent.id] - in_agent.memory['status'][in_agent.id]

        for id, value in update_value.items():

            if id in adj_id:
                update_value[id] /= -(len(adj_id) + 1)
            else:
                update_value[id] /= -len(adj_id)
            

        return update_value


        

class PreTimeConstrained(Game):

    
    @staticmethod
    def get_memory(agent, init_memory=None):
        
        memory = {}

        if init_memory is not None:
            for parameter, value in init_memory.items():
                memory[parameter] = value
        
        if 'status'  not in memory.keys():
            memory['status'] = {agent.id: np.zeros(PreTimeConstrained.get_memory_format()['status'])}

        if 'estimate' not in memory.keys():
            memory['estimate'] = {}
            for id in init_memory['n']:
                memory['estimate'][id] = np.zeros(PreTimeConstrained.get_memory_format()['estimate'])
        

        return memory
    
    @staticmethod
    def get_memory_format():
        
        memory_format = {}
        memory_format['status'] = 1
        memory_format['estimate'] = 1
        memory_format['alpha'] = 1
        memory_format['k'] = 1
        memory_format['n'] = 1

        memory_format['e1'] = 1
        memory_format['e2'] = 1
        memory_format['v'] = 1

        return memory_format

    @staticmethod
    def cost_function(agent):

        d1 = 3
        d2 = 0.02
        e1 = agent.memory['e1']
        e2 = agent.memory['e2']
        xi = agent.memory['estimate'][agent.id]

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
        
        Ri = (d1 - d2*status_sum)*xi

        if agent.memory['estimate'][agent.id] <= 1:
            Ti = (e1 + e2*xi)*xi
        else:
            Ti = (2*e1 + e2*xi)*xi - 5*e1
        
        cost = Ri - Ti

        return cost
    

    @staticmethod
    def constrained_cost(agent):

        v = agent.memory['v']

        constrained_sum = -2

        constrained_cost = 0

        for id, status in agent.memory['estimate'].items():

            constrained_sum += v[id] * status
            
        if constrained_sum <= 0:
            constrained_cost = 0
        else:
            constrained_cost -= v[agent.id]
        
        if agent.memory['estimate']['3'] + agent.memory['estimate']['4'] >= 10:
            if agent.id == '3' or agent.id == '4':
                constrained_cost -= 1
        
        constrained_cost *= constrained_cost * agent.memory['alpha']

        return constrained_cost


    @staticmethod
    def partial_cost( agent):
        
        delta = 1e-4
        cost = PreTimeConstrained.cost_function(agent)
        agent.memory['estimate'][agent.id] += delta
        cost_hat = PreTimeConstrained.cost_function(agent)
        agent.memory['estimate'][agent.id] -= delta

        return cost_hat - cost / delta


    @staticmethod
    def status_update_function(agent):

        
        k = 1e-10
        # alpha = agent.memory['alpha']
        alpha = 0
        update_value = -k*PreTimeConstrained.partial_cost(agent) + alpha * PreTimeConstrained.constrained_cost(agent)
        
        # print(update_value)
        return update_value
    

    @staticmethod
    def estimation_update_function(agent):
        

        update_value = {}

        for id in agent.memory['n']:
            update_value[id] = 0


        adj_id = []


        for in_edge in agent.in_edges:
            in_agent = in_edge.start_node
            adj_id.append(in_agent.id)

            for id, value in in_agent.memory['estimate'].items():

                update_value[id] += agent.memory['estimate'][id] - value

            
            update_value[in_agent.id] += agent.memory['estimate'][in_agent.id] - in_agent.memory['status'][in_agent.id]

        for id, value in update_value.items():

            if id in adj_id:
                update_value[id] /= -(len(adj_id) + 1)
            else:
                update_value[id] /= -len(adj_id)
            

        return update_value


        


class FixTime(Game):

    
    @staticmethod
    def get_memory(agent, init_memory=None):
        
        memory = {}
        
        if init_memory is not None:
            for parameter, value in init_memory.items():
                memory[parameter] = value
        
        memory['status'] = {agent.id: np.zeros(FixTime.get_memory_format()['status'])}
        memory['estimate'] = {agent.id: np.zeros(FixTime.get_memory_format()['estimate'])}
        
        return memory

    @staticmethod
    def get_memory_format():
        
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

    @staticmethod
    def cost_function(agent):
        p = 1
        q = 10.5
        s = 1
        f = 10
        
        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
        
        
        cost = p*((agent.memory['estimate'][agent.id]-q)**2) + (s*status_sum + f)* agent.memory['estimate'][agent.id]
        
        return cost
        


    
    @staticmethod
    def cost_function(agent):
        p = 1
        q = 10.5
        s = 1
        f = 10
        
        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
        
        
        cost = p*((agent.memory['estimate'][agent.id]-q)**2) + (s*status_sum + f)* agent.memory['estimate'][agent.id]
        
        return cost
    
    @staticmethod
    def partial_cost(agent):
        

        p = agent.memory['p']
        q = agent.memory['q']
        s = 1
        f = 10
        
        
        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
        
        partial = 2*p*(agent.memory['estimate'][agent.id]-q) + s*status_sum + f + s*agent.memory['estimate'][agent.id]
        
        
        return partial


    @staticmethod
    def status_update_function(agent):
        p = 0.5
        q = 1.5

        delta = agent.memory['delta']
        eta = agent.memory['eta']
        epsilon = agent.memory['epsilon']
        epsilon = 0

        partial_value = FixTime.partial_cost(agent)[0]
        
        sign = None
        if partial_value > 0:
            sign = 1
        else:
            sign = -1
        
        partial_value_fabs = np.fabs(partial_value)
            
    
        update_value = -(sign*delta*np.power(partial_value_fabs, p) + sign*eta*np.power(partial_value_fabs, q) + sign*epsilon*partial_value_fabs)

                    
        return update_value


    @staticmethod
    def estimation_update_function(agent):
        
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
            
            update_value[in_agent.id] += agent.memory['estimate'][in_agent.id] - in_agent.memory['status'][in_agent.id]


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
            
            update_value[id] = -1*sign*(delta*np.power(update_value_fabs, p) + eta*np.power(update_value_fabs, q) +  gama*update_value_fabs)
        
        return update_value
    
    @staticmethod
    def batch_update(graph, time_delta, epochs, is_debug=True):
        
        id_index = {}
        n = len(graph.nodes)
        status_vector = np.zeros(n, FixTime.get_memory_format['status'])
        estimation_vector = np.zeros(n*n, FixTime.get_memory_format['estimate'])
        for i, id in enumerate(graph.nodes.keys()):
            id_index[id] = i

        for id, agent in graph.nodes.items():
            status_vector[id_index[id], 0] = agent.memory['status'][id]
            for agent_id, value in agent.memory['estimate']:
                estimation_vector[id_index[id]*n + id_index[agent_id], 0] = value
        
        laplapian_matrix = graph.export_laplapian_matrix()
        M_matrix = np.zeros(n*n, n*n)
        for i in range(n):
            for j in range(n):
                M_matrix[i*n+j, i*n+j] = laplapian_matrix[i, j]
        
        # for i in range(epochs):
        #     pass
            
            
        
        
        
        

