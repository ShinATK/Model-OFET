import matplotlib.pyplot as plt
import numpy as np

sigma=0.05 # 无序度 σ

sigma_up = [2,3,4,5,6] # sigma_up=sigma/kT

e=1.6e-19
a=1e-9
kT=0.0258/e
u0=1e-5 # 本征迁移率


# E_eas = E*e*a/sigma
def mobility_func_field(E_eas, sigma_up):
    return np.exp(0.44*(sigma_up**1.5 -2.2)*((1+0.8*(E_eas)**2)**0.5-1))
    
    
E_eas=np.linspace(0, 6, 10000)
mobility_list=[]
sigma_up=[2,3,4,5,6]

plt.subplot()
plt.axes(yscale='log')
plt.xlabel('Field V/m', fontsize=14)
plt.ylabel('Mobility cm3/(V·s)', fontsize=14)

for each in sigma_up:
    mobility_list = mobility_func_field(E_eas, each)
    np.savetxt(f'mobility_filed_dependent sigma_up={each}.txt', mobility_list)
    plt.plot(E_eas, mobility_list, 'o', markersize=3, label=f'σ/kT={each}')   
plt.legend()
plt.show()
