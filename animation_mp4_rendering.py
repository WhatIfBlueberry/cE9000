import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

plt.rcParams['animation.ffmpeg_path']='C:\\Users\\Test\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'

metadata = dict(title='Random-Boolean-Matrix', artist='Me')
writer = FFMpegWriter(fps=2, metadata=metadata)  # fps is the speed of the animation

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

matrix_size = 3

# init A (array of 3d matrices)
A = []
for _ in range(10):
    A.append(np.random.choice([1, -1], size=(matrix_size, matrix_size, matrix_size)))

plt.xlim(0, matrix_size)
plt.ylim(0, matrix_size)

def plot_matrix(matrix, ax):
    ax.clear()
    ax.set_zlim(0, matrix_size)
    for i in range(matrix_size):
        for j in range(matrix_size):
            for k in range(matrix_size):
                if matrix[i, j, k] == 1:
                    ax.scatter(i, j, k, c='b', marker='o', alpha=0.5)
                else:
                    ax.scatter(i, j, k, c='r', marker='o', alpha=0.5)

with writer.saving(fig, "matrix_animation.mp4", 100):
    for i in range(10):
        plot_matrix(A[i], ax)
        writer.grab_frame()