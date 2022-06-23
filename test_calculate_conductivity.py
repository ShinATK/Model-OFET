import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

e=1.6e-19
d=20e-9 # 20nm
nd=1000
sigma=0.05 # 无序度 σ
a=1e-9
u0=1e-5 # 本征迁移率
kT=0.0258/e
# sigma_up=sigma/kT
C1=1.8e-9
C2=0.42

annots=loadmat('./Matrix/20nm-50Vn')
nmatrix=annots['nmatrix']

X=np.arange(0, 1001, 1)
Y=np.arange(0, 501, 1)

G=[]

def mobility_func_density(p, sigma_up):
    num_exp = 2 * (np.log(sigma_up ** 2 - sigma_up) - np.log(np.log(4))) / sigma_up ** 2
    return u0*C1*np.exp(-C2*sigma_up**2)*np.exp(0.5* (sigma_up**2 -sigma_up)*(2* p* a**3)**num_exp) *1e4
# E_eas = E*e*a/sigma
def mobility_func_field(E_eas, sigma_up):
    return np.exp(0.44*(sigma_up**1.5 -2.2)*((1+0.8*(E_eas)**2)**0.5-1))

def mobility_func(p, E_eas, sigma_up):
    return mobility_func_density(p, sigma_up)*mobility_func_field(E_eas, sigma_up)



	
	