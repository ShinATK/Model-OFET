import numpy as np
import matplotlib.pyplot as plt

sigma=0.05 # 无序度 σ
e=1.6e-19
a=1e-9
u0=1e-5 # 本征迁移率
kT=0.0258/e
# sigma_up=sigma/kT
C1=1.8e-9
C2=0.42


def mobility_func_density(p, sigma_up):
    num_exp = 2 * (np.log(sigma_up ** 2 - sigma_up) - np.log(np.log(4))) / sigma_up ** 2
    return u0*C1*np.exp(-C2*sigma_up**2)*np.exp(0.5* (sigma_up**2 -sigma_up)*(2* p* a**3)**num_exp) *1e4
# E_eas = E*e*a/sigma
def mobility_func_field(E_eas, sigma_up):
    return np.exp(0.44*(sigma_up**1.5 -2.2)*((1+0.8*(E_eas)**2)**0.5-1))

def mobility_func(p, E_eas, sigma_up):

	return mobility_func_density(p, sigma_up)*mobility_func_field(E_eas, sigma_up)

# p_density = np.linspace(1e21, 1e25, 10000)
p_density=1e22
E_eas=np.linspace(0, 3, 10000)
mobility_list = []
sigma_up = [2,3,4,5,6]

plt.subplot()
# plt.xlim([1e21, 1e25])
# plt.ylim([1e-16, 1e-10])
plt.axes(yscale='log')
plt.xlabel('Field V/m', fontsize=14)
plt.ylabel('Mobility cm3/(V·s)', fontsize=14)


for each in sigma_up:
    mobility_list = mobility_func(p_density, E_eas, each)
    # np.savetxt(f'mobility_func sigma_up={each}.txt', mobility_list)
    plt.plot(E_eas, mobility_list, 'o', markersize=3,label=f'σ/kT={each}')

plt.legend()
plt.show()