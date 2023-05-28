from games.base import Game


#
# PreTimeGameA: Appointed-time Distributed Nash Equilibrium Seeking for Networked Games
# PreConsGameAA: Continuous-Time Penalty Methods for Nash Equilibrium Seeking of a Nonsmooth Generalized Noncooperative Game
# PreConsGameAB: 
#


class PreTimeGameA(Game):

    def get_memory_format(self):

        memory_format = {}
        memory_format['status'] = 1
        memory_format['estimate'] = 1
        memory_format['n'] = 1

        memory_format['k'] = 1

        return memory_format

    def cost_function(self, agent):

        p_i = agent.memory['p']

        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status

        x_i = agent.memory['estimate'][agent.id]

        cost = (x_i - p_i)**2 + x_i*(0.1*status_sum + 10)

        return cost

    # def partial_cost(self, agent):

    #     p_i = agent.memory['p']

    #     status_sum = 0
    #     for id, status in agent.memory['estimate'].items():
    #         status_sum += status

    #     x_i = agent.memory['estimate'][agent.id]

    #     partial_cost = 2*(x_i - p_i) + (0.1*status_sum + 10) + x_i*0.1
        
    #     return partial_cost

    def status_update_function(self, agent):

        k = agent.memory['k']
        update_value = -k*self.partial_cost(agent)

        return update_value

    def estimation_update_function(self, agent):

        update_value = {}

        for id in agent.memory['n']:
            update_value[id] = 0

        adj_id = []

        for in_edge in agent.in_edges:
            in_agent = in_edge.start_node
            adj_id.append(in_agent.id)

            for id, value in in_agent.memory['estimate'].items():

                update_value[id] += agent.memory['estimate'][id] - value

            update_value[in_agent.id] += agent.memory['estimate'][in_agent.id] - \
                in_agent.memory['status'][in_agent.id]

        for id, value in update_value.items():

            if id in adj_id:
                update_value[id] /= -(len(adj_id) + 1)
            else:
                update_value[id] /= -len(adj_id)
    

        return update_value




class PreConsGameAA(PreTimeGameA):

    def get_memory_format(self):

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

    def cost_function(self, agent):

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

        cost = Ti - Ri

        return cost

    
    def l2_constrained_cost(self, agent):

        v = agent.memory['v']

        constrained_sum = -2

        constrained_cost = 0

        for id, status in agent.memory['estimate'].items():

            constrained_sum += v[id] * status

        if constrained_sum <= 0:
            constrained_cost = 0
        else:
            constrained_cost += 2 * constrained_sum * v[agent.id]

        special_sum = agent.memory['estimate']['3'] + agent.memory['estimate']['4'] - 10
        if  special_sum >= 0:
            if agent.id == '3' or agent.id == '4':
                constrained_cost = constrained_cost + 2 * special_sum
        
        if agent.memory['estimate'][agent.id] < 0 :
            constrained_cost = constrained_cost + 2*agent.memory['estimate'][agent.id]
            
        return constrained_cost
    
    def l1_constrained_cost(self, agent):

        v = agent.memory['v']

        constrained_sum = -2

        constrained_cost = 0

        for id, status in agent.memory['estimate'].items():

            constrained_sum += v[id] * status

        if constrained_sum <= 0:
            constrained_cost = 0
        else:
            constrained_cost += v[agent.id]

        if agent.memory['estimate']['3'] + agent.memory['estimate']['4'] > 10:
            if agent.id == '3' or agent.id == '4':
                constrained_cost = constrained_cost + 1
        
        if agent.memory['estimate'][agent.id] < 0 :
            constrained_cost = constrained_cost - 1

        # if constrained_cost > 0:            
        #     print(constrained_cost)
            
        return constrained_cost

    def status_update_function(self, agent):

        k = agent.memory['k']
        alpha = agent.memory['alpha']
        update_value = -k * \
            (self.partial_cost(agent) + alpha * \
            self.l2_constrained_cost(agent))

        return update_value

class PreConsGameAB(PreTimeGameA):
    
    
    
    
    def get_memory_format(self):

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

    def cost_function(self, agent):

        a = agent.memory['a']
        b = agent.memory['b']
        xi = agent.memory['estimate'][agent.id]
        xr = agent.memory['r']
                
        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
            
        Pi = a * status_sum + b
        
        cost = (xi - xr)**2 + xi * Pi

        return cost

    
    def l2_constrained_cost(self, agent):

        u = agent.memory['u']
        l = agent.memory['l']
        c = agent.memory['c']
        xi = agent.memory['estimate'][agent.id]
        
        constrained_cost = 0
        
        status_sum = 0
        for id, status in agent.memory['estimate'].items():
            status_sum += status
            
        if status_sum > c:
            constrained_cost += 2 * (status_sum - c)

        if xi > u:
            constrained_cost += 2 * (xi - u)
        
        if xi < l:
            
            constrained_cost += 2 * (xi - l)
            
        
        return constrained_cost
    
    def status_update_function(self, agent):

        k = agent.memory['k']
        alpha = agent.memory['alpha']
        
        cost1 = self.partial_cost(agent)
        cost2 = self.l2_constrained_cost(agent)
        update_value = -k * \
            (cost1 + alpha * \
            cost2)
        print(cost1, alpha * cost2)

        return update_value