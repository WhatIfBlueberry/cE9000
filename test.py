import numpy as np

matrix_size = 3

# init A (array of 3d matrices)
A = []
for _ in range(10):
    A.append(np.random.choice([1, -1], size=(matrix_size, matrix_size, matrix_size)))

print(len(A))

for i in range (10):
    print(i)