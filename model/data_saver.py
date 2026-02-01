# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:50:58 2025

@author: Vladimir
'''
import copy


def REC_in_files_for_INV(path, array, zagolovok_file, save_mode):
    #Путь, массив, заголовок, половина расстояния между электродами
    #формат файла 
    # 0  1    2     3     4     5     6        7       8  9  10    11  12      13  14  15  16  
    # # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny ...
    
    print (save_mode)
    
    
    array_copy = copy.deepcopy(array)


    for i in range(len(array_copy)):
        array_copy[i] = list(map(str, array_copy[i]))


    #высчитываем шаг между электродами
    all_X2 = list()
    all_Y2 = list()
    
    for item in array_copy:
        
        x1 = float(item[4])
        x2 = float(item[5])
        y1 = float(item[15])
        y2 = float(item[16])
        
        all_X2.append(x1)
        all_X2.append(x2)
        all_Y2.append(y1)
        all_Y2.append(y2)

        
    all_X2 = sorted(list(dict.fromkeys(all_X2)))
    all_Y2 = sorted(list(dict.fromkeys(all_Y2)))

    
    b = (all_X2[2]-all_X2[1])/2
    
    
    array_copy_X = []
    i = all_X2[0]
    
    while i <= all_X2[-1]:
        array_copy_X.append(i)
        i += b
        
        
    array_copy_Y = []
    i = all_Y2[0]
    
    while i <= all_Y2[-1]:
        array_copy_Y.append(i)
        i += b
         
    file = open(path, 'w')
    file.write(str(zagolovok_file) + ('\n')) #заголовок
    file.write(f'{len(array_copy_X)}\n')
    file.write(f'{len(array_copy_Y)}\n')
    file.write(str('Nonuniform grid\n'))
    file.write(str('X-location of grid lines\n'))

    for item in array_copy_X:
        file.write(f'{item}\t')
    
    file.write(str('\nY-location of grid lines\n'))

    for item in array_copy_Y:
        file.write(f'{item}\t')

    file.write(str('\n11\n'))
    file.write(str('0\n'))
    file.write(str('Type of data (0 = apparent resistivity, 1=resistance)\n'))
    
    if save_mode == 'rho':
        file.write(str('0\n'))
    else:
        file.write(str('1\n'))
    
    
    
    
    file.write(str(len(array_copy)) + ('\n'))



    if save_mode == 'rho':
        for item in array_copy:
            if item[2] != '99999.999' and item[3] != '99999.999':
                file.write(f'4\t{item[2]},\t{item[13]}\t{item[3]},\t{item[14]}\t{item[4]},\t{item[15]}\t{item[5]},\t{item[16]}\t{item[1]}\n')
            else:
                file.write(f'3\t{item[2]},\t{item[13]}\t{item[4]},\t{item[15]}\t{item[5]},\t{item[16]}\t{item[1]}\n')
               
    else:
        for item in array_copy:
            if item[2] != '99999.999' and item[3] != '99999.999':
                file.write(f'4\t{item[2]},\t{item[13]}\t{item[3]},\t{item[14]}\t{item[4]},\t{item[15]}\t{item[5]},\t{item[16]}\t{float(item[8])/float(item[9])}\n')
            else:
                file.write(f'3\t{item[2]},\t{item[13]}\t{item[4]},\t{item[15]}\t{item[5]},\t{item[16]}\t{float(item[8])/float(item[9])}\n')
        
        
        
    file.write(str('0\n0\n0\n0\n0\n0'))
    file.close()
    
    
    
    

#запись ROK
def REC_standart_ROK(path, array):
    #ver 2.1
    #массив, путь
    #файл должен быть подготовлен:
    # X Y Z R
    # X Y Z R log(R)
    # X Y Z R log(R) V I 
    # X Y Z R log(R) V I M


    if len(array[0]) == 4:
        file = open(path, 'w')
        file.write(str('X\tY\tZ\tROK\n')) #заголовок
        for item in array:
            file.write(f'{float(item[0]):.2f}\t{float(item[1]):.2f}\t{float(item[2]):.2f}\t'
                       f'{float(item[3]):.4f}\n')
        file.close()    

    elif len(array[0]) == 5:
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
    
    

    
        
def Rec_PyGimli_v2(path, data):
    
    pass
    #надо отсортировать двумерный массив и переобозначить метры на номера электродов
    meters = []

    for item in data:
        if item[2] != 99999.999:
            item[2] = item[2] + 0.1
            item[13] = item[13] + 0.1
            meters.append([item[2], item[13]] )

    for item in data:
        if item[3] != 99999.999:
            item[3] = item[3] + 0.1
            item[14] = item[14] + 0.1
            meters.append([item[3], item[14]] )
            
    for item in data:
        if item[4] != 99999.999:
            item[4] = item[4] + 0.1
            item[15] = item[15] + 0.1
            meters.append([item[4], item[15]] )
        
    for item in data:
        if item[5] != 99999.999:
            item[5] = item[5] + 0.1
            item[16] = item[16] + 0.1
            meters.append([item[5], item[16]] )       
            
    # Преобразуем каждый внутренний список в кортеж (tuple)
    unique_meters = list(set(tuple(row) for row in meters))
    
    # Преобразуем обратно в списки
    unique_meters = [list(row) for row in unique_meters]   

    sorted_unique_meters = sorted(unique_meters, key=lambda x: (x[0], x[1]))

    '''
    Итоговая сортировка
    10 20
    9 19
    8 18
    7 17
    6 16
    5 15
    4 14
    3 13
    2 12
    1 11 ... 
    
    '''

    
    i = 1
    for item in sorted_unique_meters:
        item.append(i)
        i+=1
        
        #print(item)

    #меняем метры на электроды
    for item in data: 
        for item_2 in sorted_unique_meters:
            
            if item[2] == item_2[0] and item[13] == item_2[1]:
                item[2] = item_2[2]
                
            
            if item[3] == item_2[0] and item[14] == item_2[1]:
                item[3] = item_2[2]         
                
            
            if item[4] == item_2[0] and item[15] == item_2[1]:
                item[4] = item_2[2]         
                

            if item[5] == item_2[0] and item[16] == item_2[1]:
                item[5] = item_2[2]
                
                
    for item in data:
        if item[2] == 99999.999:
            item[2] = 0
            item[13] = 0
            
        if item[3] == 99999.999:
            item[3] = 0
            item[14] = 0      
    
    file = open(path, "w")
    str_head = str(int(sorted_unique_meters[-1][2])) + '# Number of electrodes\n#x\ty\tz\n'
    str_head_data = str(len(data)) + '# Number of data\n#a\tb\tm\tn\tr\tu\ti\tk\trhoa\n'
    file.write(str_head) #заголовок электродов

    for item in sorted_unique_meters:
        item[0] = round(item[0] - 0.1, 2)
        item[1] = round(item[1] - 0.1, 2)
        
        file.write(f'{float(item[0])}\t{float(item[1])}\t0.0\n')
    
    file.write(str_head_data) #заголовок данных
    
    for item in data:
        r = item[8]/item[9]
        file.write(f'{int(item[2])}\t{int(item[3])}\t{int(item[4])}\t{int(item[5])}\t{r}\t{item[8]}\t{item[9]}\t{item[11]}\t{item[1]}\n')
    file.close()  

  


#формат файла 
# 0  1    2     3     4     5     6        7       8  9  10    11  12      13  14  15  16  
# # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny ...
        
        
        
'''
Образец записи pyGimli (чтоб не искать)
19# Number of sensors 
#x	z
1	-23.0
2	-22.0
3	-21.0
4	-20.0
5	-19.0
6	-18.0
7	-17.0
8	-16.0
9	-15.0
10	-14.0
11	-13.0
12	-12.0
13	-11.0
14	-10.0
15	-9.0
16	-8.0
17	-7.0
18	-6.0
19	-5.0
574# Number of data
#a	b	m	n	r	k
1	0	5	6	0.10160756501182033	251.32741228718345
1	0	7	8	0.08160756501182033	527.7875658030853
1	0	9	10	0.10293144208037826	904.7786842338604
1	0	11	12	0.03304964539007092	1382.300767579509
1	0	13	14	0.13037825059101654	1960.3538158400308
1	0	15	16	0.014349881796690308	2638.9378290154264
... .. 


'''
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

