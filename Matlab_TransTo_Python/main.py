# 导入第三方库
import numpy as np 
import matplotlib.pyplot as plt 

# 导入本地库
# from doping import doping
# 

e = 1.6e-19
a0 = 8.85e-12
KT = 0.0258*e

ds = 20e-9 	 # 薄膜厚度
L0 = 1e-4 # 沟道长度
W = 0.15 # 沟道宽度

N = 2000 	 # 横向分割份数
nd = 1000 # 纵向所分的份数

L=np.linspace(0, L0, N+1) # 初始化沟道长度
D=np.zeros(1, nd+1)
delta_y = ds/nd # 纵向单位长度
delta_L=L0/N # 横向单位长度

dds = 300e-9 # 介电层厚度
Ci = 11.9e-5 # 介电层电容


Vg_max = -1
Vg_min = -60
delta_Vg = 1

Va = -5 # 阈值电压

Vd = -20 # 漏极电压

dv = -1 # 导入网格的差值间隔，与泊松方程求解的矩阵横向电压步长一致

V = np.zeros((nd+1, N+1)) # 初始化网格电压

# 迁移率
q_0 = 50 # 无序度（meV）
q_up = q_0*1e-3*e/KT

a = 1e-9 # 晶格常数
C1 = 1.8e-9
C2 = 0.42
uu0 = 1e-5
u0 = uu0*C1*np.exp(-C2*(q_up)**2)
power_exp = 2*(np.log(q_up**2-q_up)-np.log(np.log(4))/q_up**2)

u = np.zeros((nd+1, N+1))
uu=1e-5 # 恒定空穴迁移率
uun=0 # 恒定电子迁移率

n=np.zeros(nd+, N+1) # 初始化网格电荷浓度
Res=np.ones(1, N-1) # 初始化网格误差
Resmax=1 # 残差最大值初值
Res_set=0.001 # 可容忍误差

Vg=Vg_min

I=np.zeros(1, round((Vg_max-Vg_min)/delta_Vg)+1) # 初始化存放电流
kk=1
VVG=np.arange(Vg_min, Vg_max, delta_Vg)

# 驻极体电荷分布并计算空间电场