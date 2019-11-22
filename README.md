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

## Installation Instructions

1. Clone the repository: `https://github.com/mynkpl1998/switch-env.git`
2. Navigate to the cloned directory: `cd switch-env` 
3. Build wheel: `python setup bdist_wheel`
4. Install: `pip install -e .`