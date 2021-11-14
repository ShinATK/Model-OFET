from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy

annots=  loadmat('20nm-120Vn.mat')
# print(annots.keys())
nmatrix = annots['nmatrix']

X = np.linspace(0, -120, 1201)
Y = np.linspace(0, 1000, 1001)

fig,ax = plt.subplots()

ax.contourf(X, Y, nmatrix, vmin=0, vmax=1e25)

# 自定义colorbar上下限
cmap1 = copy.copy(mpl.cm.viridis)
norm1 = mpl.colors.Normalize(vmin=0, vmax=1e25)
im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
cbar1 = fig.colorbar(im1, orientation='vertical')

plt.show()