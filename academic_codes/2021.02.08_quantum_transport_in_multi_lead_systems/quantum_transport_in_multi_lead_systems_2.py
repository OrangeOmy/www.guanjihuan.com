"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6075
"""

import numpy as np
import time
import guan

def lead_matrix_00(y):  
    h00 = np.zeros((y, y))
    for y0 in range(y-1):
        h00[y0, y0+1] = 1
        h00[y0+1, y0] = 1
    return h00


def lead_matrix_01(y):
    h01 = np.identity(y)
    return h01


def scattering_region(x, y):
    h = np.zeros((x*y, x*y))
    for x0 in range(x-1):
        for y0 in range(y):
            h[x0*y+y0, (x0+1)*y+y0] = 1 # x方向的跃迁
            h[(x0+1)*y+y0, x0*y+y0] = 1
    for x0 in range(x):
        for y0 in range(y-1):
            h[x0*y+y0, x0*y+y0+1] = 1 # y方向的跃迁
            h[x0*y+y0+1, x0*y+y0] = 1 
    return h


def main():
    start_time = time.time()
    width = 5
    length = 50 
    fermi_energy_array = np.arange(-4, 4, .01)

    # 中心区的哈密顿量
    H_scattering_region = scattering_region(x=length, y=width)

    # 电极的h00和h01
    lead_h00 = lead_matrix_00(width)
    lead_h01 = lead_matrix_01(width)
    
    transmission_12_array = []
    transmission_13_array = []
    transmission_14_array = []
    transmission_15_array = []
    transmission_16_array = []
    transmission_1_all_array = []

    for fermi_energy in fermi_energy_array:
        print(fermi_energy)
        #   几何形状如下所示：
        #               lead2         lead3
        #   lead1(L)                          lead4(R)  
        #               lead6         lead5 

        # 电极到中心区的跃迁矩阵
        h_lead1_to_center = np.zeros((width, width*length), dtype=complex)
        h_lead2_to_center = np.zeros((width, width*length), dtype=complex)
        h_lead3_to_center = np.zeros((width, width*length), dtype=complex)
        h_lead4_to_center = np.zeros((width, width*length), dtype=complex)
        h_lead5_to_center = np.zeros((width, width*length), dtype=complex)
        h_lead6_to_center = np.zeros((width, width*length), dtype=complex)
        for i0 in range(width):
            h_lead1_to_center[i0, i0] = 1
            h_lead2_to_center[i0, width*i0+(width-1)] = 1
            h_lead3_to_center[i0, width*(length-1-i0)+(width-1)] = 1
            h_lead4_to_center[i0, width*(length-1)+i0] = 1
            h_lead5_to_center[i0, width*(length-1-i0)+0] = 1
            h_lead6_to_center[i0, width*i0+0] = 1
        # 自能    
        self_energy1, gamma1 = guan.self_energy_of_lead_with_h_lead_to_center(fermi_energy, lead_h00, lead_h01, h_lead1_to_center)
        self_energy2, gamma2 = guan.self_energy_of_lead_with_h_lead_to_center(fermi_energy, lead_h00, lead_h01, h_lead2_to_center)
        self_energy3, gamma3 = guan.self_energy_of_lead_with_h_lead_to_center(fermi_energy, lead_h00, lead_h01, h_lead3_to_center)
        self_energy4, gamma4 = guan.self_energy_of_lead_with_h_lead_to_center(fermi_energy, lead_h00, lead_h01, h_lead4_to_center)
        self_energy5, gamma5 = guan.self_energy_of_lead_with_h_lead_to_center(fermi_energy, lead_h00, lead_h01, h_lead5_to_center)
        self_energy6, gamma6 = guan.self_energy_of_lead_with_h_lead_to_center(fermi_energy, lead_h00, lead_h01, h_lead6_to_center)

        # 整体格林函数
        green = np.linalg.inv(fermi_energy*np.eye(width*length)-H_scattering_region-self_energy1-self_energy2-self_energy3-self_energy4-self_energy5-self_energy6)

        # Transmission
        transmission_12 = np.trace(np.dot(np.dot(np.dot(gamma1, green), gamma2), green.transpose().conj()))
        transmission_13 = np.trace(np.dot(np.dot(np.dot(gamma1, green), gamma3), green.transpose().conj()))
        transmission_14 = np.trace(np.dot(np.dot(np.dot(gamma1, green), gamma4), green.transpose().conj()))
        transmission_15 = np.trace(np.dot(np.dot(np.dot(gamma1, green), gamma5), green.transpose().conj()))
        transmission_16 = np.trace(np.dot(np.dot(np.dot(gamma1, green), gamma6), green.transpose().conj()))
        transmission_12_array.append(np.real(transmission_12))
        transmission_13_array.append(np.real(transmission_13))
        transmission_14_array.append(np.real(transmission_14))
        transmission_15_array.append(np.real(transmission_15))
        transmission_16_array.append(np.real(transmission_16))
        transmission_1_all_array.append(np.real(transmission_12+transmission_13+transmission_14+transmission_15+transmission_16))
    
    guan.plot(fermi_energy_array, transmission_12_array, xlabel='Fermi energy', ylabel='Transmission_12')
    guan.plot(fermi_energy_array, transmission_13_array, xlabel='Fermi energy', ylabel='Transmission_13')
    guan.plot(fermi_energy_array, transmission_14_array, xlabel='Fermi energy', ylabel='Transmission_14')
    guan.plot(fermi_energy_array, transmission_15_array, xlabel='Fermi energy', ylabel='Transmission_15')
    guan.plot(fermi_energy_array, transmission_16_array, xlabel='Fermi energy', ylabel='Transmission_16')
    guan.plot(fermi_energy_array, transmission_1_all_array, xlabel='Fermi energy', ylabel='Transmission_1_all')
    end_time = time.time()
    print('运行时间=', end_time-start_time)


if __name__ == '__main__':
    main()