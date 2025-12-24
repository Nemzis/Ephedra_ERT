# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:49:21 2025

@author: Vladimir
'''

# 0 1    2    3     4     5     6        7         8  9  10    11  12      13  14  15  16  
# # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny

#with SP
#  0    1       2       3        4        5        6            7            8     9     10    11    12      13    14    15    16   
#['#', 'Rho', 'Spa.1', 'Spa.2', 'Spa.3', 'Spa.4', 'PassTime', 'DutyCycle', 'Vp', 'In', '888', 'K', 'Phase', 'Ay', 'By', 'My', 'Ny',

#  17     18   19     20    21    22    23    24   25     26    27     28      29     30    31      32     33     34     35     36    37 
#  M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20', 'M']

import os



#гармоники пока что отбрасываюься

def mass_load_files (path_f):
    file_list = os.listdir(path_f)
    
    array = list()
    for i in range(len(file_list)):
        with open(path_f + '\\' + file_list[i], 'r') as f:
            array += f.readlines() 
    
    for i in range(len(array)):
        array[i] = array[i].replace('\n', '')
        array[i] = array[i].split('\t')

        try:
            array[i] = list(map(float, array[i]))
        except ValueError:
            continue
        
    SP = 'Данные без ВП'
    if array[0][2] == 'M1':
        SP = 'Данные с ВП, основная гармоника перенесена в конец массива'
        #номера гармоник в массиве
        list_SP = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        array_SP = []
        for i in range(len(array)):
            a = []
            for item in list_SP:
                a.extend([array[i][item]])
            array_SP.append(a)
            
        # Удаление столбцов*
        result = [[item for i, item in enumerate(row) if i not in list_SP] for row in array]
    
        #добавляем столбец для равенства массивов
        for i in range(len(result)):
            result[i].insert(10, '888')
            #list.insert(index, element)
    
        # Соединение по горизонтали
        array = [row1 + row2 for row1, row2 in zip(result, array_SP)]
    
    a = 0
    b = 0
    c = 0 
    i = len(array)-1
    while i >= 0:
        if array[i][1] == 'Rho':
            del array[i]
            a += 1
        elif array[i][2] == 99999.999 and array[i][3] == 99999.999:
            del array[i]
            b += 1
        elif array[i][4] == 99999.999 or array[i][5] == 99999.999:
            del array[i]
            c += 1
            
        i -= 1
    return array, a, b, c, SP





def load_file(path):
    array = []
    head = []

    with open(path, 'r') as f:
        a = 0
        for line in f:
            line = line.strip()
            if not line:  # Пропускаем пустые строки
                continue
                
            # Разделяем строку, учитывая что разделитель может быть табуляцией или несколькими пробелами
            parts = [p for p in line.replace('\t', ' ').split(' ') if p]
            
            if a < 15:
                head.append(parts)
            a += 1
            
            
            try:
                # Пытаемся преобразовать все части в float
                row = list(map(float, parts))
                array.append(row)
            except (ValueError, IndexError):
                
                # Пропускаем строки, которые не удалось преобразовать (заголовки и т.д.)
                #print(f"Skipping line: {line}")
                continue
    
    

    a = 0
    
    if head[9] == ['Chargeability']:
        a = 12
    elif head[0][0] == '#':
        a = 1
    else:
        a = 9
        
    i = len(head)-1
    while i >= a:
        del head[i]
        i-=1
        

    return array, head

















