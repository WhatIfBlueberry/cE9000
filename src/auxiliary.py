import numpy as np
import logging
from datetime import datetime
import os

def setupLogger(name, logName, outDir, LOG, level=logging.INFO):
    if not LOG:
        return None
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(os.path.join(outDir, f"{logName}.txt"))
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def setupOutDir(VISUAL, LOG):
    if not VISUAL and not LOG:
        return None
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year

    base_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",  "out")

    folder_name = f"Sim{day:02d}{month:02d}{year}"
    new_directory_path = os.path.join(base_directory, folder_name)

    # Check if the directory already exists, and create it with a counter if needed
    counter = 1
    while os.path.exists(new_directory_path):
        folder_name = f"Sim{day:02d}{month:02d}{year}-{counter}"
        new_directory_path = os.path.join(base_directory, folder_name)
        counter += 1

    os.makedirs(new_directory_path)

    return new_directory_path

def algorithmLog(logger, currentTemp, E, k, accepted, p, tempBasedProbability):
    logger.info(f"Current Temperature: {currentTemp:<7.2f} Previous Energy: {E[k-1]:<10.2f} Current Energy: {E[k]:<10.2f} Iteration: {k:<7} dE: {E[k]-E[k-1]:<10.2f} p: {p:<10.2e} expProb: {tempBasedProbability:<10.2e} {'ACCEPTED' if accepted else ''}")

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

# this is done to avoid overflow errors because the exponential function is too big
# one is fine since it is the maximum probability
def tempBasedProbability(dE, currentTemp):
    if (-dE / currentTemp) > 1:
        return 1
    return np.exp(-dE / currentTemp)