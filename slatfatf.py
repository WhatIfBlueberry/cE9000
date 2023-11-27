import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

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

size = 3
spins = initialize_model(size)
print("Energie des Anfangszustands: ", ce9000(spins))

iter = int(1000) # Anz. Iterationen
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

# Create a figure and a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Function to update the scatter plot for each frame
def update(num, e, scatters):
    ax.clear()
    x, y, z = np.where(e[num] == 1)
    scatters[0] = ax.scatter(x, y, z, color='b', label='Spin 1')
    x, y, z = np.where(e[num] == -1)
    scatters[1] = ax.scatter(x, y, z, color='r', label='Spin -1')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend()

# Create an empty list for the scatter plots
scatters = [None, None]

# Create the animation
ani = FuncAnimation(fig, update, frames=len(e), fargs=(e, scatters))

# Save the animation as an mp4 file
ani.save('animation.mp4', writer='ffmpeg', fps=2)

plt.show()