import numpy as np

#### AUXILIARY FUNCTIONS ####

def printLog(k, currentTemp, accepted, E):
    print(f"Current Temperature: {currentTemp:.2f} Current Energy: {E[k]:<10} Previous Energy: {E[k-1]:<10} Iteration: {k}", "accepted: ", "YES" if accepted else "")



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