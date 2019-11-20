import random
random.seed(1)
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from constants import INV_OBJECT_MAP, UI_CONSTS, OBJECT_MAP

'''
Code is adapted from following link -> https://github.com/koulanurag/ma-gym/blob/master/ma_gym/envs/utils/draw.py
'''

class ui:

    def __init__(self, agentStartLocs):
        self.agentColors = {}
        randomColors = random.sample(UI_CONSTS['distinct_colors'], len(agentStartLocs))
        for idx, agent in enumerate(agentStartLocs.keys()):
            self.agentColors[agent] = randomColors[idx]
    
    def drawGrid(self, rows, cols, cell_size=50, fill='black', line_color='black'):
        height = rows * cell_size
        width = cols * cell_size
        img = Image.new('RGB', size=(width, height), color=fill)

        # Draw cells
        draw = ImageDraw.Draw(img)
        y_start = 0
        y_end = img.height
        step_size = cell_size

        for x in range(0, img.width, step_size):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill=line_color)
        
        x = img.width - 1
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=line_color)

        x_start = 0
        x_end = img.width

        for y in range(0, img.height, step_size):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill=line_color)
        
        y = img.height - 1
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=line_color)

        del draw
        return img
    
    def drawCell(self, img, pos, cell_size=None, fill='black', margin=0):
        assert cell_size is not None and 0 <= margin <= 1
        col, row = pos
        row, col = row * cell_size, col * cell_size
        margin *= cell_size
        x, y, x_dash, y_dash = row + margin, col + margin, row + cell_size - margin, col + cell_size - margin
        ImageDraw.Draw(img).rectangle([(x,y), (x_dash, y_dash)], fill=fill)
    
    def drawCircle(self, img, pos, cell_size=None, fill='black', radius=0.3):
        assert cell_size is not None
        col, row = pos
        row, col = row * cell_size, col * cell_size
        gap = cell_size * radius
        x, y = row + gap, col + gap
        x_dash, y_dash = row + cell_size - gap, col + cell_size - gap
        ImageDraw.Draw(img).ellipse([(x,y), (x_dash, y_dash)], outline=fill, fill=fill)
    
    def write_cell_text(self, img, text, pos, cell_size=None, fill='black', margin=0):
        assert cell_size is not None and 0 <= margin <= 1
        col, row = pos
        row, col = row * cell_size, col * cell_size
        margin *= cell_size
        x, y = row + margin, col + margin
        ImageDraw.Draw(img).text((x, y), text=text, fill=fill)
    
    def fill_cell(self, img, pos, cell_size=None, fill='black', margin=0):
        assert cell_size is not None and 0 <= margin <= 1
        col, row = pos
        row, col = row * cell_size, col * cell_size
        margin *= cell_size
        x, y, x_dash, y_dash = row + margin, col + margin, row + cell_size - margin, col + cell_size - margin
        ImageDraw.Draw(img).rectangle([(x, y), (x_dash, y_dash)], fill=fill)
    
    def getNeighbours(self, rows, cols, agentLoc):
        neighboursList = [ (agentLoc[0]-1, agentLoc[1]-1), (agentLoc[0]-1, agentLoc[1]), (agentLoc[0]-1, agentLoc[1]+1), (agentLoc[0], agentLoc[1]-1), (agentLoc[0], agentLoc[1]), (agentLoc[0], agentLoc[1]+1), (agentLoc[0]+1, agentLoc[1]-1), (agentLoc[0]+1, agentLoc[1]), (agentLoc[0]+1, agentLoc[1]+1)]
        updatedList = []
        for loc in neighboursList:
            if loc[0] < 0 or loc[1] < 0 or loc[0] >= rows or loc[1] >= cols:
                pass
            else:
                updatedList.append(loc)
        return updatedList
    
    def draw_cell_outline(sef, img, pos, cell_size=None, fill='black'):
        assert cell_size is not None
        col, row = pos
        row, col = row * cell_size, col * cell_size
        ImageDraw.Draw(img).rectangle([(row, col), (row + cell_size, col + cell_size)], outline=fill, width=3)

    def render(self, grid, agentLocs, agentGoals):

        # Draw Grid
        img = self.drawGrid(grid.shape[0], grid.shape[1], cell_size=UI_CONSTS['cell_size'], fill='white', line_color='black')
        
        # Draw neigbours
        for agent in agentLocs:
            neigbours = self.getNeighbours(grid.shape[0], grid.shape[1], agentLocs[agent])
            for neigbour in neigbours:
                self.fill_cell(img, neigbour, cell_size=UI_CONSTS['cell_size'], fill=(186, 238, 247), margin=0.1)

        # Draw agents
        for idx, agent in enumerate(agentLocs):
            color = self.agentColors[agent]
            agentID = agent[-1]
            self.drawCircle(img, agentLocs[agent], cell_size=UI_CONSTS['cell_size'], fill=color, radius=0.3)
            self.write_cell_text(img, agentID, agentLocs[agent], cell_size=UI_CONSTS['cell_size'], fill='black', margin=0.45)
        
        # Draw walls
        for row in range(0, grid.shape[0]):
            for col in range(0, grid.shape[1]):
                if grid[row][col] == OBJECT_MAP['T']:
                    self.drawCell(img, (row, col), cell_size=UI_CONSTS['cell_size'], fill='black', margin=0.05)
        
        # Draw agent goals
        for agent in agentGoals:
            color = self.agentColors[agent]
            self.draw_cell_outline(img, agentGoals[agent], cell_size=UI_CONSTS['cell_size'], fill=color)

        return img
            
     