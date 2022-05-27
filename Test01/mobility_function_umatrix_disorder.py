from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy
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

    # for each_V in Vmatrix_names_get:
    #     if os.path.isdir(f"./data/voltage/{each_V}"):
    #         continue
    #     else:
    #         name = os.path.splitext(each_V)
    #         Vmatrix.append(name[0])

    return nmatrix
# # X = np.linspace(0, -50, 501)
# X = np.arange(0, -121, -1)
# Y = np.arange(0, 1001, 1)
#
# # 绘制nmatrix云图
# fig,ax = plt.subplots()
# ax.contourf(X, Y, nmatrix, vmin=0, vmax=1e26)
# # 自定义colorbar上下限
# cmap1 = copy.copy(mpl.cm.viridis)
# norm1 = mpl.colors.Normalize(vmin=0, vmax=1e26)
# im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
# cbar1 = fig.colorbar(im1, orientation='vertical')
# plt.show()
# ===========================================================================

# 参数设置
# p=1e24 # 初始化电荷浓度
# E_eas=np.linspace(0, 3, 10000) # E_eas = E*e*a/sigma
mobility = np.zeros((1001, 41))

sigma=100 # 无序度 σ(meV) 定值/薄膜顶部
each ='100meV-20Vn'

kT=25.8 # meV
dv=-0.5
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

def disorder_incr(i, delta_sigma, sigma0=50):
    return sigma0 + abs(delta_sigma)*(i/1000)
def disorder_decr(i, delta_sigma, sigma0=100):
    return sigma0 - abs(delta_sigma) * (i/1000)

# ===========================================================================

annots = loadmat(f'./data/density/{each}.mat')
# print(annots.keys())
nmatrix = annots['nmatrix']

for i in range(41):
    mobility_list = []
    V = dv*i
    for j in range(1001):
        # 只考虑电荷密度对迁移率影响
        mobility[j, i] = mobility_func_density(nmatrix[j, i], sigma / kT)
        # mobility[j, i]=mobility_func_density(nmatrix[j, i], disorder_incr(j, 100, sigma)/kT) # 无序度沿膜厚线性增加
        # mobility[j, i] = mobility_func_density(nmatrix[j, i], disorder_decr(j, 100, sigma)/kT) # 无序度沿膜厚线性减小

        # 同时考虑电荷密度与电势对迁移率的影响
        # mobility[j, i] = mobility_func(nmatrix[j, i], V, sigma)
        # mobility[j, i]=mobility_func(nmatrix[j, i], V, disorder_incr(j, 100, sigma)) # 无序度沿膜厚线性增加
        # mobility[j, i] = mobility_func(nmatrix[j, i], V, disorder_decr(j, 100, sigma)) # 无序度沿膜厚线性减小

# for i in range(41):
#     mobility_list = []
#     # p = nmatrix[:, i]
#     V = dv*i
#     for j in range(1001):
#         # mobility[j, i]=mobility_func(p[i], V, sigma)
#         mobility[j, i] = mobility_func_density(nmatrix[j, i], sigma/kT)

# X = np.arange(0, 20, 0.5)
# Y = np.arange(0, 20, 0.02)


X = np.linspace(0, -20, 41, endpoint=True)
Y = np.linspace(20, 0, 1001, endpoint=True)

plt.contourf(X, Y, mobility*1e6, levels=1000, cmap='jet')
plt.colorbar()

font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size':20
        }
plt.xlabel('Vg(V)', font)
plt.ylabel('Film Depth(nm)', font)

name = 'Constant Disorder σ=100meV'
# name = 'Disorder Increase Δσ=+100meV'
# name = 'Disorder Decrease Δσ=-100meV'
plt.title(f"{name}", font)
plt.show()

# # 不同栅压下，迁移率随膜厚位置不同的变化
# for i in range(0, 45, 10):
#
#     V = i * dv
#     plt.plot(np.linspace(0, 20, 1001, endpoint=True), mobility[:, i]*1e6, label=f"Vg= {V}V")
# font = {'family': 'Times New Roman',
#         'weight': 'normal',
#         'size':20
#         }
# plt.xlabel('Film Depth(nm)', font)
# plt.ylabel('Mobility(cm3/(V·s))', font)
# plt.legend()
# plt.show()

#
