from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy

# 获取data文件夹下数据名称
import os
def find_file():
    nmatrix_names_get = os.listdir('./data/density/')
    Vmatrix_names_get = os.listdir('./data/voltage/')
    nmatrix = []
    Vmatrix = []
    matrix = {'nmatrix':nmatrix, 'Vmatrix':Vmatrix}

    for each_n in nmatrix_names_get:
        if os.path.isdir(f"./data/density/{each_n}"):
            continue
        else:
            name = os.path.splitext(each_n)
            nmatrix.append(name[0])

    for each_V in Vmatrix_names_get:
        if os.path.isdir(f"./data/voltage/{each_V}"):
            continue
        else:
            name = os.path.splitext(each_V)
            Vmatrix.append(name[0])

    return matrix
matrix = find_file()


annots=  loadmat('./data/density/50meV-20Vn.mat')
# print(annots.keys())

nmatrix = annots['nmatrix']

X = np.arange(0, 41, 1)
Y = np.arange(0, 1001, 1)

plt.contourf(X, Y, nmatrix, levels=1000, cmap='jet')
plt.colorbar()
plt.show()