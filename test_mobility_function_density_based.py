import numpy as np
import matplotlib.pyplot as plt

sigma=[50, 75, 100, 125, 150, 200] # 无序度 σ(meV)
e=1.6e-19
a=1e-9
u0=1e-5 # 本征迁移率
kT=0.0258 # 单位eV
# sigma_up=sigma/kT
C1=1.8e-9
C2=0.42


def mobility_func_density(p, sigma_up):
    num_exp = 2 * (np.log(sigma_up ** 2 - sigma_up) - np.log(np.log(4))) / sigma_up ** 2
    return u0*C1*np.exp(-C2*sigma_up**2)*np.exp(0.5* (sigma_up**2 -sigma_up)*(2* p* a**3)**num_exp) *1e4

p_density = np.linspace(1e21, 1e26, 10000)
mobility_list = []

sigma_up = [each/kT for each in sigma]

plt.subplot()
plt.axes(xscale='log',yscale='log')
plt.xlim([1e21, 1e26])
plt.ylim([1e-19, 1e-10])
plt.xlabel('Carrier Density m-3', fontsize=14)
plt.ylabel('Mobility cm3/(V·s)', fontsize=14)


for each in sigma:
    mobility_list = mobility_func_density(p_density, each*1e-3/kT)
    # np.savetxt(f'mobility_carrier_density sigma_up={each}.txt', mobility_list)
    plt.plot(p_density, mobility_list, 'o-', markersize=3,label=f'σ={each}meV')

plt.legend(loc='lower right')
plt.show()