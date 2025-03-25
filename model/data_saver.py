# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:50:58 2025

@author: Vladimir
'''
import copy



def REC_in_files_for_INV(path, array, zagolovok_file, a):
    #Путь, массив, заголовок, половина расстояния между электродами
    #формат файла 
    # 0  1    2     3     4     5     6        7       8  9  10    11  12      13  14  15  16  
    # # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny ...

    for i in range(len(array)):
        array[i] = list(map(str, array[i]))


    all_X = list()
    all_Y = list()
    for item in array:
        
        x1 = float(item[4])
        x2 = float(item[5])
        y1 = float(item[15])
        y2 = float(item[16])
        
        all_X.append(x1)
        all_X.append(x1 + a)
        
        all_X.append(x2)
        all_X.append(x2 + a)
        
        all_Y.append(y1)
        all_Y.append(y1 + a)
        
        all_Y.append(y2)
        all_Y.append(y2 + a)
        
        
    all_X = sorted(list(dict.fromkeys(all_X)))
    all_Y = sorted(list(dict.fromkeys(all_Y)))
    
    del all_X[len(all_X)-1]
    del all_Y[len(all_Y)-1]
    
    
    for i in range(len(all_X)):
        all_X[i] = round(all_X[i], 2)
        
        
    for i in range(len(all_Y)):
        all_Y[i] = round(all_Y[i], 2)


    
    file = open(path, 'w')
    file.write(str(zagolovok_file) + ('\n')) #заголовок
    file.write(f'{len(all_X)}\n')
    file.write(f'{len(all_Y)}\n')
    file.write(str('Nonuniform grid\n'))
    file.write(str('X-location of grid lines\n'))


    for item in all_X:
        file.write(f'{item}\t')
    
    file.write(str('\nY-location of grid lines\n'))

    for item in all_Y:
        file.write(f'{item}\t')

    file.write(str('\n11\n'))
    file.write(str('0\n'))
    file.write(str('Type of data (0=apparent resistivity,1=resistance)\n'))
    file.write(str('0\n'))
    file.write(str(len(array)) + ('\n'))

    for item in array:
        if array[0][2] != '99999.999' and array[0][3] != '99999.999':
            file.write(f'4\t{item[2]},\t{item[13]}\t{item[3]},\t{item[14]}\t{item[4]},\t{item[15]}\t{item[5]},\t{item[16]}\t{item[1]}\n')
    
    for item in array:
        if array[0][2] == '99999.999' or array[0][3] == '99999.999':
            file.write(f'3\t{item[2]},\t{item[13]}\t{item[4]},\t{item[15]}\t{item[5]},\t{item[16]}\t{item[1]}\n')
    
    file.write(str('0\n0\n0\n0\n0\n0'))
    file.close()
    
    
    

#запись ROK
def REC_standart_ROK(path, array):
    #ver 2.0
    #массив, путь
    #файл должен быть подготовлен:
    # X Y Z R log(R)
    # X Y Z R log(R) V I 
    # X Y Z R log(R) V I M
   
    if len(array[0]) == 5:
        file = open(path, 'w')
        file.write(str('X\tY\tZ\tROK\tlog(ROK)\n')) #заголовок
        for item in array:
            file.write(f'{float(item[0]):.2f}\t{float(item[1]):.2f}\t{float(item[2]):.2f}\t'
                       f'{float(item[3]):.4f}\t{float(item[4]):.4f}\n')
        file.close()
    elif len(array[0]) == 7:
        file = open(path, 'w')
        file.write(str('X\tY\tZ\tROK\tlog(ROK)\tV\tI\n')) #заголовок
        for item in array:
            file.write(f'{float(item[0]):.2f}\t{float(item[1]):.2f}\t{float(item[2]):.2f}\t'
                       f'{float(item[3]):.4f}\t{float(item[4]):.4f}\t{float(item[5]):.4f}\t'
                        f'{float(item[6]):.4f}\n')
        file.close()
    elif len(array[0]) == 8:
        file = open(path, 'w')
        file.write(str('X\tY\tZ\tROK\tlog(ROK)\tV\tI\tM\n')) #заголовок
        for item in array:
            file.write(f'{float(item[0]):.2f}\t{float(item[1]):.2f}\t{float(item[2]):.2f}\t'
                       f'{float(item[3]):.4f}\t{float(item[4]):.4f}\t{float(item[5]):.4f}\t'
                        f'{float(item[6]):.4f}\t{float(item[7]):.4f}\n')
        file.close()
    
    
    
    
def Rec_PyGimli(path_2, xyz, data):
    
    data_copy = copy.deepcopy(data)
    for i in range(len(xyz)):
        for d in range(len(data)):
            
            if xyz[i][1] == data_copy[d][2] and xyz[i][2] == data_copy[d][13]:
                data_copy[d][2] = xyz[i][0]
                
            if xyz[i][1] == data_copy[d][3] and xyz[i][2] == data_copy[d][14]:
                data_copy[d][3] = xyz[i][0]
                
            if xyz[i][1] == data_copy[d][4] and xyz[i][2] == data_copy[d][15]:
                data_copy[d][4] = xyz[i][0] 
                
            if xyz[i][1] == data_copy[d][5] and xyz[i][2] == data_copy[d][16]:
                data_copy[d][5] = xyz[i][0] 
    

    file = open(path_2, 'w')
    file.write(str(f'{len(xyz)}\n'))
    file.write(str('#\tx\ty\tz\n')) 
    for item in xyz:
        file.write(f'{float(item[1]):.2f}\t{float(item[2]):.2f}\t{float(item[3]):.2f}\n')
        
    file.write(str(f'{len(data_copy)}\n'))
    
    
    
    
    if data_copy[0][2] == 99999.999:
        
        file.write(str('#\ta\tm\tn\tR\n'))
        for item in data_copy:
            file.write(f'{int(item[3])}\t{int(item[4])}\t{int(item[5])}\t{float(item[1]):.3f}\n')
    
    elif data_copy[0][3] == 99999.999:
        
        file.write(str('#\ta\tm\tn\tR\n'))
        for item in data_copy:
            file.write(f'{int(item[2])}\t{int(item[4])}\t{int(item[5])}\t{float(item[1]):.3f}\n')
        
    else:
        file.write(str('#\ta\tb\tm\tn\tR\n'))
        for item in data_copy:
            file.write(f'{int(item[2])}\t{int(item[3])}\t{int(item[4])}\t{int(item[5])}\t{float(item[1]):.3f}\n')
            
            
        
    file.write(str('0'))
    
        
        
        
        
        
#формат файла 
# 0  1    2     3     4     5     6        7       8  9  10    11  12      13  14  15  16  
# # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny ...
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

