OBJECT_MAP = {}
OBJECT_MAP['x'] = 2
OBJECT_MAP['o'] = 0
OBJECT_MAP['T'] = 1

INV_OBJECT_MAP = {v: k for k, v in OBJECT_MAP.items()}

AGENT_START_INDEX = 10
GOAL_START_INDEX = 20
SUCCESS_START_INDEX = 30

UI_CONSTS = {}
UI_CONSTS['cell_size'] = 50
'''
Color link -> https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
'''
UI_CONSTS['distinct_colors'] = ["#800000", '#9A6324', '#808000', '#469990', '#000075', '#e6194B', '#f58231', '#bfef45', '#911eb4', '#f032e6', '#a9a9a9', '#ffd8b1']

ACTION_MAP = {}
ACTION_MAP[0] = 'UP'
ACTION_MAP[1] = 'DOWN'
ACTION_MAP[2] = 'LEFT'
ACTION_MAP[3] = 'RIGHT'
ACTION_MAP[4] = 'STAY'