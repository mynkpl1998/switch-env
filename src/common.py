import os

def readFile(filePath):
    if not os.path.exists(filePath):
        raise ValueError("invalid file path \"%s\""%(filePath))
    return open(filePath, 'r')