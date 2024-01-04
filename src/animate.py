from matplotlib import animation
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess, platform
import auxiliary

import sys
import time
import threading

logger = None
# Create a threading event to signal when the task is done
done_flag = None

# If VISUAL is true, the animation will be shown at the end
def optionalVisualization(VISUAL, optimizationLog, outDir, SIZE, LOG):
    if VISUAL:
        global logger
        logger = auxiliary.setupLogger('second_logger', "scatterLog",  outDir, LOG)

        animationPath = os.path.join(outDir, "scatter.mp4")

        global done_flag
        done_flag = threading.Event()
        spinner_thread = threading.Thread(target=loading_spinner)
        spinner_thread.start()

        try:
            create(optimizationLog, animationPath, SIZE)
        finally:
            done_flag.set()
            spinner_thread.join()
            sys.stdout.write("\r")
            sys.stdout.flush()
            print("Animation complete!")
            user_input = input("Do you wish to open it now? (Y/N): ").strip().lower()
            if user_input == "y":
                print("Done!")
                if platform.system() == 'Darwin':       # macOS
                    subprocess.call(('open', animationPath))
                elif platform.system() == 'Windows':    # Windows
                    os.startfile(animationPath)
                else:                                   # linux variants
                    subprocess.call(('xdg-open', animationPath))
            else:
                print("Goodbye!")

def create(optimizationLog, animationPath, SIZE):
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

    freezeLastFrame(optimizationLog)
    optimizationLog_size = len(optimizationLog)

    plt.xlim(0, SIZE)
    plt.ylim(0, SIZE)

    indPos = []
    indNeg = []
    for p in range(optimizationLog_size):
        indPos.append(np.argwhere(optimizationLog[p]==1))
        indNeg.append(np.argwhere(optimizationLog[p]==-1))
        logger.info("Matrix Number " + str(p) + " has " + str(len(indPos[p])) + " positive and " + str(len(indNeg[p])) + " negative particles.")

    pos = ax.scatter(indPos[0][:,0],indPos[0][:,1],indPos[0][:,2], c='b', marker='o')
    neg = ax.scatter(indNeg[0][:,0],indNeg[0][:,1],indNeg[0][:,2], c='r', marker='o')

    anim = FuncAnimation(fig, animate, frames=optimizationLog_size, interval=200, fargs=(indPos, indNeg, pos, neg), blit=True, repeat=False)
    animation.FFMpegWriter(fps = 1, bitrate =80)
    anim.save(animationPath)

def animate(i, indPos, indNeg, pos, neg):
        pos._offsets3d = (indPos[i][:,0],indPos[i][:,1],indPos[i][:,2])
        neg._offsets3d = (indNeg[i][:,0],indNeg[i][:,1],indNeg[i][:,2])
        return pos, neg

def freezeLastFrame(optimizationLog):
    for _ in range(0, 10):
        lastFrame = optimizationLog[-1]
        optimizationLog.append(lastFrame)

def loading_spinner():
    chars = ["-", "\\", "|", "/"]
    i = 0
    while not done_flag.is_set():
        sys.stdout.write("\rPreparing Animation.. " + chars[i])
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(chars)