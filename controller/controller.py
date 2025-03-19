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
        

        
    def processing_file(self):
        #Вызывает функцию separator для разделения данных.

        if not self.data:
            self.ui.update_message('Данные не загружены.')
        
        # Вызываем функцию separator
        pole_dipole, dipole_dipole, schlumberger = dp.separator(self.data)
        
        return pole_dipole, dipole_dipole, schlumberger, self.data
    
    
    
    def get_histogram(self, data, a, title):
        '''
        Возвращает гистограмму для данных.
        '''
        return dp.gistogramma(data, a, title)
    
    
    
        
    def filter_data_c(self, array, min_ROK, max_ROK, param_index):
        '''
        Фильтрует данные через процессор.
        :param array: Исходный массив.
        :param min_ROK: Минимальное значение ROK.
        :param max_ROK: Максимальное значение ROK.
        :return: Отфильтрованный массив.
        '''

        
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
        
        

    
    
    
    
    def safe_data(self, path, array, zagolovok_file, a):
        '''
        Возвращает гистограмму для данных.
        '''
        return ds.REC_in_files_for_INV(path, array, zagolovok_file, a)


    



