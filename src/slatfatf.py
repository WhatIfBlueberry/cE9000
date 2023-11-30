import numpy as np
import matplotlib.pyplot as plt
import animate
from matplotlib.animation import FFMpegWriter
from tqdm import tqdm
import os

optimizationLog = [] #  array of spin states. Used for visualization at the end
animationFrames = 200 #  counter for optimizationLog

SIZE = 20 # model dimensions: size x size x size
ITERATIONS = int(100000) # Amount of iterations
TEMPERATURE_LADDER = 100 # Amount of steps until temperature is lowered
E = np.zeros([ITERATIONS]) # Array of energy value
T0 = 7 # Starting temperature

def main(visual=False):
    spins = initialize_model(SIZE)
    E[0] = ce9000(spins) # Initial Energy
    printInitialEnergy(spins)

    T = mkCoolingScheduleLin(T0,TEMPERATURE_LADDER,ITERATIONS)

    xrand, yrand, zrand = generateRandomCoordinates(ITERATIONS) # Coordinates of random spins to be flipped
    prand = generateRandomIntegers(ITERATIONS) # Random number for probability calculation


    for k in tqdm(range(0, ITERATIONS), desc ="Progress: "):
        x,y,z = xrand[k],yrand[k], zrand[k]
        p = prand[k]
        dE = deltaE(x,y,z, spins)
        apply_simulated_annealing_step(spins, T, x, y, z, dE, k, p)
        storeOptimizationLog(spins, k)

    printFinalEnergy(spins)
    optional_visualization(visual)


def optional_visualization(visual):
    if visual:
        animate.create_animation(optimizationLog)
        os.system("start ../out/matrix_animation.mp4")

def storeOptimizationLog(spins, k):
    if (k % (ITERATIONS / animationFrames) == 0):
        optimizationLog.append(np.copy(spins))

def apply_simulated_annealing_step(spins, T, x, y, z, dE, k, p):
    deltaSmaller = dE < 0
    currentTemp = T[k]
    if deltaSmaller or (currentTemp > 0 and p < np.exp(-dE / T[k])):
        spins[x,y,z] = -spins[x,y,z]
        E[k] = E[k-1] + dE
    else:
        E[k] = E[k-1]


def initialize_model(n):
    return np.random.choice([1, -1], size=(n, n, n))

def ce9000(spins, interactionDistance=1):
    energy = 0
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                energy += energyOfSpinAtPos(i, j, k, spins, interactionDistance)
    return energy

def energyOfSpinAtPos(i, j, k, spins, interactionDistance=1):
    spin = spins[i,j,k]
    neighbors_sum = (
        spins[(i+interactionDistance) % SIZE,j,k] +
        spins[(i-interactionDistance+SIZE) % SIZE,j,k] +
        spins[i,(j+interactionDistance) % SIZE,k] +
        spins[i,(j-interactionDistance+SIZE) % SIZE,k] +
        spins[i,j,(k+interactionDistance) % SIZE] +
        spins[i,j,(k-interactionDistance+SIZE) % SIZE])
    return (-1) * spin * neighbors_sum

def deltaE(i, j, k, spins, interactionDistance=1):
    return -2 * energyOfSpinAtPos(i, j, k, spins, interactionDistance=1)


def mkCoolingScheduleLin(T0,K,iter):
    T = np.ones(iter)*T0
    dT = T0/(iter/K)
    for k in np.arange(2,iter):
        T[k] = T[k-1]
        if k%K == 0:
            T[k] -= dT
    return T

def printInitialEnergy(spins):
    print("Energy before optimization: ", ce9000(spins))

def printFinalEnergy(spins):
    print("Energy after optimization: ", ce9000(spins))

def generateRandomIntegers(ITERATIONS):
    return np.random.randint(0,SIZE,[ITERATIONS]).astype(int)

def generateRandomCoordinates(ITERATIONS):
    x = generateRandomIntegers(ITERATIONS)
    y = generateRandomIntegers(ITERATIONS)
    z = generateRandomIntegers(ITERATIONS)
    return x,y,z


main(visual=True)


