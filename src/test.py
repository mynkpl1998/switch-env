from switch import makeEnv


if __name__ == "__main__":
    exampleMap = '/home/mayank/Documents/multi-agentEnv/Switch/examples/map.txt'
    env = makeEnv(gridMapFile=exampleMap)

    obv = env.reset()
    for key in obv.keys():
        print("Key : ", key)
        print(obv[key])
    
    env.render()