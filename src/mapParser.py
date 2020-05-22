import numpy as np
import pandas as pd

class mapParser():

    def __init__(self, mapHandle, parseTargets):
        self.mapHandle = mapHandle
        self.parseTargets = parseTargets
    
    def parseMap(self):
        gridMap = pd.read_csv(self.mapHandle, sep=' ', header=None)
        gridMap = gridMap.dropna(axis=1, how='all')
        rows, cols = {}, {}
        rows['rows'], cols['cols'] = gridMap.shape[0], gridMap.shape[1]
        numAgents, agentLocs, agentGoals = self.parseAgents(gridMap)
        obstacles = self.parseObstacles(gridMap)
        return self.packData(numAgents, agentLocs, agentGoals, obstacles, rows, cols)
    
    def parseAgentsGoal(self, gridMap, agentID):
        rows, cols = gridMap.shape[0], gridMap.shape[1]

        for row in range(0, rows):
            for col in range(0, cols):
                if gridMap.iloc[row][col].startswith('g%d'%(agentID)):
                    return (row, col)
        raise RuntimeError("No target was found against agent_%d"%(agentID))
    
    def parseAgents(self, gridMap):
        numAgents = {}
        numAgents['numAgents'] = 0
        agentLocs = {}
        agentLocs['agentLocs'] = {}
        agentGoals = {}
        agentGoals['agentGoals'] = {}

        rows, cols = gridMap.shape[0], gridMap.shape[1]
        
        for row in range(0, rows):
            for col in range(0, cols):
                if gridMap.iloc[row][col].startswith('x'):
                    numAgents['numAgents'] += 1
                    if int(gridMap.iloc[row][col][1]) < 0:
                        raise ValueError("agent id should be positive")
                    agentName = 'agent_%d'%(int(gridMap.iloc[row][col][1]))
                    if self.parseTargets:
                        agentGoals['agentGoals'][agentName] = self.parseAgentsGoal(gridMap, int(gridMap.iloc[row][col][1]))
                    else:
                        agentGoals['agentGoals'][agentName] = None
                    agentLocs['agentLocs'][agentName] = (row, col)
        '''
        for row in range(0, rows):
            for col in range(0, cols):
                if gridMap.iloc[row][col].startswith('x') and gridMap.iloc[row][col].endswith('e'):
                    agentName = 'agent_%d'%(int(gridMap.iloc[row][col][1]))
                    agentGoals['agentGoals'][agentName] = (row, col)
        '''
        return numAgents, agentLocs, agentGoals
    
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