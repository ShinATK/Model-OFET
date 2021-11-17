import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt 
import math
from scipy.io import loadmat

annots_n = loadmat('./Matrix/20nm-50Vn')
annots_V = loadmat('./Matrix/20nm-50VV')
nmatrix = annots_n['nmatrix']
Vmatrix = annots_V['Vmatrix']

ds = 20e-9 # 薄膜厚度
L = 3e-4 # 沟道长度
W = 3e-2 # 沟道宽度

nd = 1000 # 薄膜纵向分割份数
N = 2000 # 沟道长度方向（横向分割份数）
delta_y = ds/nd


V=np.zeros((nd+1, N+1)) # 初始化薄膜内部电势矩阵
n=np.zeros((nd+1, N+1)) # 初始化薄膜内部载流子浓度矩阵

Vd = -20 # 漏极电压
Vs = 0 # 源极电压
Vsd = Vd - Vs # 源漏电压
# 根据源漏电压初始化器件上表面电势
delta_Vsd = Vsd/N
for i in range(0, N+1):
	V[0, i] = delta_Vsd * i + Vs

Va = 0 # 阈值电压

# Vg_max = -0.5
# Vg_min = -40
# delta_Vg = 0.5
# Vg = np.arange(-40, -20, 0.5)
Vg = 0

V_temp = V[0, :]
# 假设器件0V即可关闭（即无掺杂）
delta_v = 1 # 与泊松方程计算得到的矩阵横向电压步长相同
for i in range(N+1):
	b = math.floor((Vg-V[0, i])/delta_v)
	V[:, i] = Vmatrix[:, b] - ((Vg-V[0, i])/delta_v-b)*(Vmatrix[:, b+1]-Vmatrix[:, b])
	n[:, i] = nmatrix[:, b] - ((Vg-V[0, i])/delta_v-b)*(nmatrix[:, b+1]-nmatrix[:, b])


fig,ax = plt.subplots()
ax.contourf(n)
plt.show()