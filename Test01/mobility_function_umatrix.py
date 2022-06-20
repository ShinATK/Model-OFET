from scipy.io import loadmat
from scipy.io import savemat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy

# ===========================================================================
# 参数设置
# p=1e24 # 初始化电荷浓度
# E_eas=np.linspace(0, 3, 10000) # E_eas = E*e*a/sigma
sigma = 200 # 无序度 σ(meV) 如果无序度变化，这里设置为薄膜顶部的无序度
delta_sigma = -150 # 最大与最小无序度差值（分正负）
Vg = -120
mobility = np.zeros((1001, abs(Vg-1)))
kT=25.8 # meV
dv=-1
ds=10e-9 # 薄膜厚度
e=1.6e-19 # 元电荷
a=1e-9 # 预设晶格参数
u0=1e-5 # 本征迁移率
# sigma_up=sigma/kT
C1=1.8e-9
C2=0.42
# ===========================================================================
# 计算迁移率函数
def mobility_func_density(p, sigma):
    num_exp = 2 * (np.log(sigma ** 2 - sigma) - np.log(np.log(4))) / sigma ** 2
    return u0*C1*np.exp(-C2*sigma**2)*np.exp(0.5* (sigma**2 -sigma)*(2* p* a**3)**num_exp)
# E_eas = E*e*a/sigma
def mobility_func_field(V, sigma):
    return np.exp(0.44*((sigma/kT)**1.5 -2.2)*((1+0.8*(V*e*a/(ds*sigma))**2)**0.5-1))

def mobility_func(p, V, sigma):
    return mobility_func_density(p, sigma/kT)*mobility_func_field(V, sigma)

def disorder(i, delta_sigma, sigma0):
    if delta_sigma == 0:
        return sigma0
    else:
        return sigma0 + delta_sigma*(i/1000)

filename = str(sigma)+'+'+str(delta_sigma)+'meV20nm-120Vn'
annots = loadmat(f'./data/{filename}.mat')
# print(annots.keys())

nmatrix = annots['nmatrix']

X = np.arange(0, Vg-1, -1)
Y = np.arange(0, 1001, 1)

# 绘制nmatrix云图
fig,ax = plt.subplots()
ax.contourf(X, Y, nmatrix, vmin=0, vmax=1e26)
plt.title(f"Charge density {filename}")
# 自定义colorbar上下限
cmap1 = copy.copy(mpl.cm.viridis)
norm1 = mpl.colors.Normalize(vmin=0, vmax=1e26)
im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
cbar1 = fig.colorbar(im1, orientation='vertical')

plt.show()

for i in range(abs(Vg-1)):
    mobility_list = []
    V = dv*i
    for j in range(1001):
        mobility[j, i] = mobility_func(nmatrix[j, i], V, disorder(j, delta_sigma, sigma))

X = np.arange(0, Vg-1, -1)
Y = np.arange(0, 1001, 1)

# fig,ax = plt.subplots()
plt.contourf(X, Y, mobility, levels=1000, cmap='jet')
plt.colorbar()
plt.title(f"Mobility {filename}")

# # 自定义colorbar上下限
# cmap1 = copy.copy(mpl.cm.viridis)
# norm1 = mpl.colors.Normalize(vmin=1e-17, vmax=1e-14)
# im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
# cbar1 = fig.colorbar(im1, orientation='vertical')

plt.savefig(f'./output_mobility/mobility_{filename}.png', dpi=720)
plt.show()
savemat(f'./output_mobility/mobility_{filename}.mat', {'data': mobility})