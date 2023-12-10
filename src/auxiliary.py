import numpy as np
import logging

def setupLogger(name, log_file, LOG, level=logging.INFO):
    if not LOG:
        return None
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def algorithmLog(logger, currentTemp, E, k, accepted, p, tempBasedProbability):
    logger.info(f"Current Temperature: {currentTemp:.2f}     Previous Energy: {E[k-1]:<10}  Current Energy: {E[k]:<10} Iteration: {k:<7}  dE:  {E[k]-E[k-1]:<7} p: {p:.2e}   expProb: {tempBasedProbability:.2e} {'ACCEPTED' if accepted else ''}")

# Stores a sample of the spin states for visualization purposes
def storeOptimizationLog(ITERATIONS, ANIMATION_FRAMES, optimizationLog, spinMatrix, k):
    if (k % (ITERATIONS / ANIMATION_FRAMES) == 0):
        optimizationLog.append(spinMatrix.copy())

def generateRandomIntegers(ITERATIONS, SIZE):
    return np.random.randint(0,SIZE,[ITERATIONS])

def generateRandomCoordinates( ITERATIONS, SIZE):
    x = generateRandomIntegers(ITERATIONS, SIZE)
    y = generateRandomIntegers(ITERATIONS, SIZE)
    z = generateRandomIntegers(ITERATIONS, SIZE)
    return x,y,z

def printInitialEnergy(E):
    print("Energy before optimization: ", E[0])

def printFinalEnergy(E):
    print("Energy after optimization: ", E[-1])