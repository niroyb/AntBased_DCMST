import re
from os import path
import glob

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
    
    constraint = 3
    
    for filePath in glob.glob('Data/shrd*.txt'):
        nbVertices = getNbVertices(filePath)
        edges = getEdges(filePath, nbVertices)
        print filePath
        print edges