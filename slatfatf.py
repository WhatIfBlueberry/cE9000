import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

# global array of spin states. Used for visualization at the end
e = []
count = 0

def initialize_model(n):
    return np.random.choice([1, -1], size=(n, n, n))

def ce9000(spins, interactionDistance=1):
    size = spins.shape[0]
    energy = 0
    for i in range(size):
        for j in range(size):
            for k in range(size):
                energy += energyOfSpinAtPos(i, j, k, spins, interactionDistance)
    return energy

def energyOfSpinAtPos(i, j, k, spins, interactionDistance=1):
    size = spins.shape[0]
    spin = spins[i,j,k]
    neighbors_sum = (
        spins[(i+interactionDistance) % size,j,k] +
        spins[(i-interactionDistance+size) % size,j,k] +
        spins[i,(j+interactionDistance) % size,k] +
        spins[i,(j-interactionDistance+size) % size,k] +
        spins[i,j,(k+interactionDistance) % size] +
        spins[i,j,(k-interactionDistance+size) % size])
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


#################

size = 50
spins = initialize_model(size)
print("Energie des Anfangszustands: ", ce9000(spins))

iter = int(10000) # Anz. Iterationen
T0 = 7         # Starttemperatur
K = 100         # Kettenlänge

T = mkCoolingScheduleLin(T0,K,iter)

irand = np.random.uniform(0,size,[iter]).astype(int)
jrand = np.random.uniform(0,size,[iter]).astype(int)
krand = np.random.uniform(0,size,[iter]).astype(int)
# Das sind die koordinaten des zufälligen Punktes, der evtl. geflippt wird
Prand = np.random.uniform(0,1,[iter]) # Rand

# Initialisierung benötigter Vektoren
E   = np.zeros([iter])

E[0] = ce9000(spins)
for k in np.arange(1,iter):
    i,j,z = irand[k],jrand[k], krand[k]
    dE = deltaE(i,j,z, spins)
    deltaSmaller = dE<0
    currentTemp = T[k]
    if deltaSmaller or (currentTemp > 0 and Prand[k]<np.exp(-dE/T[k])):
        # Move durchführen
        spins[i,j,z] = -spins[i,j,z]
        # Energie speichern
        E[k] = E[k-1] + dE
    else:
        E[k] = E[k-1]
    if (count % (iter / 20) == 0):
        e.append(np.copy(spins))
    count += 1

################

print("Energie des Endzustands: ", ce9000(spins))
y = 0
for x in e:
    print('state', y)
    print(x)
    print("Energie des Zustands: ", ce9000(x))
    y += 1

plt.rcParams['animation.ffmpeg_path']='C:\\Users\\Test\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'

metadata = dict(title='Ising-Model', artist='Dylan & Eva')
writer = FFMpegWriter(fps=2, metadata=metadata)  # fps is the speed of the animation

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

plt.xlim(0, size)
plt.ylim(0, size)

def plot_matrix(matrix, ax):
    ax.clear()
    ax.set_zlim(0, size)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if matrix[i, j, k] == 1:
                    ax.scatter(i, j, k, c='b', marker='o', alpha=0.5)
                else:
                    ax.scatter(i, j, k, c='r', marker='o', alpha=0.5)

with writer.saving(fig, "matrix_animation.mp4", 100):
    for i in range(len(e)):
        plot_matrix(e[i], ax)
        writer.grab_frame()