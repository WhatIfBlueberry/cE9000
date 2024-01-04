import numpy as np
import matplotlib.pyplot as plt
from slatfatf import T0
import temperature
import time

def plotFigures(s,k,T,E,var, x,y,z):
    # Calculation of susceptibility
    # (as a moving average)
    #x = particleMatrix[:][0][0]
    #y = particleMatrix[0][:][0]
    #z = particleMatrix[0][0][:]
    span = 1000
    sus  = np.convolve(var, np.ones(span), 'valid') / span
    Tsus = T[span//2:-(span//2-1)]

    # Multiplot
    plt.clf()
    plt.suptitle(f"k={k}, T={T[k]:.2f}, E={E[k]:.0f}")

    # First plot shows spins
    ax1 = plt.subplot2grid((2, 2), (0, 0), projection = '3d')
    ax1.scatter(x, y, z, c=s, s=10, cmap='bwr')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])

    # Second plot shows energy over iterations
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax2.plot(E)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Energy")

    # Third plot shows susceptibility over temperature
    ax3 = plt.subplot2grid((2, 2), (0, 1))
    ax3.plot(Tsus,sus)
    ax3.invert_xaxis()
    ax3.yaxis.tick_right()
    ax3.set_ylim(0,1.5*np.max(sus[0:-sus.size//10]))
    ax3.set_xlabel("Temperature")
    ax3.set_ylabel("Variance")
    ax3.yaxis.set_label_position("right")

    # Fourth plot shows temperature over iterations
    ax4 = plt.subplot2grid((2, 2), (1, 1))
    ax4.plot(T)
    #ax4.plot(range(k+1), T[:k+1])
    ax4.set_xlabel("Iteration")
    ax4.set_ylabel("Temperature")
    ax4.yaxis.set_label_position("right")
    ax4.yaxis.tick_right()
    ax4.set_xlim(0,k)
    ax4.autoscale(enable=False, axis='x')
    ax4.set_ylim(min(T),max(T))


    plt.draw()
    plt.pause(0.001)
    plt.clf()
    #time.sleep(0.1)