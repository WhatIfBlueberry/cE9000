#%matplotlib notebook
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib import animation
from matplotlib.animation import FuncAnimation

plt.rcParams['animation.ffmpeg_path']='C:\\Users\\Test\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw=dict(projection='3d')) # size of the figure and making it 3d
ax.view_init(25,135)
ax.set_axis_off()
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
matrix_size = 25

# init A (array of 3d matrices)
A = []
for _ in range(30):
    A.append(np.random.choice([1, -1], size=(matrix_size, matrix_size, matrix_size)))

plt.xlim(0, matrix_size)
plt.ylim(0, matrix_size)

indPos = []
indNeg = []
for p in range(len(A)):
    indPos.append(np.argwhere(A[p]==1))
    indNeg.append(np.argwhere(A[p]==-1))

pos = ax.scatter(indPos[0][:,0],indPos[0][:,1],indPos[0][:,2], c='b', marker='o')
neg = ax.scatter(indNeg[0][:,0],indNeg[0][:,1],indNeg[0][:,2], c='r', marker='o')
def animate(i, indPos, indNeg):
    pos._offsets3d = (indPos[i][:,0],indPos[i][:,1],indPos[i][:,2])
    neg._offsets3d = (indNeg[i][:,0],indNeg[i][:,1],indNeg[i][:,2])
    return pos, neg


anim = FuncAnimation(fig, animate, frames=len(A), interval=500, fargs=(indPos, indNeg), blit=True, repeat=False)
writervideo = animation.FFMpegWriter(fps =1, bitrate =80)
anim.save("matrix_animation4.mp4")