import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd

from k_means import generate_centroids, assign_to_centroids, calculate_centroids

class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, x, y, groupings):
        self.numpoints = len(groupings)
        self.x = np.array(x)
        self.y = np.array(y)
        self.groupings = np.array(groupings)

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=500,
                                           frames=len(groupings), repeat_delay=1000,
                                           init_func=self.setup_plot, blit=False)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        c = self.groupings[0]
        self.scat = self.ax.scatter(self.x, self.y, c=c, cmap="viridis")

        # Find size based on the range of xs and ys
        self.ax.axis([min(self.x) - (max(self.x)-min(self.x))/10,
                     max(self.x) + (max(self.x)-min(self.x))/10,
                     min(self.y) - (max(self.y)-min(self.y))/10,
                     max(self.y) + (max(self.y)-min(self.y))/10])

        return self.scat,

    def update(self, i):
        """Update the scatter plot."""
        group = self.groupings[i]

        # Create a new plot with new c
        self.scat = self.ax.scatter(self.x, self.y, c=group, cmap="viridis")

        # Return updated scatterplot
        return self.scat,


if __name__ == '__main__':
    df = pd.read_csv('iris.csv')
    data = ['sepal_width', 'sepal_length']
    k = 3
    centroids = generate_centroids(df, k, data)
    groups = assign_to_centroids(df, centroids, data)

    x, y = df[data[0]], df[data[1]]

    groupings = [groups[:]]
    for count in range(100):
        if(centroids == calculate_centroids(df, centroids, groups, data)):
            print(f"Finished at PASS: ", count)
            break
        centroids = calculate_centroids(df, centroids, groups, data)
        groups = assign_to_centroids(df, centroids, data)
        groupings.append(groups[:])

    
    a = AnimatedScatter(x, y, groupings)
    plt.show()