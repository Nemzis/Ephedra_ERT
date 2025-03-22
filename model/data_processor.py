# -*- coding: utf-8 -*-
'''
Created on Mon Mar  3 01:27:38 2025

@author: Vladimir
'''
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import math #мат библиотека


def separator (data, x, y, r):
    #Раскидываем на разные установки
    # 0 1    2    3     4     5     6        7         8  9  10    11  12      13  14  15  16  
    # # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny
    
    pole_dipole = list()
    
    pole_dipole_X_sistem = list()
    pole_dipole_L_sistem = list()
    
    dipole_dipole = list()
    
    dipole_dipole_X_sistem = list()
    dipole_dipole_L_sistem = list()
    
    schlumberger  = list()
    
    data = multiply_data(data, x, y, r)
    
    
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
                
    if pole_dipole:
        for i in range(len(pole_dipole)):
            if pole_dipole[i][4] == pole_dipole[i][5] or pole_dipole[i][15] == pole_dipole[i][16]:
                pole_dipole_L_sistem.append(pole_dipole[i])
            else:
                pole_dipole_X_sistem.append(pole_dipole[i])
                
        
    if dipole_dipole:
        for i in range(len(dipole_dipole)):
            if dipole_dipole[i][4] == dipole_dipole[i][5] or dipole_dipole[i][15] == dipole_dipole[i][16]:
                dipole_dipole_L_sistem.append(dipole_dipole[i])
            else:
                dipole_dipole_X_sistem.append(dipole_dipole[i])
  
    
    if schlumberger:
        pass              

    return pole_dipole, pole_dipole_X_sistem, pole_dipole_L_sistem, dipole_dipole, dipole_dipole_L_sistem, dipole_dipole_X_sistem, schlumberger




def filter_array(array, min_ROK, max_ROK, param_index):
    '''
    Фильтрует массив по значениям ROK.
    :param array: Исходный массив.
    :param min_ROK: Минимальное значение ROK.
    :param max_ROK: Максимальное значение ROK.
    :return: Отфильтрованный массив.
    '''
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
    ax.set_ylabel('Частость', fontsize=6)   # Размер шрифта подписи оси Y
    
    plt.close(fig)
    
    return fig  # Возвращаем объект Figure




def plot(array, a, b):
    """
    Функция для построения графика.
    :param array: Многомерный массив с данными.
    :param a: Индекс для оси X.
    :param b: Индекс для оси Y.
    :return: Объект Figure с графиком.
    """
    fig = Figure(figsize=(5, 3))  # Создаём объект Figure
    ax = fig.add_subplot(111)  # Добавляем оси

    # Создаём списки для значений X и Y
    x = [row[a] for row in array]  # Берём значение из столбца `a` для каждой строки
    y = [row[b] for row in array]  # Берём значение из столбца `b` для каждой строки

    # Строим график
    ax.set_title('Электроды', fontsize=7)
    
    ax.plot(x, y, 'go', markersize=3)  # 'go' — зелёные кружки
    ax.set_xlabel('X (м)', fontsize=6)  # Подпись оси X
    ax.set_ylabel('Y (м)', fontsize=6)  # Подпись оси Y
    ax.grid(which='major', linestyle=':')  # Сетка с пунктирными линиями

    # Устанавливаем размер шрифта для цифр на осях
    ax.tick_params(axis='both', which='major', labelsize=6)  # Размер шрифта для меток осей

    fig.tight_layout()  # Улучшенное расположение элементов

    return fig  # Возвращаем объект Figure
  


def Rok_3D2D (array, type_array):
    #стандартный рассчет Рок для трехэл формирование списка
    #v 3.0
    #         Ax   Bx    Mx    Nx   
    # 0 1    2    3     4     5     6        7         8  9  10    11  12      13  14  15  16  
    # # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny
    
    Rok_data = []
    key_M = 0
    if len(array[0]) > 17:
        key_M = 1

    for i in range(len(array)):
        v = array[i][8]
        a = array[i][9]
        
       
        if type_array == 'Pole-Dipole':
            #pole-dipole
            #x = MN/2
            #z = AO/3
            x = (array[i][4] + array[i][5])/2
            y = (array[i][15] + array[i][16])/2
            z = -((x - array[i][2])**2 + (y - array[i][13])**2)**(0.5)/3

        elif type_array == 'Dipole-Dipole':
            #dipole-dipole
            #x = (B+M)/2
            #z = OO`/2  
            x = (array[i][3] + array[i][4])/2
            y = (array[i][14] + array[i][15])/2
            Ox = (array[i][2] + array[i][3])/2
            Oy = (array[i][13] + array[i][14])/2
            Ox2 = (array[i][4] + array[i][5])/2
            Oy2 = (array[i][15] + array[i][16])/2
            z = -((Ox - Ox2)**2 + (Oy - Oy2)**2)**(0.5)/2
            
        elif type_array == 'Schlumberge':
            #schlumberger
            #x = (M+N)/2
            #z = AB/2
            x = (array[i][4] + array[i][5])/2
            y = (array[i][15] + array[i][16])/2
            z = -((array[i][2] - array[i][3])**2 + (array[i][13] - array[i][14])**2)**(0.5)/2
        else:
            pass
            
        z = round(z, 3)
        r = array[i][1]
        log_r = math.log(r)
        
        if key_M == 1:
            m = array[i][37]
            Rok_data.append([x, y, z, r, log_r, v, a, m])
        else:
            Rok_data.append([x, y, z, r, log_r, v, a])

    return Rok_data




def multiply_data(array, x, y, r):
    if x and x != '0':
        x = float(x)
        multiply_id = [2, 3, 4, 5] 
        for row in array:
            for m in multiply_id:
                if isinstance(row[m], (int, float)) and row[m] != 99999.999:
                    row[m] = row[m] * x
                    row[m] = round(row[m], 2)
                else:
                    continue                      
    if y and y != '0':
        y = float(y)
        multiply_id_2 = [13, 14, 15, 16] 
        for row in array:
            for m in multiply_id_2:
                if isinstance(row[m], (int, float)) and row[m] != 99999.999:
                    row[m] = row[m] * y
                    row[m] = round(row[m], 2)
                else:
                    continue
      
    if r and r != '0':
        r = float(r)
        for row in array:
            if isinstance(row[1], (int, float)):
                row[1] = row[1] * r
                row[1] = round(row[1], 4)
     
    return array













