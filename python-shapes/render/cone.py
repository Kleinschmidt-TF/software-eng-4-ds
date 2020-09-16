from matplotlib import pyplot as plt
import numpy as np
from math import pi, cos, sin

def render_cone():
    z = np.arange(0, 1, 0.02)
    theta = np.arange(0, 2 * pi + pi / 50, pi / 50)

    fig = plt.figure()
    axes1 = fig.add_subplot(111, projection='3d')
    for zval in z:
        x = zval * np.array([cos(q) for q in theta])
        y = zval * np.array([sin(q) for q in theta])
        axes1.plot(x, y, -zval, 'b-',  alpha=0.5)

    plt.show()