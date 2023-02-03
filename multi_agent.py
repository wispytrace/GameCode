from graph import Node, Graph
from game import Agent, Game, FixTime
import numpy as np
import matplotlib.pyplot as plt	
import matplotlib.colors as mcolors

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

    def load_game_model(self, game_model):
        
        agents = {}
        for node_id, node in self.graph.nodes.items():
            agent = Agent(node)
            agent.set_game(game_model)
            agents[node_id] = agent
        
        for edge_id, edge in self.graph.edges.items():
            edge.start_node = agents[edge.start_node.id]
            edge.end_node = agents[edge.end_node.id]

        self.graph.nodes = agents
    
    def run(self, is_debug=True):
    
        for i in range(self.epochs):
            for node_id, agent in self.graph.nodes.items():
                agent.update(self.update_time)

                if is_debug:
                    agent.record(self.update_time)

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
            print(simulate_data[node_id])
            
        for i, node_id in enumerate(simulate_data.keys()):
            plt.plot(simulate_time, simulate_data[node_id], color=mcolors.TABLEAU_COLORS[colors[i]], label=node_id)
                     
        plt.legend()
        plt.xlabel('time/s')
        plt.ylabel('status')
        plt.show()

    


if __name__ == '__main__':
    
    matrix = [[1,1,1,1],[1, 1, 1,1], [1, 1, 1, 1], [1,1,1,1]]
    graph = Graph.load_matrix(matrix)
    graph.draw_graph()
    fixed = GameSimulation()
    fixed.set_graph(graph)
    fixed.set_update_time(0.01)
    fixed.load_game_model(FixTime)
    fixed.set_epochs(100)
    fixed.run()
