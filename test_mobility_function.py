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


def mobility_func(p, sigma_up):
    num_exp = 2 * (np.log(sigma_up ** 2 - sigma_up) - np.log(np.log(4))) / sigma_up ** 2
    return u0*C1*np.exp(-C2*sigma_up**2)*np.exp(0.5* (sigma_up**2 -sigma_up)*(2* p* a**3)**num_exp)

p_density = np.linspace(1e21, 1e25, 10000)
mobility_list = []
sigma_up = [2,3,4,5,6]

for each in sigma_up:
    mobility_list = mobility_func(p_density, each)
    np.savetxt(f'mobility sigma_up={each}.txt', mobility_list)
    plt.plot(p_density, mobility_list, label=f'σ/kT={each}')

plt.legend()
plt.show()