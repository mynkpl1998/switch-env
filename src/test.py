from switch import makeEnv
import numpy as np

if __name__ == "__main__":
    exampleMap = '/home/mayank/Documents/MARLC/MARLC/experiments/narrowLane_2agent.map'
    env = makeEnv(gridMapFile=exampleMap, frameDelay=0.01, parseTargets=True)
    
    for i in range(0, 1):
        env.reset()
        done = False
        while True:
            env.render()
            
            actions = {}
            for agent in env.agentIDs:
                actions[agent] = np.random.randint(0, 5)
            
            nextObs, reward, dones, _ = env.step(actions)

            if dones['__all__']:
                env.render()
                input()
                break