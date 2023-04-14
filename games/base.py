import numpy as np


class Game:

    def __init__(self) -> None:
        pass

    def get_memory(self, agent, init_memory=None):

        memory = {}

        if init_memory is not None:
            for parameter, value in init_memory.items():
                memory[parameter] = value

        if 'status' not in memory.keys():
            memory['status'] = {agent.id: np.zeros(
                self.get_memory_format()['status'])}

        if 'estimate' not in memory.keys():
            memory['estimate'] = {}
            for id in init_memory['n']:
                memory['estimate'][id] = np.zeros(
                    self.get_memory_format()['estimate'])

        return memory

    def get_memory_format(self):
        pass

    def cost_function(self, agnet):
        pass
    
    def partial_cost(self, agent):
        
        delta = 1e-8
        cost = self.cost_function(agent)
        agent.memory['estimate'][agent.id] += delta
        cost_hat = self.cost_function(agent)
        agent.memory['estimate'][agent.id] -= delta
        
        return (cost_hat - cost) / delta
    
    def status_update_function(self, agent):
        pass

    def estimation_update_function(self, agent):

        update_value = {}

        for id in agent.memory['n']:
            update_value[id] = 0

        for in_edge in agent.in_edges:
            in_agent = in_edge.start_node

            for id, value in in_agent.memory['estimate'].items():

                update_value[id] += agent.memory['estimate'][id] - value

            update_value[in_agent.id] += agent.memory['estimate'][in_agent.id] - \
                in_agent.memory['status'][in_agent.id]

        return update_value


    def others_update_function(self, agent):
        pass
    
    
