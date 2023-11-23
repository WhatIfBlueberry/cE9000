import numpy as np
def initialize_model(n):
    return np.random.choice([1, -1], size=(n, n))

def cE9000(spins, interactionDistance=1):
    size = spins.shape[0]
    energy = 0
    for i in range(size):
        for j in range(size):
            for k in range(size):
                spin = spins[i,j,k]
                neighbors_sum = (
                    spins[(i+interactionDistance) % size,j,k] +
                    spins[(i-interactionDistance+size) % size,j,k] +
                    spins[i,(j+interactionDistance) % size,k] +
                    spins[i,(j-interactionDistance+size) % size,k] +
                    spins[i,j,(k+interactionDistance) % size] +
                    spins[i,j,(k-interactionDistance+size) % size])
                energy += (-1) * spin * neighbors_sum
    return energy

def cE9000_2D(spins, interactionDistance=1):
    size = spins.shape[0]
    energy = 0
    for i in range(size):
        for j in range(size):
            spin = spins[i,j]
            neighbors_sum = (
                spins[(i+interactionDistance) % size,j] +
                spins[(i-interactionDistance+size) % size,j] +
                spins[i,(j+interactionDistance) % size] +
                spins[i,(j-interactionDistance+size) % size])
            energy += (-1) * spin * neighbors_sum
    return energy

def breidbachZeugsl(s):
    so = np.roll(s,-1,0)
    su = np.roll(s, 1,0)
    sl = np.roll(s,-1,1)
    sr = np.roll(s, 1,1)
    H = -1 * (s*so + s*su + s*sl + s*sr)
    return H.sum()

interactionDistance = 1
size = 5
spins = initialize_model(size)
energy = 0
#for x in range(interactionDistance, 0, -1):
    #energy += cE9000(spins, x)
print("breidbachZeugsl: ",breidbachZeugsl(spins))
print("UnserZeugsl:",cE9000_2D(spins))
