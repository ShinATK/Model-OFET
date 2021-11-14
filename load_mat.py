from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

annots=  loadmat('20nm-120Vn.mat')
# print(annots.keys())
nmatrix = annots['nmatrix']

X = np.linspace(0, -120, 1201)
Y = np.linspace(0, 1000, 1001)

plt.contourf(X, Y, nmatrix)
plt.show()