# -*- coding: utf-8 -*-
'''
Created on Tue Mar  4 02:19:56 2025

@author: Vladimir
'''


#       (M)            
# 0  1   2     3     4     5     6        7         8  9  10    11  12      13  14  15  16 17  
# # Rho  0  Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny

# 0 1   2     3     4     5     6        7         8  9  10    11  12      13  14  15  16  
# # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import copy 
import json
import os


class Komarov_SP:
    def __init__(self, parent, ui):
        self.parent = parent  # Главное окно
        self.ui = ui  # Сохраняем ссылку на UI
        
        self.filepath_1 = '1'
        self.filepath_2 = '2'

        self.array_low = list()
        self.array_high = list()
        self.result_data = list()
        
        self.file_extension_low = '1'
        self.file_extension_high = '2'

        # Инициализация переменных для чекбоксов

        self.sp100 = tk.IntVar()

        # Загружаем состояния чекбоксов
        self.state = self.load_state()
        self.sp100.set(self.state.get('check2', 0))  # По умолчанию 0, если ключа нет
        
        # Создаем интерфейс
        self.frame = self.create_komarov_tab()



    def create_komarov_tab(self):
        self.komarov_body_tab = ttk.Frame(self.parent)

        a = 0
        w = 20

        label = tk.Label(self.komarov_body_tab, text='Вызванная поляризация методом Комарова (V 1.4.3 2025)')
        label.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, columnspan=50,  sticky='nw')
        a += 1

        button_open_file_1 = ttk.Button(self.komarov_body_tab, width = w, text='Низкая частота', command=self.array_low_load)
        button_open_file_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1

        button_open_file_2 = ttk.Button(self.komarov_body_tab, width = w, text='Высокая частота', command=self.array_high_load)
        button_open_file_2.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1

        button_rasschet = ttk.Button(self.komarov_body_tab, width = w, text='Рассчитать', command=self.rok_minus_rok_2)
        button_rasschet.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        button_safe_file = ttk.Button(self.komarov_body_tab, width = w, text='Сохранить', command = self.save_file)
        button_safe_file.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        
        button_reset = ttk.Button(self.komarov_body_tab, width=w, text='Сброс', command=self.reset)
        button_reset.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1

        open_button_ask = ttk.Button(self.komarov_body_tab, width = w, text='?', command=self.helper)
        open_button_ask.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        open_button_safe_chek = ttk.Button(self.komarov_body_tab, width = w, text='Cохранить настройки модуля', command=self.on_closing)
        open_button_safe_chek.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        self.label_text_info = tk.Label(self.komarov_body_tab, text='Основная формула ((A-B)*100/B)')
        self.label_text_info.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, columnspan=50, sticky='w')
        a += 1
        
        
        b = 1
        self.label_text_load_1 = tk.Label(self.komarov_body_tab, text='Файл...')
        self.label_text_load_1.grid(row=b, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        b += 1
        
        self.label_text_load_2 = tk.Label(self.komarov_body_tab, text='Файл...')
        self.label_text_load_2.grid(row=b, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        b += 1
        
        self.label_text_result = tk.Label(self.komarov_body_tab, text='Результат...')
        self.label_text_result.grid(row=b, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        b += 1
        
        
        # Создаем чекпоинты
        
        checkbutton_100 = tk.Checkbutton(
            self.komarov_body_tab,
            text='+100 к рассчетным данным',
            variable=self.sp100
        )
        checkbutton_100.grid(row=a, column=0, padx=0, pady=0, columnspan=50, sticky='nw')
        a += 1
        
        return self.komarov_body_tab
    
    
    def get_frame(self):
        return self.frame
    
    
    def reset(self):
        self.array_low_copy = list()
        self.array_high_copy = list()
        self.result_data_copy = list()
        
        self.filepath_1 = '1'
        self.filepath_2 = '2'
        
        self.array_low = list()
        self.array_high = list()
        self.head = list()
        
        self.file_extension_low = '1'
        self.file_extension_high = '2'
        
        self.label_text_load_1['text'] = ('Файл...')
        self.label_text_load_2['text'] = ('Файл...')
        self.label_text_result ['text'] = ('Результат...')
        
    
    
    def array_low_load(self):
        self.array_low = list()
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'),
            ('Res2Dinv', '*.dat')
        ]
         
        self.filepath_1 = filedialog.askopenfilename(filetypes=filetypes)
    
        try:
            if self.filepath_1 != self.filepath_2:
                
                self.array_low, self.head = self.ui.controller.load_file(self.filepath_1)

                self.label_text_load_1['text'] = (f'{self.filepath_1}')
                self.ui.update_message(f'Файл успешно загружен, размер массива: {len(self.array_low)}')
                self.file_extension_low = os.path.splitext(self.filepath_1)[1]
                
            else:
                self.ui.update_message('Один и тот же файл')
                
        except Exception as e:
            self.ui.update_message(f'Ошибка при выборе файла: {e}')      
                       

    def array_high_load(self):
        self.array_high = list()
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'),
            ('Res2Dinv', '*.dat')
        ]
    
        self.filepath_2 = filedialog.askopenfilename(filetypes=filetypes)
    
        try:
            if self.filepath_1 != self.filepath_2:
                
                self.array_high, self.head = self.ui.controller.load_file(self.filepath_2)
                
                self.label_text_load_2['text'] = (f'{self.filepath_2}')
                self.ui.update_message(f'Файл успешно загружен, размер массива: {len(self.array_high)}')
                self.file_extension_high = os.path.splitext(self.filepath_2)[1]
            else:
                self.ui.update_message('Один и тот же файл')
        except Exception as e:
            self.ui.update_message(f'Ошибка при выборе файла: {e}')
 

    def rok_minus_rok_2(self):
        self.result_data = list()
        self.array_low_copy = list()
        self.array_high_copy = list()

        self.array_low_copy = copy.deepcopy(self.array_low)
        self.array_high_copy = copy.deepcopy(self.array_high)
        
        a = 0
        b = 0

        # 0 1    2    3     4     5     6        7         8  9  10    11  12      13  14  15  16  
        # # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny
        
        if self.file_extension_low == self.file_extension_high:
            if self.file_extension_low == '.txt':
                
                if len(self.array_low_copy[0]) == 17:
                    for item1 in self.array_low_copy:
                        for item2 in self.array_high_copy:
                            if item1[2] == item2[2] and\
                                item1[3] == item2[3] and\
                                item1[4] == item2[4] and\
                                item1[5] == item2[5] and\
                                item1[13] == item2[13] and\
                                item1[14] == item2[14] and\
                                item1[15] == item2[15] and\
                                item1[16] == item2[16]:
                                    item1[1] = (item1[1] - item2[1]) * (100 / item2[1])
                                           
                    self.result_data = self.array_low_copy

                elif len(self.array_low_copy[0]) > 17:
                    for item1 in self.array_low_copy:
                        for item2 in self.array_high_copy:
                            if item1[23] == item2[23] and\
                                item1[24] == item2[24] and\
                                item1[25] == item2[25] and\
                                item1[26] == item2[26] and\
                                item1[33] == item2[33] and\
                                item1[34] == item2[34] and\
                                item1[35] == item2[35] and\
                                item1[36] == item2[36]:
                                    item1[1] = (item1[1] - item2[1]) * (100 / item2[1])
                                    
                    self.result_data = self.array_low_copy
                else:
                    self.ui.update_message('Неизвестный формат файла')
                    
                
            elif self.file_extension_low == '.dat':
                
                i = len(self.array_low_copy) - 1
                while i >= 0:
                    if len(self.array_low_copy[i]) < 6 or self.array_low_copy[i][0] == 20.0:
                        del self.array_low_copy[i]
                    i -= 1


                i = len(self.array_high_copy) - 1
                while i >= 0:
                    if len(self.array_high_copy[i]) < 6 or self.array_high_copy[i][0] == 20.0:
                        del self.array_high_copy[i]
                    i -= 1                    
                    

                for item1 in self.array_low_copy:
                    if item1[0] == 3.0:
                        for item2 in self.array_high_copy:
                            if item1[0] == item2[0] and\
                                item1[1] == item2[1] and\
                                item1[2] == item2[2] and\
                                item1[3] == item2[3] and\
                                item1[4] == item2[4] and\
                                item1[5] == item2[5] and\
                                item1[6] == item2[6]:
                                    item1[7] = ((item1[7] - item2[7]) * (100 / item2[7]))
                                    
                    elif item1[0] == 4.0:
                        for item2 in self.array_high_copy:
                            if item1[0] == item2[0] and\
                                item1[1] == item2[1] and\
                                item1[2] == item2[2] and\
                                item1[3] == item2[3] and\
                                item1[4] == item2[4] and\
                                item1[5] == item2[5] and\
                                item1[6] == item2[6] and\
                                item1[7] == item2[7] and\
                                item1[8] == item2[8]:
                                    item1[9] = ((item1[9] - item2[9]) * (100 / item2[9]))
                    else:
                        continue
                                             
                self.result_data = self.array_low_copy
                
            a = len(self.array_low) - len(self.result_data)
            b = len(self.array_high) - len(self.result_data)
            self.label_text_result['text'] = f'Разница между результатом и массивом low - {a}, и массивом high - {b}'
            self.ui.update_message(f'Рассчет выполнен {len(self.result_data)}')
        
        else:
            self.ui.update_message('Файлы разных форматов!')



    def save_file(self):
        self.result_data_copy = copy.deepcopy(self.result_data)
        
        if self.sp100.get() == 0:
            plus = 0
        else:
            plus = 100
                 
        if self.file_extension_low == self.file_extension_high:
            if self.file_extension_low == '.txt':
                if self.result_data_copy:
                    path = filedialog.asksaveasfilename(
                        defaultextension='.txt', # Автоматически добавляет .dat
                        filetypes=[('DAT files', '*.txt'), ('All files', '*.*')],  # Фильтр для расширений
                        title='Сохранить файл') #Заголовок
                     
                    for item in self.result_data_copy:
                        item[0] = int(item[0])
                        item[1] = round(item[1] + plus, 4)
                          
                    if path:
                        file = open(path, 'w')
                        file.write('\t'.join(self.head[0]) + '\n') #заголовок

                        for row in self.result_data_copy:
                            # Преобразуем числа в строки и объединяем через пробел
                            line = '\t'.join(map(str, row))  
                            file.write(line + '\n')  # Записываем строку и переходим на новую

                        file.close()                
                        
                        self.ui.update_message('Сохранение выполнено')
                    else:
                        self.ui.update_message('Не выбрано место сохранения')
                             
                        
            elif self.file_extension_low == '.dat':
                if self.result_data_copy:
                    path = filedialog.asksaveasfilename(
                        defaultextension='.dat', # Автоматически добавляет .dat
                        filetypes=[('DAT files', '*.dat'), ('All files', '*.*')], # Фильтр для расширений
                        title='Сохранить файл') #Заголовок
                                              
                    if path:
                        if self.result_data_copy[0][0] == 4:
                            b = 9
                        elif self.result_data_copy[0][0] == 3:
                            b = 7
                            
                        for item in self.result_data_copy:
                            item[0] = int(item[0])
                            item[b] = round(item[b] + plus, 4)
                            
                        self.head[6] = [str(len(self.result_data_copy))]
                        
                        file = open(path, 'w')
                        
                        for row in self.head:
                            # Преобразуем числа в строки и объединяем через пробел
                            line = ' '.join(map(str, row))  
                            file.write(line + '\n')  # Записываем строку и переходим на новую
                        
                        for row in self.result_data_copy:
                            # Преобразуем числа в строки и объединяем через пробел
                            line = ' '.join(map(str, row))  
                            file.write(line + '\n')  # Записываем строку и переходим на новую
                              
                        file.write('0\n0\n0\n0\n0\n0\n0')
                        file.close()

                        self.ui.update_message('Сохранение выполнено')
                    else:
                        self.ui.update_message('Не выбрано место сохранения') 
                    



    def save_state(self, state):
        '''Сохраняет состояния чекбоксов в файл.'''
        try:
            settings_dir = 'module/komarov_sp'
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)  # Создаем каталог, если его нет

            settings_path = os.path.join(settings_dir, 'settings.json')
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(state, file, indent=4)
            self.ui.update_message('Состояния успешно сохранены.')
        except Exception as e:
            self.ui.update_message(f'Ошибка при сохранении состояний: {e}')
                


    def load_state(self):
        '''Загружает состояния чекбоксов из файла.'''
        try:
            settings_path = os.path.join('module/komarov_sp', 'settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                self.ui.update_message('Файл настроек не найден, используются значения по умолчанию.')
                return {'check1': 0, 'check2': 0}
        except Exception as e:
            self.ui.update_message(f'Ошибка при загрузке состояний: {e}')
            return {'check1': 0, 'check2': 0}


    def on_closing(self):
        '''Обрабатывает закрытие окна.'''
        self.state = {'check2': self.sp100.get()}
        self.save_state(self.state)
        
        

        
    def helper(self):
        with open('module/komarov_sp/helper_Komarov.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()

        new_window = tk.Toplevel(self.komarov_body_tab)
        new_window.title('Helper')
        new_window.geometry('650x400')

        text_widget = tk.Text(new_window, wrap='word', font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)

        text_widget.insert('1.0', file_content)
        text_widget.config(state='disabled')


'''
сортировка для txt and dat внутри одного файла 
Amn
mnB
внутри сортировка с минимального сверху вниз 

внутри .dat после кс SP и Ox и AO или OB 


'''



