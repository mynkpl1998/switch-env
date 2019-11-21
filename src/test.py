from switch import makeEnv
import numpy as np

if __name__ == "__main__":
    exampleMap = '/home/mayank/Documents/multi-agentEnv/Switch/examples/map.txt'
    env = makeEnv(gridMapFile=exampleMap, frameDelay=0.5)

    for ep in range(0, 10):
        obs = env.reset()
        count = 0
        print("Reset...")
        for i in range(0, 10):
            count += 1
            env.render()

            actions = {}
            for agent in env.agentIDs:
                actions[agent] = np.random.randint(0, 5)

            nextObs, reward, dones, _ = env.step(actions)
            
            if dones['__all__']:
                print(count)
                break