import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import util
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# #############################################################################
# Generate sample data
targets = util.create_dataset()
connector_array = [[t['x'] , t['y'], t['z']] for t in targets]
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)


# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=500,metric=util.calculate_distance_cart, min_samples=3).fit(connector_array)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
_labels = db.labels_
print(_labels)
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(_labels)) - (1 if -1 in _labels else 0)
n_noise_ = list(_labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# print(connector_array)
def init():
    for i in range(len(connector_array)):
        ax.scatter(connector_array[i][0],connector_array[i][1],connector_array[i][2], label=_labels[i])
    return fig,
# ax.scatter([e[0] for e in connector_array],[e[1] for e in connector_array],[e[2] for e in connector_array])
# ax.set_label(_labels)
plt.show()
ax = Axes3D(fig)

# Create an init function and the animate functions.
# Both are explained in the tutorial. Since we are changing
# the the elevation and azimuth and no objects are really
# changed on the plot we don't have to return anything from
# the init and animate function. (return value is explained
# in the tutorial.
def randrange(n, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin
n = 100
xx = randrange(n, 23, 32)
yy = randrange(n, 0, 100)
zz = randrange(n, -50, -25)
def init():
    for i in range(len(connector_array)):
        ax.scatter(connector_array[i][0],connector_array[i][1],connector_array[i][2], label=_labels[i])
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
# Save
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])