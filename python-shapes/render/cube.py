import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def render_cube():
    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.array([[0,0,1,1],[0,0,1,1],[0,0,1,1],[0,0,1,1],[0,0,1,1]])
    Y = np.array([[0,0,0,0],[1,1,1,1],[1,1,1,1],[0,0,0,0],[0,0,0,0]])
    Z = np.array([[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,1,1,1],[0,0,0,0]])
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.5)
    plt.show()