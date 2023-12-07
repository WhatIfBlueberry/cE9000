from matplotlib import animation
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

def create_animation(optimizationLog):
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
    optimizationLog_size = len(optimizationLog[0][0])

    plt.xlim(0, optimizationLog_size)
    plt.ylim(0, optimizationLog_size)

    positiveIndex = [[] for _ in range(len(optimizationLog))]
    negativeIndex = [[] for _ in range(len(optimizationLog))]

    for i, outer_list in enumerate(optimizationLog):
        for j, inner_list in enumerate(outer_list):
            for k, item_list in enumerate(inner_list):
                for o, item in enumerate(item_list):
                    if item['spin'] == 1:
                        positiveIndex[i].append((i, j, k))
                    elif item['spin'] == -1:
                        negativeIndex[i].append((i, j, k))

    # Assuming positiveIndex and negativeIndex are defined somewhere above
    optimizationLogList = [(np.array(positiveIndex[i]), np.array(negativeIndex[i])) for i in range(len(positiveIndex))]

    fig, ax = plt.subplots()

    pos = ax.scatter([], [], [], c='b', marker='o')
    neg = ax.scatter([], [], [], c='r', marker='o')

    def animate(i, optimizationLogList):
        pos._offsets3d = (optimizationLogList[i][0][:,0], optimizationLogList[i][0][:,1], optimizationLogList[i][0][:,2])
        neg._offsets3d = (optimizationLogList[i][1][:,0], optimizationLogList[i][1][:,1], optimizationLogList[i][1][:,2])
        return pos, neg

    anim = FuncAnimation(fig, animate, frames=len(optimizationLogList), interval=200, fargs=(optimizationLogList,), blit=True, repeat=False)

    writervideo = animation.FFMpegWriter(fps =10, bitrate =80)
    anim.save("../out/optimizationLog_animation.mp4")
