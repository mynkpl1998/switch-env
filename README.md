# Switch Environment

## How to use ?

```
exampleMap = '/home/mayank/Documents/switch-env/examples/map.txt'
env = makeEnv(gridMapFile=exampleMap, frameDelay=0.01)
obs = env.reset()

while True:
    env.render()

    actions = {}
    for agent in env.agentIDs:
        actions[agent] = np.random.randint(0, 5)

    nextObs, reward, dones, _ = env.step(actions)    
    if dones['__all__']:
        break
```

## How to create a map via Example

The following scheme is used to represent the various entities in the map.

1. Free - o
2. Occupied - T
3. Agent start location - x
4. Agent target location - g

An example map with 2 agents and a narrow lane.

```
x1 o o T T T T o o g1
o o o o o o o o o o
g2 o o o o o o o o x2
```


## Installation Instructions

1. Clone the repository: `https://github.com/mynkpl1998/switch-env.git`
2. Navigate to the cloned directory: `cd switch-env` 
3. Build wheel: `python setup bdist_wheel`
4. Install: `pip install -e .`