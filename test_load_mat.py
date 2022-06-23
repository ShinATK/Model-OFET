import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import math
from scipy.io import loadmat

path_set = 'Matrix/'


def load_files(path=path_set):
    # 读取 path 下的所有文件的文件名
    files_name = os.listdir(path)

    # 存储后缀名为mat的文件名称
    files_mat = []

    # 根据后缀名筛选出mat文件
    for each in files_name:
        files_extension = os.path.splitext(each)[1]
        # print(files_extension)
        if files_extension == '.mat':
            files_mat.append(each)
    # 按文件名排序
    files_mat.sort()
    return files_mat

def load_mat_data(path=path_set):
    mat_name = load_files(path)
    mat_name.sort()
    Vg = range(-61, -1, 1)
    I = dict()

    for each_name in mat_name:
        annots = loadmat(f'./Matrix/{each_name}')
        Imatrix = annots['I'][0, :]
        I[each_name[:-4]] = Imatrix

        plt.plot(Vg, Imatrix, label=each_name[:-4])

    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'style': 'italic',
            'size': 14
            }
    plt.xlabel('V$_g$ (V)', font)
    plt.ylabel('-I$_s$$_d$ (A)', font)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return I, mat_name

# 定义计算离散点导数的函数
def cal_deriv(x, y):  # x, y的类型均为列表
    diff_x = []  # 用来存储x列表中的两数之差
    for i, j in zip(x[0::], x[1::]):
        diff_x.append(j - i)

    diff_y = []  # 用来存储y列表中的两数之差
    for i, j in zip(y[0::], y[1::]):
        diff_y.append(j - i)

    slopes = []  # 用来存储斜率
    for i in range(len(diff_y)):
        slopes.append(diff_y[i] / diff_x[i])

    deriv = []  # 用来存储一阶导数
    for i, j in zip(slopes[0::], slopes[1::]):
        deriv.append(((i + j) / 2))  # 根据离散点导数的定义，计算并存储结果
    deriv.insert(0, slopes[0])  # (左)端点的导数即为与其最近点的斜率
    deriv.append(slopes[-1])  # (右)端点的导数即为与其最近点的斜率

    #for i in deriv:  # 打印结果，方便检查，调用时也可注释掉
    #     print(i)

    return deriv  # 返回存储一阶导数结果的列表

if __name__ == '__main__':


    I, mat_name = load_mat_data()

    e=1.6e-19
    L=3e-4 # 300μm
    W=3e-3 # 3mm
    C=11.9e-9 # F
    Vsd=-5 # V
    d=1e-8 # 10nm
    delta_d = 2e-9
    Vg = range(-61, -1, 1)

    k = dict()
    k_list = []

    G = dict()
    G_list = []

    n = dict()
    n_list = []

    N = dict()
    N_list = []

    mobility = dict()
    mobility_list = []

    i = 0
    A_list = []
    B = abs(L / (W * C * Vsd))

    for each_name in mat_name:
        A = abs(L / (W * (d - i * delta_d) * e))
        A_list.append(A)

        k[each_name[:-4]] = abs(cal_deriv(I[each_name[:-4]], Vg)[0])
        k_list.append(float(k[each_name[:-4]]))

        mobility[each_name[:-4]] = B * k[each_name[:-4]]
        mobility_list.append(mobility[each_name[:-4]])

        G[each_name[:-4]] = abs(I[each_name[:-4]] / Vsd)
        G_list.append(G[each_name[:-4]])

        n[each_name[:-4]] = A * G[each_name[:-4]] / mobility[each_name[:-4]]
        n_list.append(n[each_name[:-4]])

        N[each_name[:-4]] = n[each_name[:-4]] * (d - i * delta_d)
        N_list.append(N[each_name[:-4]])

        i += 1

    plt.subplot(2, 2, 1)
    plt.plot(G_list, label='G')
    plt.legend()
    plt.subplot(2, 2, 2)
    plt.plot(mobility_list, label='mobility')
    plt.legend()
    plt.subplot(2, 2, 3)
    plt.plot(n_list, label='n')
    plt.legend()
    plt.subplot(2, 2, 4)
    plt.plot(N_list, label='N')
    plt.legend()
    plt.tight_layout()
    plt.show()


