from graph import Node, Graph
from game import Agent, Game, FixTime
import numpy as np
import matplotlib.pyplot as plt	
import matplotlib.colors as mcolors
from concurrent import futures
import time

class GameSimulation():

    def __init__(self):
        self.graph = None
        self.update_time = None
        self.epochs = None
        self.max_works = 16
        
        self.summary = None
        
    def set_graph(self, graph):
        self.graph = graph
        
    def set_epochs(self, epochs):
        self.epochs = epochs

    def set_update_time(self, time_delta):
        self.update_time = time_delta  

    def load_game_model(self, game_model, paramas=None):
        
        agents = {}
        for node_id, node in self.graph.nodes.items():
            agent = Agent(node)
            
            if paramas is not None:
                FixTime.set_agent_parameter(agent, paramas[agent.id])
            
            agent.set_game(game_model)
            agents[node_id] = agent
    

        for edge_id, edge in self.graph.edges.items():
            edge.start_node = agents[edge.start_node.id]
            edge.end_node = agents[edge.end_node.id]

        self.graph.nodes = agents
    
    
    def run(self, is_debug=True):
        
        start = time.time()
        agent_list = [agent for agent in self.graph.nodes.values()]
        update_function = getattr(Agent, 'update')
        # print((agent_list[0], self.update_time))
        for i in range(self.epochs):
            
            # with futures.ThreadPoolExecutor(min(len(agent_list), self.max_works)) as executor:
            #     res = executor.map(update_function, agent_list, [self.update_time]*len(agent_list))
            for node_id, agent in self.graph.nodes.items():
                agent.update(self.update_time)

               
            for node_id, agent in self.graph.nodes.items():
                
                if is_debug:
                    agent.record(self.update_time)
                agent.flush()

        end = time.time()
        
        print("time: " ,end-start)

        if is_debug:
            self.show_process()
        
    def show_process(self):
        
        simulate_time = []
        simulate_data = {}

        colors=list(mcolors.TABLEAU_COLORS.keys())
        for node_id, agent in self.graph.nodes.items():
            simulate_data[node_id] = []
            simulate_time = []

            for record in agent.records:
                simulate_data[node_id].append(record['status_vector'][node_id][0])
                simulate_time.append(record['time'])
            
        for i, node_id in enumerate(simulate_data.keys()):
            plt.plot(simulate_time, simulate_data[node_id], color=mcolors.TABLEAU_COLORS[colors[i]], label=node_id)
                     
        plt.legend()
        plt.xlabel('time/s')
        plt.ylabel('status')
        plt.show()

    


if __name__ == '__main__':
    
    matrix = [[1,1,1,1],[1, 1, 1,1], [1, 1, 1, 1], [1,1,1,1]]
    graph = Graph.load_matrix(matrix)
    # graph.draw_graph()
    fixed = GameSimulation()
    fixed.set_graph(graph)
    fixed.set_update_time(5e-4)
    paramas = {
        '0': {'delta': 4, 'eta': 1, 'gama': 20, 'epsilon': 1, 'p': 1, 'q': 10.5}, 
        '1': {'delta': 4, 'eta': 2, 'gama': 20, 'epsilon': 2, 'p': 2, 'q': 5.5}, 
        '2': {'delta': 3, 'eta': 1, 'gama': 20,'epsilon': 1, 'p': 1, 'q': 6}, 
        '3': {'delta': 6, 'eta': 3, 'gama': 20, 'epsilon': 3, 'p': 2, 'q': 11}
    }
    fixed.load_game_model(FixTime, paramas)
    fixed.set_epochs(15000)
    fixed.run()
