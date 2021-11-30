import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def plotIndividumOverview(individumOverview, n , numberOfGenerations):
    X = np.arange(0,n,1)
    Y = np.arange(0,numberOfGenerations,1)
    X,Y = np.meshgrid(X,Y)
    Z = individumOverview[X,Y]

    #Transperent colors
    # get colormap
    ncolors = 256
    color_array = plt.get_cmap('rainbow')(range(ncolors))

    # change alpha values
    color_array[:,-1] = np.linspace(0.5,1,256)

    # create a colormap object
    cmap = LinearSegmentedColormap.from_list(name='rainbow_alpha',colors=color_array)

    # register this new colormap with matplotlib
    plt.register_cmap(cmap=cmap)
    fig = plt.figure()
    fig.set_size_inches(15, 8)
    fig.canvas.manager.set_window_title('Auswertung aller Individuen')

    ay = fig.add_subplot(111, projection='3d')
    ay.plot_surface(X=X,Y=Y,Z=Z, cmap='rainbow_alpha')
    ay.set_zlim(bottom=0)
    ay.set_xlabel('Individuen numeriert')
    ay.set_ylabel('Generationen')
    ay.set_zlabel('Fitness des Individums')

    plt.show()

        