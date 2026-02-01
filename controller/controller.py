# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:51:42 2025

@author: Vladimir
'''

import model.data_loader as dl
import model.data_processor as dp
import model.data_saver as ds


class Controller:
    
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на UI
        self.data = list()
        

    def process_files(self, input_dir):

        # Чтение файлов
        self.data, n_file, error_AB, error_MN, SP  = dl.mass_load_files(input_dir)
        
        
        # Обновляем сообщение в UI
        self.ui.update_message(f'{len(self.data)} - количество строчек, {n_file} - файлов\n'\
                               f'Удалены ошибки: {error_AB} - A and B = 99999.999, {error_MN} - M or N = 99999.999,\n'\
                               f'{SP}')
        

        
    def processing_file(self, x, y, r):
        #Вызывает функцию separator для разделения данных.

        if not self.data:
            self.ui.update_message('Данные не загружены.')
        
        # Вызываем функцию separator
        pole_dipole, pole_dipole_X_sistem, pole_dipole_L_sistem, dipole_dipole,\
            dipole_dipole_L_sistem, dipole_dipole_X_sistem, pl_messege, schlumberger = dp.separator(self.data, x ,y, r)
        
        return pole_dipole, pole_dipole_X_sistem, pole_dipole_L_sistem, dipole_dipole,\
            dipole_dipole_L_sistem, dipole_dipole_X_sistem, pl_messege, schlumberger, self.data
    
    
    
    def get_histogram(self, data, a, title):
        #Возвращает гистограмму для данных.
        return dp.gistogramma(data, a, title)
    


    def get_plot(self, array, a, b):
        return dp.plot(array, a, b)  # Возвращаем объект Figure
    
    
        
    def filter_data_c(self, array, min_ROK, max_ROK, param_index):

        try:
            # Преобразуем значения в float
            min_ROK = float(min_ROK) if min_ROK else float('-inf')  # Если min_ROK пустое, используем -∞
            max_ROK = float(max_ROK) if max_ROK else float('inf')   # Если max_ROK пустое, используем +∞
            
            if min_ROK > max_ROK or min_ROK == max_ROK:
                self.ui.update_message('Ошибка ввода данных: min_ROK >= max_ROK')
                return array
            
            # Фильтруем массив
            array_filter = dp.filter_array(array, min_ROK, max_ROK, param_index)
    
        except Exception as e:
            self.ui.update_message(f'Ошибка: {e}')
            return array  # Возвращаем исходный массив в случае ошибки
    
        return array_filter
    
    
    def processing_xyzrho(self, array, type_array, path):
        data = dp.Rok_3D2D(array, type_array)
        return ds.REC_standart_ROK(path, data)
        
        
    def multiply(self, array, x, y, r):
        array = dp.multiply_data(array, x, y, r)
        return array


    def processing_array_for_PyGimli(self, path, data):
        #Rec_PyGimli
        return ds.Rec_PyGimli_v2(path, data)
        
    
    def safe_data(self, path, array, zagolovok_file, save_mode):
        return ds.REC_in_files_for_INV(path, array, zagolovok_file, save_mode)
    
    
    #-----------------------------------------------------работа с модулем Sim
    def load_file(self, path):
        array, head = dl.load_file(path)
        return array, head
    
    
    def save_file(self, path, array):
        return ds.REC_standart_ROK(path, array)





    



