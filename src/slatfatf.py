import numpy as np
import matplotlib.pyplot as plt
import animate
from matplotlib.animation import FFMpegWriter
from tqdm import tqdm
import energyWJ
import os
from dotenv import load_dotenv

# Load environment variables from config.env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config.env')
load_dotenv(dotenv_path)

# Model Parameters read from config.env
VISUAL = os.getenv("VISUAL") #  if true, the animation will be shown at the end
SIZE = int(os.getenv("SIZE")) # model dimensions: size x size x size
ITERATIONS = int(os.getenv("ITERATIONS")) # Amount of iterations
TEMPERATURE_LADDER = int(os.getenv("TEMPERATURE_LADDER")) # Amount of steps until temperature is lowered
INTERACTION_DISTANCE = int(os.getenv("INTERACTION_DISTANCE")) # Distance of interaction
T0 = int(os.getenv("T0")) # Starting temperature
J0 = int(os.getenv("J0")) # Interaction strength
T1 = float(os.getenv("T1"))
T2 = float(os.getenv("T2"))
TE = float(os.getenv("TE"))
PORTION1 = float(os.getenv("PORTION1"))
PORTION2 = float(os.getenv("PORTION2"))
ANIMATION_FRAMES = int(os.getenv("ANIMATION_FRAMES")) #  counter for optimizationLog

E = np.zeros([ITERATIONS]) # Array of energy values
optimizationLog = [] #  array of spin states. Used for visualization at the end

def main():
    particleMatrix = initialize_model()
    E[0] = energyWJ.energy_of_system(particleMatrix, J0) # Initial Energy
    printInitialEnergy(particleMatrix)

    T_lin = mkCoolingScheduleLin(T0,TEMPERATURE_LADDER,ITERATIONS)
    plot_cooling_schedule(T_lin, 'Linear')
    T_bil = mkCoolingScheduleBilin(T0, TEMPERATURE_LADDER, ITERATIONS, T1, T2, PORTION1, PORTION2)
    plot_cooling_schedule(T_bil, 'Bilinear')
    T_exp = mkCoolingScheduleExp(T0, TEMPERATURE_LADDER, ITERATIONS, TE)
    plot_cooling_schedule(T_exp, 'Exponential')

    plt.xlabel('Iteration')
    plt.ylabel('Temperature')
    plt.title('Cooling Schedule Comparison')
    plt.legend()
    plt.show()

    T=T_lin

    xrand, yrand, zrand = generateRandomCoordinates(ITERATIONS) # Coordinates of random spins to be flipped
    prand = generateRandomIntegers(ITERATIONS) # Random number for probability calculation


    for k in tqdm(range(0, ITERATIONS), desc ="Progress: "): # Iterate while also showing fancy progress bar
        x,y,z = xrand[k],yrand[k], zrand[k] # Coordinates of random spin to be flipped
        p = prand[k]
        dE = energyWJ.get_delta_energy_of_particle(particleMatrix[x][y][z])
        apply_simulated_annealing_step(particleMatrix[x][y][z], dE, T,  k, p)
        storeOptimizationLog(particleMatrix, k)

    printFinalEnergy(particleMatrix)
    optional_visualization()

# If VISUAL is true, the animation will be shown at the end
def optional_visualization():
    if VISUAL:
        animate.create_animation(optimizationLog)
        os.system("start ../out/matrix_animation.mp4")

# Stores a sample of the spin states for visualization purposes
def storeOptimizationLog(particleMatrix, k):
    if (k % (ITERATIONS / ANIMATION_FRAMES) == 0):
        optimizationLog.append(particleMatrix.copy())


def apply_simulated_annealing_step(particle, dE, T, k, p):
    deltaSmaller = dE < 0
    currentTemp = T[k]
    if deltaSmaller or (currentTemp > 0 and p < np.exp(-dE / T[k])):
        particle['spin'] = (-1) * particle['spin']
        E[k] = E[k-1] + dE
    else:
        E[k] = E[k-1]


def initialize_model():
   matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': np.random.choice([1, -1])} for z in range(SIZE)] for y in range(SIZE)] for x in range(SIZE)]
   for x in range(SIZE):
       for y in range(SIZE):
           for z in range(SIZE):
               energyWJ.find_neighbors(matrix[x][y][z], matrix, INTERACTION_DISTANCE)
   return matrix
    #return np.random.choice([1, -1], size=(n, n, n))

def mkCoolingScheduleLin(T0,K,iter):
    T = np.ones(iter)*T0
    dT = T0/(iter/K)
    for k in np.arange(2,iter):
        T[k] = T[k-1]
        if k%K == 0:
            T[k] -= dT
    return T

def mkCoolingScheduleBilin(T0,K,iter,T1,T2,anteil1,anteil2):
    T = np.ones(iter)*T0;
    k1 = iter * (anteil1/1)
    k2 = iter * (anteil2/1)
    for k in np.arange(2,iter):
        T[k] = T[k-1]
        dT = 0
        if k%K == 0:
            if k<k1:
                dT = -(T1-T0)/(k1- 0)*K
            elif k<k2:
                dT = -(T2-T1)/(k2-k1)*K
            else:
                dT = -(0 -T2)/(iter-k2)*K            
            T[k] -= dT
        if T[k]<0:
            T[k]=0       
    return T

def mkCoolingScheduleExp(T0,K,iter,Te):
    T = np.ones(iter)*T0;
    λ = -1/iter * np.log(Te/T0)
    for k in np.arange(2,iter):
        T[k] = T[k-1]
        if k%K == 0:
            T[k] = T0 * np.exp(-λ*k)
    return T

def printInitialEnergy(spins):
    print("Energy before optimization: ", energyWJ.energy_of_system(spins, J0))

def printFinalEnergy(spins):
    print("Energy after optimization: ", energyWJ.energy_of_system(spins, J0))

def plot_cooling_schedule(T, title):
    plt.plot(range(len(T)), T, label=title)

def generateRandomIntegers(ITERATIONS):
    return np.random.randint(0,SIZE,[ITERATIONS])

def generateRandomCoordinates(ITERATIONS):
    x = generateRandomIntegers(ITERATIONS)
    y = generateRandomIntegers(ITERATIONS)
    z = generateRandomIntegers(ITERATIONS)
    return x,y,z


main()


