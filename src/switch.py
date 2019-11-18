import gym
import pygame
import numpy as np

from common import readFile
from parser import mapParser

class makeEnv():

    def __init__(self, gridMapFile):

        # Grid map file path
        self.gridMapFile = gridMapFile
        
        # Grid map file handle
        self.gridMapFileHandle = readFile(self.gridMapFile)

        # Parse map
        self.gridParser = mapParser(self.gridMapFileHandle)
        self.parsedMap = self.gridParser.parseMap()
        



