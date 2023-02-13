import math
import cv2 as cv
import numpy as np

class Node:
    
    def __init__(self) -> None:
        self.id = None
        self.in_edges = []
        self.out_edges = []
    
    # def bind_agent(self, agent):
        
    #     agent.id = self.id
    #     self.agent = agent
        

    def set_id(self, id):
        self.id = str(id)

    def add_in_edge(self, edge):
        self.in_edges.append(edge)
    
    def add_out_edge(self, edge):
        self.out_edges.append(edge)

class Edge:
    
    def __init__(self) -> None:
        
        self.start_node = None
        self.end_node = None
        self.id = None
        self.weight = 1
    
    def set_start_end(self, start_node, end_node):
        self.start_node =  start_node
        self.end_node = end_node
        self.id = start_node.id + "->" + end_node.id
    
    
    def set_weight(self, weight):
        self.weight = weight
    


class Graph:

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}
    
    def add_node(self, node):

        self.nodes[node.id] = node

    def add_edge(self, edge):

        self.edges[edge.id] = edge

    def get_node(self, id):

        return self.nodes[str(id)]
    
    def get_edge(self, id):

        return self.edges[str(id)]

    @staticmethod
    def load_matrix(matrix):

        n = len(matrix)
        graph = Graph()
        for i in range(n):
            node = Node()
            node.set_id(i)
            graph.add_node(node)
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if matrix[i][j] > 0:
                    edge = Edge()
                    edge.set_start_end(graph.get_node(j), graph.get_node(i))
                    edge.set_weight(matrix[i][j])
                    graph.get_node(i).add_in_edge(edge)
                    graph.get_node(j).add_out_edge(edge)
                    graph.add_edge(edge)

        return graph

    def export_matrix(self):

        n = len(self.nodes)
        matrix = np.zeros((n,n))
        id_index = {}

        for i, id in enumerate(self.nodes.keys()):
            id_index[id] = i

        for id, node in self.nodes.items():
            matrix[id_index[id]][id_index[id]] = 1
            for edge in node.in_edges:
                matrix[id_index[id]][id_index[edge.start_node.id]] = edge.weight

        return matrix


    def draw_graph(self):

        height = 600
        width = 800
        radius = 150
        circle_radius = 30
        text_color = (0,0,0)
        circle_color = (0, 0, 0)
        arrow_color = (0, 0, 0)
        nodes_position = {}

        n = len(self.nodes)

        count = 0
        for id, node in self.nodes.items():
            x = int(radius * math.sin(count*(2*math.pi/n)) + width / 2)
            y = int(radius * math.cos(count*(2*math.pi/n)) + height / 2)
            count += 1
            nodes_position[id] = (x, y)



        img=np.ones((height,width,3),np.uint8) * 255
        for id, pos in nodes_position.items():
            cv.circle(img,pos,circle_radius,circle_color,2)
            cv.putText(img, id, (pos[0]-5,pos[1]+5), cv.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)

        for node_id, node in self.nodes.items():
            in_pos = nodes_position[node_id]
            for in_edge in node.in_edges:
                out_pos = nodes_position[in_edge.start_node.id]
                distance = np.sqrt((out_pos[1] - in_pos[1])**2 + (out_pos[0] - in_pos[0])**2)
                direction = (in_pos[0] - out_pos[0] ,in_pos[1] - out_pos[1])
                ratio = circle_radius / distance
                arrow_start = (int(direction[0] * ratio + out_pos[0]), int(direction[1] * ratio + out_pos[1]))
                arrow_end = (int(direction[0] * (1-ratio) + out_pos[0]), int(direction[1] * (1-ratio) + out_pos[1]))

                cv.arrowedLine(img, arrow_start, arrow_end, arrow_color, 2)

        cv.imshow('graph',img)
        cv.waitKey(0)


if __name__ == '__main__':
    
    matrix = [[1,1,0,1, 0],[1, 1, 1,0, 0], [1, 0, 1, 0, 1], [0,1,1,1, 0], [0, 1, 0, 1, 1]]
    # a = A()
    # b = B(a)
    # b.x = 20
    # b.x = 20
    # b.x = 20
    # b.b = 30

    # print(a.x, b.b. a.b)
    print (type(b), b.a, b.b)

    graph = Graph.load_matrix(matrix)
    print(graph.export_matrix())
    graph.draw_graph()

            
