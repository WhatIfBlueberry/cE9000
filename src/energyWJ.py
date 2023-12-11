
# particle:
#   x, y, z
#   spin
#   neighbors: -> particle[]

# matrix:
#   x, y, z size
#   -> particles[]

# interaction distance
#   int > 0

# find all neighbors of each particle
#   check the box around the particle of choice
#   for n in x where x || matrix.xmin and x || matrix.xmax
#   check if the distance between them is smaller or equal to int_dist
#   if (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 <= int_dist**2
#

# get the energy of the whole system (matrix, distance)

import numpy as np
import math
# find the neighbors of a particle
#   center as particle
#   matrix as matrix
#   distance as int
def find_neighbors(center, matrix, distance):
    neighbors = []
    x_center, y_center, z_center = center['x'], center['y'], center['z']
    for x in range(max(0, x_center - distance), min(len(matrix), x_center + distance + 1)):
        for y in range(max(0, y_center - distance), min(len(matrix[0]), y_center + distance + 1)):
            for z in range(max(0, z_center - distance), min(len(matrix[0][0]), z_center + distance + 1)):
                if  x == x_center and y == y_center and z == z_center:
                    continue
                point = matrix[x][y][z]
                dist = math.sqrt((x - x_center)**2 + (y - y_center)**2 + (z - z_center)**2)
                if dist <= distance and point is not None:
                    neighbors.append(point)
    center['neighbors'] = neighbors

# get the energy of the whole system (matrix, distance)
def energy_of_system(matrix, J0):
    energy = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            for z in range(len(matrix[0][0])):
                particle = matrix[x][y][z]
                if particle is not None:
                    energy += J0 * get_energy_of_particle(particle)
    return energy


def get_delta_energy_of_particle(particle):
    # energy of the particle if it would flip. Times 2 because
    return -2 * get_energy_of_particle(particle)

# get the energy of a single particle (particle, distance)
def get_energy_of_particle(particle):
    neighbors = particle['neighbors']
    sum = 0
    for neighbor in neighbors:
        # TODO 1 as constant, might be -1
        sum += neighbor['spin'] * (1 / distanceToParticle(particle, neighbor))
    return particle['spin'] * sum

def distanceToParticle(particle1, particle2):
    return math.sqrt((particle1['x'] - particle2['x'])**2 + (particle1['y'] - particle2['y'])**2 + (particle1['z'] - particle2['z'])**2)