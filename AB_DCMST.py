#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import division
from collections import defaultdict
from UnionFind import UnionFind
import random

class EdgeInfo:
    def __init__(self, cost, u, v, initialPheromone):
        self.cost = cost
        self.u = u #vertice 1
        self.v = v #vertice 2 #TODO watch out for vertice order dependent bugs
        self.initialPheromone = initialPheromone  # Initial Level
        self.pheromoneLevel = initialPheromone  # Current level
        self.updates = 0
        
    def __repr__(self):
        return 'EdgeInfo(cost={:.1f}, ip={:.1f}, l={:.1f}, u={})'.format(self.cost,
                self.initialPheromone, self.pheromoneLevel, self.updates)

class Ant:
    def __init__(self, initialVertice):
        self.position = initialVertice
        self.visited = set()

    def __repr__(self):
        return 'Ant({}, {})'.format(self.position, self.visited)
    
class AB_DCMST:
    maxCycles = 10000  # Maximum allowed cycles
    s = 75  # Steps: number of edges an ant traverses each cycle
    H = 0.5  # Initial pheromone evaporation factor
    Y = 1.5  # Initial pheromone enhancement factor
    DH = 0.95  # Update constant applied to η
    DY = 1.05  # Update constant applied to γ
    updateCycles = 500  # Number of cycles between updating η and γ
    updateSteps = s / 3  # Number of steps between applying pheromone updates
    escapeCycles = 100  # Number of cycles without improvement before escaping
    stopCycles = 2500  # Number of cycles without improvement before stopping
    
    def __init__(self, edges, d):
        
        self.edges = edges
        
        # Edge data
        edges.sort()
        self.m = float(edges[ 0][0])  # min edge cost
        self.M = float(edges[-1][0])  # max edge cost
        costDiff = self.M - self.m
        self.minP = costDiff / 3.0  # max pheromone level
        self.maxP = 1000.0 * (costDiff + self.minP)  # min pheromone level
        
        self.d = d  # degree constraint
        
        self.graph = defaultdict(dict)
        '''Sets the associated edge data'''
        self.edgeInfos = []
        for cost, u, v in self.edges:
            cost = float(cost)
            initialPheromone = (self.M - cost) + self.minP
            ei = EdgeInfo(cost, u, v, initialPheromone)
            # To get info from two vertices easily
            self.graph[u][v] = ei
            self.graph[v][u] = ei
            # To iterate easily
            self.edgeInfos.append(ei)
        
        self.ants = [Ant(i) for i in self.graph.keys()]
        self.n = len(self.ants)  # Number of vertices
        self.nCandiates = 5 * self.n  # Candidate set size
        
    
    # the sum Could be calculated after each pheromone update
    def getNextVertice(self, startVertice):
        '''Returns a neighbour vertice according to probability of pheromone levels'''
        neighbourPheromes = (ei.pheromoneLevel for ei in self.graph[startVertice].values())
        pheromoneSum = sum(neighbourPheromes)
        target = random.uniform(0.0, pheromoneSum)
        pheromoneSum = 0.0
        for v2, ei in self.graph[startVertice].items():
            pheromoneSum += ei.pheromoneLevel
            if pheromoneSum >= target:
                return v2
        # return v2
        raise Exception("Shouldn't get here")
    
    def moveAnt(self, ant):
        '''Move an ant'''
        nAttempts = 0
        i = ant.position
        while nAttempts < 5:
            # select an edge (i, j) at random and proportional to its pheromone level
            j = self.getNextVertice(i)
            if j not in ant.visited:
                # mark edge (i, j) for pheromone update
                self.graph[i][j].updates += 1
                # move ant to vertex j
                ant.position = j
                # mark j visited
                ant.visited.add(j)
                break
            else:
                nAttempts += 1
    
    def updatePheromone(self):
        for _, u, v in self.edges:
            ei = self.graph[u][v]
            ei.pheromoneLevel = (1 - self.H) * ei.pheromoneLevel + \
                                ei.updates * ei.initialPheromone
            if ei.pheromoneLevel > self.maxP:
                ei.pheromoneLevel = self.maxP - ei.initialPheromone
            if ei.pheromoneLevel < self.minP:
                ei.pheromoneLevel = self.minP + ei.initialPheromone
            # TODO do not forget to clear ei.updates
    
    def getTree(self):
        self.edgeInfos.sort(key=lambda ei: ei.pheromoneLevel, reverse=True)
            
        subtrees = UnionFind()
        solution = []
        degrees = defaultdict(int)
        
        for ei in self.edgeInfos:
            u, v = ei.u, ei.v
            '''Essaye d'ajouter un arc a la solution'''
            if subtrees[u] != subtrees[v] and \
            degrees[u] < self.d and degrees[v] < self.d: #Check constraint
                solution.append(ei)
                if len(solution) == self.n - 1:
                    break
                degrees[u] += 1
                degrees[v] += 1
                subtrees.union(u,v)
            
        return solution

    '''    
    def getSolution(self):
        #Initialization State
        assign one ant to each vertex of the graph
        initialize pheromone level of each edge
        B ←− ∅ # best tree
        cost(B) ←− ∞
        while stopping criteria not met
            # Exploration Stage
            for step = 1 to s
                if step = s/3 or step = 2s/3
                    update pheromone levels for all edges
                end-if
                for each ant a
                    move a along one edge

            update pheromone levels for all edges
            # Tree Construction Stage
            while |T| = n−1
                identify a set C of candidate edges
                using pheromone levels
                construct degree-constrained spanning tree T from C

            if cost(T) < cost(B)
                B ←− T

            enhance pheromone levels for edges in the best tree B
            if no improvement in 100 cycles
                evaporate pheromone from edges of the best tree B


        return the best tree found B
        '''

if __name__ == '__main__':
    
    edges = [(4, 1, 0), (3, 2, 0), (31, 2, 1), (11, 3, 0), (38, 3, 1),
             (44, 3, 2), (16, 4, 0), (34, 4, 1), (54, 4, 2), (68, 4, 3),
             (14, 5, 0), (22, 5, 1), (51, 5, 2), (76, 5, 3), (92, 5, 4),
             (14, 6, 0), (37, 6, 1), (47, 6, 2), (71, 6, 3), (90, 6, 4),
             (118, 6, 5), (4, 7, 0), (25, 7, 1), (56, 7, 2), (76, 7, 3),
             (85, 7, 4), (117, 7, 5), (128, 7, 6), (12, 8, 0), (29, 8, 1),
             (57, 8, 2), (68, 8, 3), (89, 8, 4), (118, 8, 5), (122, 8, 6),
             (144, 8, 7), (16, 9, 0), (37, 9, 1), (43, 9, 2), (71, 9, 3),
             (93, 9, 4), (110, 9, 5), (135, 9, 6), (141, 9, 7), (169, 9, 8),
             (14, 10, 0), (31, 10, 1), (52, 10, 2), (75, 10, 3), (89, 10, 4),
             (113, 10, 5), (122, 10, 6), (152, 10, 7), (178, 10, 8), (186, 10, 9),
             (18, 11, 0), (22, 11, 1), (47, 11, 2), (61, 11, 3), (84, 11, 4),
             (116, 11, 5), (125, 11, 6), (146, 11, 7), (170, 11, 8), (183, 11, 9),
             (203, 11, 10), (16, 12, 0), (21, 12, 1), (42, 12, 2), (73, 12, 3),
             (81, 12, 4), (115, 12, 5), (123, 12, 6), (146, 12, 7), (164, 12, 8),
             (186, 12, 9), (217, 12, 10), (233, 12, 11), (15, 13, 0), (32, 13, 1),
             (42, 13, 2), (65, 13, 3), (84, 13, 4), (104, 13, 5), (121, 13, 6),
             (149, 13, 7), (176, 13, 8), (191, 13, 9), (208, 13, 10),
             (237, 13, 11), (243, 13, 12), (7, 14, 0), (36, 14, 1), (52, 14, 2),
             (68, 14, 3), (88, 14, 4), (118, 14, 5), (123, 14, 6), (147, 14, 7),
             (172, 14, 8), (190, 14, 9), (202, 14, 10), (228, 14, 11), (247, 14, 12),
             (271, 14, 13)]

    c = 3
    abDCMST = AB_DCMST(edges, c)
    for _ in xrange(100):
        print abDCMST.getNextVertice(0)
        
    print abDCMST.ants
    for ant in abDCMST.ants:
        abDCMST.moveAnt(ant)
    print abDCMST.ants
    
    def printEI():
        for ei in abDCMST.edgeInfos:
            print ei
    printEI()
    print
    abDCMST.updatePheromone()
    printEI()
    print
    
    print abDCMST.getTree()
    
