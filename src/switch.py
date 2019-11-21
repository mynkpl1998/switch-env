import gym
import time
import pygame
from ui import ui
import numpy as np
from common import readFile
from mapParser import mapParser
from constants import OBJECT_MAP, AGENT_START_INDEX


class makeEnv():

    def __init__(self, gridMapFile):

        # Grid map file path
        self.gridMapFile = gridMapFile
        
        # Grid map file handle
        self.gridMapFileHandle = readFile(self.gridMapFile)

        # Parse map
        self.gridParser = mapParser(self.gridMapFileHandle)
        self.parsedMap = self.gridParser.parseMap()

        # UI object
        self.uiHandler = ui(self.parsedMap['agentLocs'])
        self.viewer = None
    

    def getAgentObservation(self, agentLoc, gridMap):
        
        '''
        Order of observation
        0 1 2
        3 4 5
        6 7 8
        '''
        row = agentLoc[0]
        col = agentLoc[1]
        obsVector = -1 * np.ones(9)
        indices = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1), (row, col), (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)]
        for idx, index in enumerate(indices):
            if index[0] >= 0 and index[1] >= 0 and index[0] < self.parsedMap['rows'] and index[1]< self.parsedMap['cols']:
                obsVector[idx] = gridMap[index[0], index[1]]
        return obsVector.reshape(3,3).copy()
    
    def getState(self, gridMap):
        return gridMap.copy()

    def getAllAgentsObservation(self, agentLocs, gridMap):
        obs = {}
        for agentID in agentLocs.keys():
            obs[agentID] = self.getAgentObservation(agentLocs[agentID], gridMap)
        obs['state'] = self.getState(gridMap)
        return obs

    def reset(self):
        # Create empty grid
        self.gridMap = np.zeros((self.parsedMap['rows'], self.parsedMap['cols']))

        # Init agents
        self.agentLocs = {}
        for agent in range(0, self.parsedMap['numAgents']):
            agentName = 'agent_%d'%(agent+1)
            agentLoc = self.parsedMap['agentLocs'][agentName]
            self.agentLocs[agentName] = [agentLoc[0], agentLoc[1]]

        # Init obstacles
        for blockedCell in self.parsedMap['blockedCells']:
            self.gridMap[blockedCell[0], blockedCell[1]] = OBJECT_MAP['T']

        # Put agents in the grids
        for idx, agent in enumerate(self.parsedMap['agentLocs'].keys()):
            self.gridMap[self.parsedMap['agentLocs'][agent][0], self.parsedMap['agentLocs'][agent][1]] = 100 + int(agent[-1])
        
        return self.getAllAgentsObservation(self.agentLocs, self.gridMap.copy())
    
    def render(self,):
        img = self.uiHandler.render(self.gridMap, self.agentLocs, self.parsedMap['agentGoals'])

        img = np.asarray(img)
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        self.viewer.imshow(img)
        time.sleep(100)
        return self.viewer.isopen