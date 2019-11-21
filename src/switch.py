import gym
import time
import copy
import pygame
from ui import ui
import numpy as np
from common import readFile
from mapParser import mapParser
from constants import OBJECT_MAP, AGENT_START_INDEX, ACTION_MAP


class makeEnv():

    def __init__(self, gridMapFile, frameDelay=0.05, cooperative=False):

        # Delay between two frames
        self.frameDelay = frameDelay

        # Agents type
        self.cooperative = cooperative

        # Grid map file path
        self.gridMapFile = gridMapFile
        
        # Grid map file handle
        self.gridMapFileHandle = readFile(self.gridMapFile)

        # Parse map
        self.gridParser = mapParser(self.gridMapFileHandle)
        self.parsedMapOrig = copy.deepcopy(self.gridParser.parseMap())

        # UI object
        self.uiHandler = ui(self.parsedMapOrig['agentLocs'])
        self.viewer = None

        # Variables
        self.agentIDs = list(self.parsedMapOrig['agentLocs'].keys())

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
    
    def buildDoneDict(self, agents):
        dones = {}
        for agent in agents:
            dones[agent] = False
        dones['__all__'] = False
        return copy.deepcopy(dones)

    def reset(self):
        
        # Reset the map
        self.parsedMap = copy.deepcopy(self.parsedMapOrig)

        # Create empty grid
        gridMap = np.zeros((self.parsedMap['rows'], self.parsedMap['cols']))
        gridMap = self.populateObstacles(self.parsedMap['blockedCells'], gridMap)
        gridMap = self.populateAgents(self.parsedMap['agentLocs'], gridMap)
        self.gridMap = gridMap
        self.dones = self.buildDoneDict(self.parsedMap['agentLocs'].keys())
        return self.getAllAgentsObservation(self.parsedMap['agentLocs'], gridMap.copy())
    
    def render(self,):
        img = self.uiHandler.render(self.gridMap, self.parsedMap['agentLocs'], self.parsedMap['agentGoals'])

        img = np.asarray(img)
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        self.viewer.imshow(img)
        time.sleep(self.frameDelay)
        return self.viewer.isopen
    
    def checkValidLoc(self, newAgentLoc, agentLoc):
        if newAgentLoc[0] >= 0 and newAgentLoc[1] >= 0 and newAgentLoc[0] < self.parsedMap['rows'] and newAgentLoc[1] < self.parsedMap['cols']:
            return newAgentLoc, True
        else:
            return agentLoc, False
    
    def checkValidCell(self, agentLoc, obstacles, otherAgents, oldLoc):
        if agentLoc in obstacles or agentLoc in otherAgents.values():
            return oldLoc
        return agentLoc


    def moveUP(self, agentLoc, otherAgentsLoc, obstacles):
        newAgentLoc, res = self.checkValidLoc((agentLoc[0]-1, agentLoc[1]), agentLoc)
        if not res:
            return agentLoc
        else:
            agentLoc = self.checkValidCell(newAgentLoc, obstacles, otherAgentsLoc, agentLoc)
        return agentLoc
    
    def moveDOWN(self, agentLoc, otherAgentsLoc, obstacles):
        newAgentLoc, res = self.checkValidLoc((agentLoc[0]+1, agentLoc[1]), agentLoc)
        if not res:
            return agentLoc
        else:
            agentLoc = self.checkValidCell(newAgentLoc, obstacles, otherAgentsLoc, agentLoc)
        return agentLoc
    
    def moveLEFT(self, agentLoc, otherAgentsLoc, obstacles):
        newAgentLoc, res = self.checkValidLoc((agentLoc[0], agentLoc[1]-1), agentLoc)
        if not res:
            return agentLoc
        else:
            agentLoc = self.checkValidCell(newAgentLoc, obstacles, otherAgentsLoc, agentLoc)
        return agentLoc
    
    def moveRIGHT(self, agentLoc, otherAgentsLoc, obstacles):
        newAgentLoc, res = self.checkValidLoc((agentLoc[0], agentLoc[1]+1), agentLoc)
        if not res:
            return agentLoc
        else:
            agentLoc = self.checkValidCell(newAgentLoc, obstacles, otherAgentsLoc, agentLoc)
        return agentLoc
    

    def step(self, action):
        
        # Updates agent position
        for agent in action:
            if not self.dones[agent]:
                newLoc = None
                otherAgentsLocs = copy.deepcopy(self.parsedMap['agentLocs'])
                del otherAgentsLocs[agent]
                
                if ACTION_MAP[action[agent]] == 'UP':
                    newLoc = self.moveUP(self.parsedMap['agentLocs'][agent], otherAgentsLocs, self.parsedMap['blockedCells'])
                elif ACTION_MAP[action[agent]] == 'DOWN':
                    newLoc = self.moveDOWN(self.parsedMap['agentLocs'][agent], otherAgentsLocs, self.parsedMap['blockedCells'])
                elif ACTION_MAP[action[agent]] == 'LEFT':
                    newLoc = self.moveLEFT(self.parsedMap['agentLocs'][agent], otherAgentsLocs, self.parsedMap['blockedCells'])
                elif ACTION_MAP[action[agent]] == 'RIGHT':
                    newLoc = self.moveRIGHT(self.parsedMap['agentLocs'][agent], otherAgentsLocs, self.parsedMap['blockedCells'])
                elif ACTION_MAP[action[agent]] == 'STAY':
                    newLoc = self.parsedMap['agentLocs'][agent]
                else:
                    raise ValueError("invalid action %d... for agent %s"%(action[agent], agent))

                self.parsedMap['agentLocs'][agent] = newLoc
        
        # New observation
        # Create empty grid
        gridMap = np.zeros((self.parsedMap['rows'], self.parsedMap['cols']))
        gridMap = self.populateObstacles(self.parsedMap['blockedCells'], gridMap)
        gridMap = self.populateAgents(self.parsedMap['agentLocs'], gridMap)
        self.gridMap = gridMap
        obsDict = self.getAllAgentsObservation(self.parsedMap['agentLocs'], gridMap.copy())
        
        # Update done dict
        for agent in self.parsedMap['agentGoals'].keys():
            if self.parsedMap['agentGoals'][agent] == self.parsedMap['agentLocs'][agent]:
                self.dones[agent] = True
        allDone = True
        for agent in self.parsedMap['agentGoals'].keys():
            allDone = allDone and self.dones[agent]
        self.dones['__all__'] = allDone

        # Reward Calculation
        rewardDict = {}
        if self.cooperative:
            rewardDict['team_reward'] = 0.0
        else:
            for agent in self.parsedMap['agentLocs'].keys():
                rewardDict[agent] = None
        
        if self.cooperative:
            if self.dones['__all__']:
                rewardDict['team_reward'] = 0.0
            else:
                totalSum = 0.0
                for agent in self.parsedMap['agentLocs'].keys():
                    totalSum += -(not self.dones[agent])
                rewardDict['team_reward'] = totalSum
        else:
            for agent in self.parsedMap['agentLocs'].keys():
                rewardDict[agent] = -(not self.dones[agent])
        return obsDict, rewardDict, self.dones, {}