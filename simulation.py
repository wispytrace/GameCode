from graph import Node, Graph
from agent import Agent
from game import Game, FixTime, PreTimeConstrained, PreTime
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



class PrescribeSimulation(GameSimulation):

    def __init__(self):
        super().__init__()
        self.T = 0
    
    def set_T(self,T):
        self.T = T

    def run(self, is_debug=True):
    
        start = time.time()
        
        for i in range(self.epochs):
            t = (self.T / ((np.pi*np.pi)/6)) * (1 / ((i+1)**2))
            t = max(t, 0.0001)
            for node_id, agent in self.graph.nodes.items():
                agent.update(1)

            for node_id, agent in self.graph.nodes.items():               
                if is_debug:
                    agent.record(t)
                agent.flush()
            print(self.graph.nodes['0'].memory['status'])

        end = time.time()
        
        print("time: " ,end-start)

        if is_debug:
            self.show_process()