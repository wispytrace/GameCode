import numpy as np
from graph import Node
from copy import deepcopy

class Game:

    @staticmethod
    def get_data_shape():
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

class Agent(object):

    def __init__(self, node):
        self.status_vector = {}
        self.estimate_vector = {}
        self.others_vector = {}
        
        self.status_vector_updated = {}
        self.estimate_vector_updated = {}
        self.others_vector_updated = {}
        
        self.game = None
        self.super_parameter = {}
        
        self.__node = node

        self.records = []
    
    def set_game(self, game):
        
        self.game = game
        self.status_shape, self.estimate_shape, self.others_shape = self.game.get_data_shape()
        self.status_vector[self.id] = np.zeros(self.status_shape)
        self.estimate_vector[self.id] = np.zeros(self.estimate_shape)
        self.others_vector[self.id] = np.zeros(self.others_shape)

    def update(self, time_delta=1e-4):
        
        self.status_vector_updated = deepcopy(self.status_vector)
        self.estimate_vector_updated = deepcopy(self.estimate_vector)
        self.others_vector_updated = deepcopy(self.others_vector)
        
        self.status_vector_updated[self.id] += self.game.status_update_function(self) * time_delta
        self.others_vector_updated[self.id] += self.game.others_update_function(self) * time_delta
        
        esitimate_update = self.game.estimation_update_function(self)
        for id, value in esitimate_update.items():
            if id not in self.estimate_vector_updated.keys():
                self.estimate_vector_updated[id] = np.zeros(self.estimate_shape)
            self.estimate_vector_updated[id] += value * time_delta
                    
    def flush(self):
        
        self.status_vector = self.status_vector_updated
        self.estimate_vector = self.estimate_vector_updated
        self.others_vector = self.others_vector_updated
    
    
    def record(self, time_delta=0.1):

        current_record = {}
        
        if len(self.records) == 0:
            current_record['time'] = 0
        else:
            current_record['time'] = time_delta + self.records[-1]['time']
        current_record['status_vector'] = deepcopy(self.status_vector)
        current_record['estimate_vector'] = deepcopy(self.estimate_vector)
        current_record['others_vector'] = deepcopy(self.others_vector)

        self.records.append(current_record)

    def __getattr__(self, attr): # 当在 Proxy 类中搜索不到对应的属性或方法时（调用 __getattribute__ 方法 便会调用 __getattr__ 方法，此时则利用 getattr() 函数获取代理对象的对应方法再返回即可。
        return getattr(self.__node, attr)

    # def __setattr__(self, attr, val):

    #     if attr == '_Agent__node':      # __x 会变成私有变量，即_x_xx 就可以巧妙避免命名重复
    #         object.__setattr__(self, attr, val)
    #     else:
    #         return setattr(self.__node, attr, val)


class FixTime(Game):

    
    
    
    
    @staticmethod
    def get_data_shape():
        
        status_vetcor_shape = 1
        estimate_vector_shape = 1
        other_vector_shape = 1

        return status_vetcor_shape, estimate_vector_shape, other_vector_shape

    @staticmethod
    def set_agent_parameter(agent, param):
        agent.super_parameter = param
    
    
    @staticmethod
    def cost_function(agent):
        p = 1
        q = 10.5
        s = 1
        f = 10
        
        status_sum = 0
        for id, status in agent.estimate_vector.items():
            status_sum += status
        
        
        cost = p*((agent.estimate_vector[agent.id]-q)**2) + (s*status_sum + f)* agent.estimate_vector[agent.id]
        
        # return (agent.estimate_vector[agent.id]-q)**2
        return cost
    
    @staticmethod
    def partial_cost(agent):
        
        # delta = 1e-4
        # cost = FixTime.cost_function(agent)
        # agent.estimate_vector[agent.id] += delta
        # cost_hat = FixTime.cost_function(agent)
        # agent.estimate_vector[agent.id] -= delta

        # partial = (cost_hat - cost) / delta
        p = agent.super_parameter['p']
        q = agent.super_parameter['q']
        s = 1
        f = 10
        
        
        status_sum = 0
        for id, status in agent.estimate_vector.items():
            status_sum += status
        
        partial = 2*p*(agent.estimate_vector[agent.id]-q) + s*status_sum + f + s*agent.estimate_vector[agent.id]
        
        
        return partial


    @staticmethod
    def status_update_function(agent):
        p = 0.5
        q = 1.5

        delta = agent.super_parameter['delta']
        eta = agent.super_parameter['eta']
        epsilon = agent.super_parameter['epsilon']
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
            for id, value in in_agent.estimate_vector.items():
                if id not in update_value.keys():
                    update_value[id] = 0

                if id in agent.estimate_vector.keys():
                    update_value[id] += agent.estimate_vector[id] - value
                else:
                    update_value[id] += -value
                    agent.estimate_vector[id] = 0
            
            update_value[in_agent.id] += agent.estimate_vector[in_agent.id] - in_agent.status_vector[in_agent.id]


        delta = agent.super_parameter['delta']
        eta = agent.super_parameter['eta']
        gama = agent.super_parameter['gama']
        
                   
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
    def others_update_function(agent):
        
        return 0 

    
    
