from matplotlib import animation
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import logging


def create_animation(optimizationLog):
    logging.basicConfig(filename='..\out\scatter.log', encoding='utf-8', level=logging.INFO)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(25, 25), subplot_kw=dict(projection='3d')) # size of the figure and making it 3d
    ax.view_init(25,135)
    ax.set_axis_off()
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    optimizationLog_size = len(optimizationLog)

    plt.xlim(0, optimizationLog_size)
    plt.ylim(0, optimizationLog_size)

    indPos = []
    indNeg = []
    for p in range(optimizationLog_size):
        indPos.append(np.argwhere(optimizationLog[p]==1))
        indNeg.append(np.argwhere(optimizationLog[p]==-1))
        logging.info("Matrix Number " + str(p) + " has " + str(len(indPos[p])) + " positive and " + str(len(indNeg[p])) + " negative particles.")

    pos = ax.scatter(indPos[0][:,0],indPos[0][:,1],indPos[0][:,2], c='b', marker='o')
    neg = ax.scatter(indNeg[0][:,0],indNeg[0][:,1],indNeg[0][:,2], c='r', marker='o')

    anim = FuncAnimation(fig, animate, frames=optimizationLog_size, interval=200, fargs=(indPos, indNeg, pos, neg), blit=True, repeat=False)
    writervideo = animation.FFMpegWriter(fps = 1, bitrate =80)
    anim.save("..\out\scatter.mp4")

def animate(i, indPos, indNeg, pos, neg):
        pos._offsets3d = (indPos[i][:,0],indPos[i][:,1],indPos[i][:,2])
        neg._offsets3d = (indNeg[i][:,0],indNeg[i][:,1],indNeg[i][:,2])
        return pos, neg