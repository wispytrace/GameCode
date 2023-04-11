from graph import Node, Graph
from game import Agent, Game, FixTime, PreTimeConstrained
import numpy as np
import matplotlib.pyplot as plt	
import matplotlib.colors as mcolors
import time

class GameSimulation():

    def __init__(self):
        self.graph = None
        self.update_time = None
        self.epochs = None
        
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
            agent.set_game(game_model)
                        
            if paramas is not None and agent.id in paramas:
                memory = game_model.get_memory(agent, paramas[agent.id])
            else:
                memory = game_model.get_memory(agent)
            agent.set_memory(memory)
            
            agents[node_id] = agent
    

        for edge_id, edge in self.graph.edges.items():
            edge.start_node = agents[edge.start_node.id]
            edge.end_node = agents[edge.end_node.id]

        self.graph.nodes = agents
    
    
    def run(self, is_debug=True):
        
        start = time.time()

        for i in range(self.epochs):

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



class PrescribeGame(GameSimulation):

    def __init__(self):
        super().__init__()
        self.T = 0
    
    def set_T(self,T):
        self.T = T

    def run(self, is_debug=True):
    
        start = time.time()
        
        for i in range(self.epochs):
            t = self.T / (np.pi*np.pi/6) * (1/((i+1)**2))
            t = max(t, 1e-4)
            for node_id, agent in self.graph.nodes.items():
                agent.update(1/t)

            for node_id, agent in self.graph.nodes.items():               
                if is_debug:
                    agent.record(t)
                agent.flush()

        end = time.time()
        
        print("time: " ,end-start)

        if is_debug:
            self.show_process()
        


if __name__ == '__main__':
    
    # matrix = [[1,1,1,1],[1, 1, 1,1], [1, 1, 1, 1], [1,1,1,1]]
    # graph = Graph.load_matrix(matrix)
    # # graph.draw_graph()
    # fixed = GameSimulation()
    # fixed.set_graph(graph)
    # fixed.set_update_time(5e-4)
    # paramas = {
    #     '0': {'delta': 4, 'eta': 1, 'gama': 20, 'epsilon': 1, 'p': 1, 'q': 10.5}, 
    #     '1': {'delta': 4, 'eta': 2, 'gama': 20, 'epsilon': 2, 'p': 2, 'q': 5.5}, 
    #     '2': {'delta': 3, 'eta': 1, 'gama': 20,'epsilon': 1, 'p': 1, 'q': 6}, 
    #     '3': {'delta': 6, 'eta': 3, 'gama': 20, 'epsilon': 3, 'p': 2, 'q': 11}
    # }
    # fixed.load_game_model(FixTime, paramas)
    # fixed.set_epochs(5000)
    # fixed.run()

    matrix = [[1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1]]
    graph = Graph.load_matrix(matrix)
    game = PrescribeGame()
    game.set_graph(graph)
    game.set_T(10)
    v = {'0': 0.091, '1': 0.161, '2': 0.221, '3': 0.1, '4':0.242, '5': 0.385}
    n = {'0', '1', '2', '3', '4', '5'}
    paramas = {
        '0': {'e1': 0.56, 'e2': 0.075, 'v': v, 'n': n, 'alpha': 100}, 
        '1': {'e1': 1.37, 'e2': 0.15, 'v': v, 'n': n, 'alpha': 100}, 
        '2': {'e1': 1.75, 'e2': 0.2, 'v': v, 'n': n, 'alpha': 100}, 
        '3': {'e1': 1, 'e2': 0.1, 'v': v, 'n': n, 'alpha': 100}, 
        '4': {'e1': 1.5, 'e2': 0.2, 'v': v, 'n': n, 'alpha': 100}, 
        '5': {'e1': 2, 'e2': 0.3, 'v': v, 'n': n, 'alpha': 100}, 
    }
    game.load_game_model(PreTimeConstrained, paramas)
    game.set_epochs(5000)
    game.run()