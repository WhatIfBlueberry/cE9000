# Requirements:
# Calculation of the energy of a given spin for fixed interaction distance 1, 2 or 3
# For example distance 2 is defined as all spins within a euclidean distance of 2 or less
# Distance for direct neighbors is 1. For next-nearest neighbors it is 2. For the one on the top left, it is sqrt(2) and so on
# Interaction decreases by the factor 1/d (d = distance to neighbor)





def calculateSystemEnergy(spins, interactionDistance, energy=0):
    SIZE = spins.shape[0]
    interactionDistance = 1
    energy = 0
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                energy += energyOfSpinAtPos(i, j, k, spins, interactionDistance)
    return energy

def energyOfSpinAtPos(i, j, k, spins, interactionDistance):
    if (interactionDistance == 1):
        return energyOfSpinWithDistance1(i, j, k, spins)
    elif (interactionDistance == 2):
        return energyOfSpinWithDistance2(i, j, k, spins)
    elif (interactionDistance == 3):
        return energyOfSpinWithDistance3(i, j, k, spins)
    else:
        print("Interaction distance not supported")
        return 0


"""
3D grid: For distance 1
+---+---+---+
|   | N |   |
+---+---+---+
| N |(*)| N |
+---+---+---+
|   | N |   |
+---+---+---+

(*) Spin at position (i, j, k)
N   Direct neighbors at positions (i±distance, j, k), (i, j±distance, k), and (i, j, k±distance)
"""
def trivialNeighborSum(i, j, k, spins, energy, interactionDistance):
    if (interactionDistance == 0):
        return energy

    SIZE = spins.shape[0]
    spin = spins[i,j,k]
    direct_neighbors_sum = (
        spins[(i+interactionDistance) % SIZE,j,k] +
        spins[(i-interactionDistance+SIZE) % SIZE,j,k] +
        spins[i,(j+interactionDistance) % SIZE,k] +
        spins[i,(j-interactionDistance+SIZE) % SIZE,k] +
        spins[i,j,(k+interactionDistance) % SIZE] +
        spins[i,j,(k-interactionDistance+SIZE) % SIZE])
    energy += (-1) * spin * direct_neighbors_sum * (1 / interactionDistance)
    return trivialNeighborSum(i, j, k, spins, energy, interactionDistance - 1)

def diagonalNeighborSum(i, j, k, spins, energy, interactionDistance):
    if (interactionDistance == 1):
        return energy

    SIZE = spins.shape[0]
    spin = spins[i,j,k]
    direct_neighbors_sum = (
        spins[(i+interactionDistance) % SIZE,j,k] +
        spins[(i-interactionDistance+SIZE) % SIZE,j,k] +
        spins[i,(j+interactionDistance) % SIZE,k] +
        spins[i,(j-interactionDistance+SIZE) % SIZE,k] +
        spins[i,j,(k+interactionDistance) % SIZE] +
        spins[i,j,(k-interactionDistance+SIZE) % SIZE])
    energy += (-1) * spin * direct_neighbors_sum * (1 / interactionDistance)


def energyOfSpinWithDistance1(i, j, k, spins, energy = 0):
    return trivialNeighborSum(i, j, k, spins, energy, 1)

def energyOfSpinWithDistance2(i, j, k, spin, energy = 0):
    directSum = trivialNeighborSum(i, j, k, spin, energy, 2)

    return 0

def energyOfSpinWithDistance3(i, j, k, spin):
    energy = 0

    return 0



def deltaE(i, j, k, spins, interactionDistance):
    return -2 * energyOfSpinAtPos(i, j, k, spins, interactionDistance)


# 