# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 01:27:38 2025

@author: Vladimir
"""
import matplotlib.pyplot as plt


def separator (data):
    #Раскидываем на разные установки
    # 0 1    2    3     4     5     6        7         8  9  10    11  12      13  14  15  16  
    # # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny
    
    pole_dipole = list()
    dipole_dipole = list()
    schlumberger  = list()
    
    for i in range(len(data)):
        A = list()
        B = list()
        M = list()
        N = list()
        if data[i][2] == 99999.999 or data[i][3] == 99999.999:
            pole_dipole.append(data[i])
        else:
            A = [data[i][2], data[i][13]]
            B = [data[i][3], data[i][14]]
            M = [data[i][4], data[i][15]]
            N = [data[i][5], data[i][16]]
            # реализовать через середину отрезков и совпадение центров
            OAB = [(A[0]+B[0])/2, (A[1]+B[1])/2]
            OMN = [(M[0]+N[0])/2, (M[1]+N[1])/2]
            if OAB == OMN and A[1] == M[1] == N[1] == B[1]:
                schlumberger.append(data[i])
            else:
                dipole_dipole.append(data[i])
                

    return pole_dipole, dipole_dipole, schlumberger




def filter_array(array, min_ROK, max_ROK, param_index):
    """
    Фильтрует массив по значениям ROK.
    :param array: Исходный массив.
    :param min_ROK: Минимальное значение ROK.
    :param max_ROK: Максимальное значение ROK.
    :return: Отфильтрованный массив.
    """
    filtered_array = list()
    for item in array:
        if min_ROK <= item[param_index] <= max_ROK:  # Проверяем, что значение ROK в диапазоне
            filtered_array.append(item)
    return filtered_array



def gistogramma(array, a, title):
    # Выбираем массив, индекс и подпись
    data = [row[a] for row in array]  # Более компактный способ
    
    n = int((len(array))**(0.5))  # Количество бинов
    fig, ax = plt.subplots()
    
    # Заголовок
    ax.set_title(title, fontsize=6)  # Размер шрифта заголовка
    
    # Сетка
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=':')
    
    # Гистограмма
    ax.hist(data, bins=n)
    ax.set_xscale('log')
    
    # Размер шрифта для меток осей
    ax.tick_params(axis='both', which='major', labelsize=6)  # Размер шрифта меток
    ax.set_xlabel('Значения', fontsize=6)  # Размер шрифта подписи оси X
    ax.set_ylabel('Частота', fontsize=6)   # Размер шрифта подписи оси Y

    return fig  # Возвращаем объект Figure


