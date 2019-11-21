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
    
    def populateObstacles(self, obstaclesLocs, grid):
        for blockedCell in obstaclesLocs:
            grid[blockedCell[0], blockedCell[1]] = OBJECT_MAP['T']
        return grid
    
    def populateAgents(self, agentLocs, grid):
        for idx, agent in enumerate(agentLocs.keys()):
            grid[agentLocs[agent][0], agentLocs[agent][1]] = 100 + int(agent[-1])
        return grid

    def reset(self):
        # Create empty grid
        gridMap = np.zeros((self.parsedMap['rows'], self.parsedMap['cols']))

        gridMap = self.populateObstacles(self.parsedMap['blockedCells'], gridMap)
        gridMap = self.populateAgents(self.parsedMap['agentLocs'], gridMap)
        self.gridMap = gridMap
        return self.getAllAgentsObservation(self.parsedMap['agentLocs'], gridMap.copy())
    
    def render(self,):
        img = self.uiHandler.render(self.gridMap, self.parsedMap['agentLocs'], self.parsedMap['agentGoals'])

        img = np.asarray(img)
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        self.viewer.imshow(img)
        time.sleep(100)
        return self.viewer.isopen
    

    def step(self, action):
        pass