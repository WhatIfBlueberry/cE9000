import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from tqdm import tqdm
import os
from dotenv import load_dotenv
## import own modules
import energyWJ
import temperature
import auxiliary
import animate

# Load environment variables from config.env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config.env')
load_dotenv(dotenv_path)

# Model Parameters read from config.env
VISUAL = bool(os.getenv("VISUAL").lower() == "true")            # if true, the animation will be shown at the end
SIZE = int(os.getenv("SIZE"))                                   # model dimensions: size x size x size
ITERATIONS = int(os.getenv("ITERATIONS"))                       # Amount of iterations
INTERACTION_DISTANCE = int(os.getenv("INTERACTION_DISTANCE"))   # Distance of interaction
J0 = int(os.getenv("J0"))                                       # Interaction strength
T0 = float(os.getenv("T0"))                                     # Starting temperature
TEMP_PROFILE = os.getenv("TEMP_PROFILE")                        # Temperature profile  (lin, bilin, exp)
TEMPERATURE_LADDER = int(os.getenv("TEMPERATURE_LADDER"))       # Amount of steps until temperature is lowered
ANIMATION_FRAMES = int(os.getenv("ANIMATION_FRAMES"))           # counter for optimizationLog
LOG = bool(os.getenv("LOG").lower() == "true")                  # if true, the log will be printed

E = np.zeros([ITERATIONS])  # Array of energy values
optimizationLog = []        # Array of spin states. Used for visualization at the end
logger = None               # Logger for the log file

def main():
    # In the first Matrix, every particle knows its own state and all its neighbors
    # The second only contains the spin values for easier computation
    particleMatrix, spinMatrix = init()
    E[0] = energyWJ.systemEnergy(particleMatrix, J0)
    T = temperature.temperatureProfile(TEMP_PROFILE, T0, TEMPERATURE_LADDER, ITERATIONS)

    global logger
    logger = auxiliary.setupLogger('first_logger', '../out/algorithmLog.txt', LOG)

    auxiliary.printInitialEnergy(E)

    xrand, yrand, zrand = auxiliary.generateRandomCoordinates(ITERATIONS, SIZE) # Coordinates of random spins to be flipped
    prand = np.random.uniform(0,1,ITERATIONS) # Random number for probability calculation

    for k in tqdm(range(0, ITERATIONS), desc ="Progress: "): # Iterate while also showing fancy progress bar
        x,y,z = xrand[k], yrand[k], zrand[k] # Coordinates of random spin to be flipped
        p = prand[k]
        dE = energyWJ.deltaEnergyOfParticle(particleMatrix[x][y][z], J0)
        applySimulatedAnnealingStep(particleMatrix, spinMatrix, x, y, z, dE, T,  k, p)
        auxiliary.storeOptimizationLog(ITERATIONS, ANIMATION_FRAMES, optimizationLog, spinMatrix, k)

    auxiliary.printFinalEnergy(E)
    animate.optionalVisualization(VISUAL, optimizationLog, LOG)

def applySimulatedAnnealingStep(particleMatrix, spinMatrix, x, y, z, dE, T, k, p):
    particle = particleMatrix[x][y][z]
    deltaSmaller = dE < 0
    currentTemp = T[k]
    accepted = False
    tempBasedProbability = np.exp(-dE / T[k])
    if deltaSmaller or (currentTemp > 0 and p < tempBasedProbability):
        accepted = True
        particle['spin'] = (-1) * particle['spin']
        spinMatrix[x][y][z] = (-1) * spinMatrix[x][y][z]
        E[k] = E[k-1] + dE
    else:
        E[k] = E[k-1]
    if LOG:
        auxiliary.algorithmLog(logger, currentTemp, E, k, accepted, p, tempBasedProbability)

def init():
   matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': np.random.choice([1, -1])} for z in range(SIZE)] for y in range(SIZE)] for x in range(SIZE)]
   spin_matrix = np.array([[[item['spin'] for item in row] for row in layer] for layer in matrix])
   for x in range(SIZE):
       for y in range(SIZE):
           for z in range(SIZE):
               energyWJ.find_neighbors(matrix[x][y][z], matrix, INTERACTION_DISTANCE)
   return matrix, spin_matrix

### RUN!! ###

main()


