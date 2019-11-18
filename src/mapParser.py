import numpy as np
import pandas as pd

class mapParser():

    def __init__(self, mapHandle):
        self.mapHandle = mapHandle
    
    def parseMap(self):
        gridMap = pd.read_csv(self.mapHandle, sep=' ', header=None)
        gridMap = gridMap.dropna(axis=1, how='all')
        rows, cols = {}, {}
        rows['rows'], cols['cols'] = gridMap.shape[0], gridMap.shape[1]
        numAgents, agentLocs = self.parseAgents(gridMap)
        obstacles = self.parseObstacles(gridMap)
        return self.packData(numAgents, agentLocs, obstacles, rows, cols)
    
    def parseAgents(self, gridMap):
        numAgents = {}
        numAgents['numAgents'] = 0
        agentLocs = {}
        agentLocs['agentLocs'] = {}

        rows, cols = gridMap.shape[0], gridMap.shape[1]
        
        for row in range(0, rows):
            for col in range(0, cols):
                if gridMap.iloc[row][col] == 'x':
                    numAgents['numAgents'] += 1
                    agentLocs['agentLocs'][numAgents['numAgents']] = (row, col)
        
        return numAgents, agentLocs
    
    def parseObstacles(self, gridMap):
        blockedCells = {}
        blockedCells['blockedCells'] = []

        rows, cols = gridMap.shape[0], gridMap.shape[1]

        for row in range(0, rows):
            for col in range(0, cols):
                if gridMap.iloc[row][col] == 'T':
                    blockedCells['blockedCells'].append((row, col))
        return blockedCells
    
    def packData(self, *args):
        packedDataDict= {}
        for arg in args:
            for key in arg.keys():
                packedDataDict[key] = arg[key]
        return packedDataDict