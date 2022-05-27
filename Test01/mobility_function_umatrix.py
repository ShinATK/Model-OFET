from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy



# annots= loadmat('50meV20nm-120Vn.mat') # 无序度沿膜厚方向为定值
annots=  loadmat('50+50meV20nm-120Vn.mat') # 无序度沿膜厚方向线性增加
# annots= loadmat('100-50meV20nm-120Vn.mat') # 无序度沿膜厚方向线性减小
# print(annots.keys())

nmatrix = annots['nmatrix']

X = np.arange(0, -121, -1)
Y = np.arange(0, 1001, 1)

# 绘制nmatrix云图
fig,ax = plt.subplots()
ax.contourf(X, Y, nmatrix, vmin=0, vmax=1e26)
plt.title("Charge density")
# 自定义colorbar上下限
cmap1 = copy.copy(mpl.cm.viridis)
norm1 = mpl.colors.Normalize(vmin=0, vmax=1e26)
im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
cbar1 = fig.colorbar(im1, orientation='vertical')

plt.show()
# ===========================================================================

# 参数设置
# p=1e24 # 初始化电荷浓度
# E_eas=np.linspace(0, 3, 10000) # E_eas = E*e*a/sigma
mobility = np.zeros((1001, 121))
sigma=50 # 无序度 σ(meV)
kT=25.8 # meV
dv=-0.1
ds=20e-9 # 薄膜厚度
e=1.6e-19 # 元电荷
a=1e-9 # 预设晶格参数
u0=1e-5 # 本征迁移率
# sigma_up=sigma/kT
C1=1.8e-9
C2=0.42


# 计算迁移率函数
def mobility_func_density(p, sigma):
    num_exp = 2 * (np.log(sigma ** 2 - sigma) - np.log(np.log(4))) / sigma ** 2
    return u0*C1*np.exp(-C2*sigma**2)*np.exp(0.5* (sigma**2 -sigma)*(2* p* a**3)**num_exp)
# E_eas = E*e*a/sigma
def mobility_func_field(V, sigma):
    return np.exp(0.44*((sigma/kT)**1.5 -2.2)*((1+0.8*(V*e*a/(ds*sigma))**2)**0.5-1))

def mobility_func(p, V, sigma):
    return mobility_func_density(p, sigma/kT)*mobility_func_field(V, sigma)

def disorder_decr(i, delta_sigma, sigma0=50):
    return sigma0 + abs(delta_sigma)*(1-i/1000)
def disorder_incr(i, delta_sigma, sigma0=50):
    return sigma0 + abs(delta_sigma) * (i / 1000)

# ===========================================================================
for i in range(121):
    mobility_list = []
    V = dv*i
    for j in range(1001):
        mobility[j, i]=mobility_func(nmatrix[j, i], V, disorder_incr(j, 50))
        # mobility[j, i] = mobility_func(nmatrix[j, i], V, disorder_decr(j, 50))
        # mobility[j, i] = mobility_func_density(nmatrix[j, i], disorder_incr(j, 50)/kT)

X = np.arange(0, -121, -1)
Y = np.arange(0, 1001, 1)

fig,ax = plt.subplots()
ax.contourf(X, Y, mobility)
plt.title("Mobility with Charge density & Field")

# 自定义colorbar上下限
cmap1 = copy.copy(mpl.cm.viridis)
norm1 = mpl.colors.Normalize(vmin=1e-17, vmax=1e-14)
im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
cbar1 = fig.colorbar(im1, orientation='vertical')

plt.show()