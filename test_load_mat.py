from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy

annots=  loadmat('./Matrix/20nm-50Vn.mat')
# print(annots.keys())
nmatrix = annots['nmatrix']

# X = np.linspace(0, -50, 501)
X = np.arange(0, -50.1, -0.1)
Y = np.arange(0, 1001, 1)

fig,ax = plt.subplots()

ax.contourf(X, Y, nmatrix, vmin=0, vmax=1e25)

# 自定义colorbar上下限
cmap1 = copy.copy(mpl.cm.viridis)
norm1 = mpl.colors.Normalize(vmin=0, vmax=1e25)
im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
cbar1 = fig.colorbar(im1, orientation='vertical')

plt.show()