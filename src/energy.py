


def ce9000(spins, interactionDistance=1):
    energy = 0
    SIZE = spins.shape[0]
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                energy += energyOfSpinAtPos(i, j, k, spins, interactionDistance)
    return energy

def energyOfSpinAtPos(i, j, k, spins, interactionDistance=1):
    spin = spins[i,j,k]
    SIZE = spins.shape[0]
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