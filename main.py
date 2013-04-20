import re
from os import path
import glob
from AB_DCMST import AB_DCMST, getTreeCost

def getNbVertices(filePath):
    '''Extract number of vertices from file name'''
    fileName = path.basename(filePath)
    fNameNb = re.search('([0-9]+)', fileName).group(0)
    nbVertices = int(fNameNb[:-1])
    return nbVertices

def getEdges(filePath, nbVertices):
    '''Extract edges from file content'''
    fileContent = open(filePath).read()
    lines = fileContent.splitlines()
    numbers = [int(nb) for line in lines for nb in line.split()]
    
    # Generate edges
    edges = []
    nbIndex = 0
    for i in xrange(nbVertices):
        for j in xrange(i):
            edges.append((numbers[nbIndex], i, j))
            nbIndex += 1
    return edges

if __name__ == '__main__':

    for filePath in glob.glob('Data/shrd*.txt'):
        print filePath
        nbVertices = getNbVertices(filePath)
        edges = getEdges(filePath, nbVertices)
        #print 'Vertices :', nbVertices, 'Edges :', len(edges)
        
        antBasedSolver = AB_DCMST(edges)
        for constraint in xrange(3, 6):
            tree = antBasedSolver.getSolution(constraint)
            print '{}\t{}'.format(constraint, getTreeCost(tree))
        #print