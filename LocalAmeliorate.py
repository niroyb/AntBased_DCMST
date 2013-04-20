# -*- coding: utf-8 -*-

import time
import UnionFind

def getEdgesCost(edges):
    '''Returns the cost of a group of edges'''
    return sum(edge[0] for edge in edges)

def printEdgesSol(sol):
    '''Prints the edges in the specified format'''
    edges = []
    #Extraire les vertices
    for _, v1, v2 in sol:
        # Contrainte de v1 < v2 a l'affichage
        if v1 > v2:
            v1, v2 = v2, v1
        edges.append((v1, v2))
    # Trier par v1
    edges.sort()
    # Afficher les edges
    for edge in edges:
        print '{} {}'.format(*edge)
        
def printSolIfBetter(sol, cost, startTime):
    global absoluteMinCost
    if(cost < absoluteMinCost):
        absoluteMinCost = cost
        executionTime = time.clock() - startTime
        print cost, executionTime
        printEdgesSol(sol)
        print ''
    
class ConstrainedKruskall():
    @classmethod
    def getSolution(self, nbVertices, edges, constraint, includedEdges = None):
        edges.sort()
        
        subtrees = UnionFind.UnionFind()
        solution = []
        degrees = [0]*nbVertices
        
        def pick(edge):
            '''Essaye d'ajouter un arc a la solution'''
            _, u, v = edge
            if subtrees[u] != subtrees[v] and \
            degrees[u] < constraint and degrees[v] < constraint:
                degrees[u] += 1
                degrees[v] += 1
                solution.append(edge)
                subtrees.union(u,v)
        
        if includedEdges is not None:
            includedEdges.sort()
            for edge in includedEdges:
                pick(edge)
        
        edges.sort()
        for edge in edges:
            pick(edge)
            
        return solution
