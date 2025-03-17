# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 02:19:56 2025

@author: Vladimir
"""


#       (M)            
# 0  1   2     3     4     5     6        7         8  9  10    11  12      13  14  15  16 17  
# # Rho  0  Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny

# 0 1   2     3     4     5     6        7         8  9  10    11  12      13  14  15  16  
# # Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny

# ui_KomarovSP.py
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
import json
import os #работа с файлами


class Komarov_SP:
    
    def __init__(self, parent, ui):
        self.parent = parent
        self.ui = ui  # Сохраняем ссылку на UI
        self.frame = self.create_komarov_tab()

    def create_komarov_tab(self):
        """
        Создает содержимое вкладки Комаров ВП.
        """
        komarov_body_tab = ttk.Frame(self.parent)
        
        # Добавляем содержимое вкладки
        
        a = 0
        w = 20
        
        label = tk.Label(komarov_body_tab, text='Вызванная поляризация методом Комарова (V 1.0 2025)')
        label.grid(row=a, column=0, sticky='nw', padx=5, pady=5)
        a += 1
        
        button_safe_file = ttk.Button(komarov_body_tab, width = w, text='Сохранить')    
        button_safe_file.grid(row=a, column=0, ipadx=1, ipady=0, padx=1, pady=1, sticky='nw')
        a += 1
    
        button_open_file_1 = ttk.Button(komarov_body_tab, width = w, text='Низкая частота', command=self.array_low)    
        button_open_file_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=1, pady=1, sticky='nw')
        a += 1
        
        button_open_file_2 = ttk.Button(komarov_body_tab, width = w, text='Высокая частота', command=self.array_high)    
        button_open_file_2.grid(row=a, column=0, ipadx=1, ipady=0, padx=1, pady=1, sticky='nw')
        a += 1
        
        
        button_rasschet = ttk.Button(komarov_body_tab, width = w, text='Рассчитать')    
        button_rasschet.grid(row=a, column=0, ipadx=1, ipady=0, padx=1, pady=1, sticky='nw')
        a += 1
    
    
    
        return komarov_body_tab
    

    def get_frame(self):
        """
        Возвращает фрейм вкладки.
        """
        return self.frame



    def array_low(self):
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'), 
            ('Res2Dinv', '*.dat')
        ]
        
        # Открываем диалоговое окно для выбора файла
        filepath = filedialog.askopenfilename (filetypes=filetypes)
        
        
        try:
            self.array_low = self.read_array_RES(filepath)
            self.ui.update_message(f'Файл успешно загружен: {filepath}')
        except Exception as e:
            self.ui.update_message(f'Ошибка при выборе файла: {e}')


    def array_high(self):
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'), 
            ('Res2Dinv', '*.dat')
        ]
        
        # Открываем диалоговое окно для выбора файла
        filepath = filedialog.askopenfilename (filetypes=filetypes)
        
        try:
            self.array_high = self.read_array_RES(filepath)
            self.ui.update_message(f'Файл успешно загружен: {filepath}')
        except Exception as e:
            self.ui.update_message(f'Ошибка при выборе файла: {e}')





    @staticmethod
    def read_array_RES(path):

        array = list()
        
        with open(path, 'r') as f:
            array = f.readlines() 

        file_extension = os.path.splitext(path)[1]
        
        if file_extension == '.txt':
            for i in range(len(array)):
                array[i] = array[i].replace('\n', '')
                array[i] = array[i].split('\t')
                
                try:
                    array[i] = list(map(float, array[i]))
                except ValueError:
                    continue

        elif file_extension == '.dat':
            for i in range(len(array)):
                array[i] = array[i].replace('\n', '')
                array[i] = array[i].split(' ')
                
                try:
                    array[i] = list(map(float, array[i]))
                except ValueError:
                    continue
            
            
    

                
    
        return array



    
    
    
'''


# Функция для сохранения состояния чекпоинтов
def save_state(state):
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(state, file)  # Сохраняем состояние в JSON-файл

# Функция для загрузки состояния чекпоинтов
def load_state():
    try:
        with open('settings.json', 'r', encoding='utf-8') as file:
            return json.load(file)  # Читаем состояние из JSON-файла
    except (FileNotFoundError, json.JSONDecodeError):
        return {'check1': 0, 'check2': 0}  # Возвращаем значения по умолчанию




def insert_column(matrix, new_column, insert_position):
    for i in range(len(matrix)):
        matrix[i].insert(insert_position, new_column[i])
    return matrix


def rok_minus_rok_2():
    data_more = ''
    data_less = ''
    path_more = ''
    path_less = ''
    file_extension_1 = ''
    file_extension_2 = ''

    global final_array
    final_array = []
    
    data_more, label_3['text'], path_more, file_extension_1 = open_file()
    
    if path_more != '':
        data_less, label_4['text'], path_less, file_extension_2 = open_file()
    else:
        label_3['text'] = ''
        label_4['text'] = ''
        label_5['text'] = 'Error: Не выбран первый файл'

        open_button_5.config(state='disabled')
        return None  # Возвращаем None в случае ошибки

    
    if file_extension_1 == file_extension_2:
    
        if file_extension_1 == '.txt':
            data_type = '.txt'
            if path_more != '' and path_less != '' and path_more != path_less:
                del data_less[0]
                del data_more[0]
        
                a = list(range(len(data_more)))
                data_more = insert_column(data_more, a, 2)
                
                for i in range(len(data_more)):
                    for d in range(len(data_less)):
                        if data_more[i][3] == data_less[d][2] and \
                           data_more[i][4] == data_less[d][3] and \
                           data_more[i][5] == data_less[d][4] and \
                           data_more[i][6] == data_less[d][5]:
                            data_more[i][2] = (data_less[d][1] - data_more[i][1]) * (100 / data_more[i][1])
                            final_array.append(data_more[i])
        
                label_5['text'] = 'Done'
                open_button_5.config(state='normal')

                       
            else:
                label_5['text'] = 'Один файл не выбран или выбран один и тот же'
                open_button_5.config(state='disabled')
                return None  # Возвращаем None в случае ошибки

        elif file_extension_1 == '.dat':
            data_type = '.dat'
            global head_array
            head_array = []
            
            if path_more != '' and path_less != '' and path_more != path_less:
                
                i = len(data_more) - 1
                a = len(data_more[i-10])

                i = 0
                while True:
                    if len(data_more[i]) != a:
                        head_array.append(data_more[i])
                    else:
                        break
                    i += 1
                    
                i = len(data_more) - 1
                while i >= 0:
                    if len(data_more[i]) != a:
                        del data_more[i]
                    i -= 1
    
                i = len(data_less) - 1
                while i >= 0:
                    if len(data_less[i]) != a:
                        del data_less[i]
                    i -= 1
                
                a = len(data_more[0]) - 1
                for i in range(len(data_more)):
                        for d in range(len(data_less)):
                            if data_more[i][0] == data_less[d][0] and \
                               data_more[i][1] == data_less[d][1] and \
                               data_more[i][2] == data_less[d][2] and \
                               data_more[i][3] == data_less[d][3]:
                                
                                data_more[i].append((data_less[d][a] - data_more[i][a]) * (100 / data_more[i][a]))
    
                final_array = data_more
                label_5['text'] = 'Файлы .dat'
                open_button_5.config(state='normal')

                
            else:
                label_5['text'] = 'Один файл не выбран или выбран один и тот же'
                open_button_5.config(state='disabled')
                return None  # Возвращаем None в случае ошибки
            
        else:
            label_5['text'] = 'Файлы неизвестного формата'
            open_button_5.config(state='disabled')
            return None  # Возвращаем None в случае ошибки
    
    else:
        label_5['text'] = 'Файлы разных расширений'
        open_button_5.config(state='disabled')
        return None  # Возвращаем None в случае ошибки


def save_file():
    if data_type == '.txt':
        if rksp.get():  # Если чекпоинт активен (True)
            filepath_exit = filedialog.asksaveasfilename(defaultextension='txt')
            if filepath_exit != '':
                with open(filepath_exit, 'w') as file:
                    file.write(str('#\tRho\tM\tSpa.1\tSpa.2\tSpa.3\tSpa.4\tPassTime\tDutyCycle\tVp\tIn\tDev.\tK\tPhase\tAy\tBy\tMy\tNy\n'))
                    
    
                    if sp100.get():  # Если чекпоинт активен (True)
                        s = 1
                        for item in final_array:
                            file.write(f'{s}\t{float(item[1]):.3f}\t{100 + float(item[2]):.3f}\t'
                                       f'{float(item[3]):.3f}\t{float(item[4]):.3f}\t{float(item[5]):.3f}\t'
                                       f'{float(item[6]):.3f}\t{float(item[7]):.3f}\t{float(item[8]):.3f}\t'
                                       f'{float(item[9]):.3f}\t{float(item[10]):.3f}\t{float(item[11]):.3f}\t'
                                       f'{float(item[12]):.3f}\t{float(item[13]):.3f}\t{float(item[14]):.3f}\t'
                                       f'{float(item[15]):.3f}\t{float(item[16]):.3f}\t{float(item[17]):.3f}\n')
                            s += 1
                        label_5['text'] = 'Сохранено КС+(100+ВП)'
                    else:  # Если чекпоинт неактивен (False)
                        s = 1
                        for item in final_array:
                            file.write(f'{s}\t{float(item[1]):.3f}\t{float(item[2]):.3f}\t'
                                       f'{float(item[3]):.3f}\t{float(item[4]):.3f}\t{float(item[5]):.3f}\t'
                                       f'{float(item[6]):.3f}\t{float(item[7]):.3f}\t{float(item[8]):.3f}\t'
                                       f'{float(item[9]):.3f}\t{float(item[10]):.3f}\t{float(item[11]):.3f}\t'
                                       f'{float(item[12]):.3f}\t{float(item[13]):.3f}\t{float(item[14]):.3f}\t'
                                       f'{float(item[15]):.3f}\t{float(item[16]):.3f}\t{float(item[17]):.3f}\n')
                            s += 1
                
                        label_5['text'] = 'Сохранено КС+ВП'
    
        
        else:  # Если чекпоинт неактивен (False)
            filepath_exit = filedialog.asksaveasfilename(defaultextension='txt')
            if filepath_exit != '':
                with open(filepath_exit, 'w') as file:
                    file.write(str('#\tRho\tSpa.1\tSpa.2\tSpa.3\tSpa.4\tPassTime\tDutyCycle\tVp\tIn\tDev.\tK\tPhase\tAy\tBy\tMy\tNy\n'))
                    
                    
                    if sp100.get():  # Если чекпоинт активен (True)
                        s = 1
                        for item in final_array:
                            file.write(f'{s}\t{100 + float(item[2]):.3f}\t'
                                       f'{float(item[3]):.3f}\t{float(item[4]):.3f}\t{float(item[5]):.3f}\t'
                                       f'{float(item[6]):.3f}\t{float(item[7]):.3f}\t{float(item[8]):.3f}\t'
                                       f'{float(item[9]):.3f}\t{float(item[10]):.3f}\t{float(item[11]):.3f}\t'
                                       f'{float(item[12]):.3f}\t{float(item[13]):.3f}\t{float(item[14]):.3f}\t'
                                       f'{float(item[15]):.3f}\t{float(item[16]):.3f}\t{float(item[17]):.3f}\n')
                            s += 1
                        label_5['text'] = 'Сохранено (100 + ВП) вместо КС'
                        
                    else:  # Если чекпоинт неактивен (False)
                        s = 1
                        for item in final_array:
                            file.write(f'{s}\t{float(item[2]):.3f}\t'
                                       f'{float(item[3]):.3f}\t{float(item[4]):.3f}\t{float(item[5]):.3f}\t'
                                       f'{float(item[6]):.3f}\t{float(item[7]):.3f}\t{float(item[8]):.3f}\t'
                                       f'{float(item[9]):.3f}\t{float(item[10]):.3f}\t{float(item[11]):.3f}\t'
                                       f'{float(item[12]):.3f}\t{float(item[13]):.3f}\t{float(item[14]):.3f}\t'
                                       f'{float(item[15]):.3f}\t{float(item[16]):.3f}\t{float(item[17]):.3f}\n')
                            s += 1
                        label_5['text'] = 'Сохранено ВП вместо КС'
                        
    elif data_type == '.dat':

        
        filepath_exit = filedialog.asksaveasfilename(defaultextension='txt')
        if filepath_exit != '':
            with open(filepath_exit, 'w') as file:
                #0  1    2  3     4  5     6  7
                #3 0.00  0  2.00  0  4.00  0  199.16
                
                file.write(str('file Сохранено КС+ВП\n'))
                file.write(f'{head_array[1][0]}\n')
                file.write(str('11\n'))
                file.write(str('0\n'))
                file.write(str('Type of measurement (0=app.resistivity,1=resistance)\n'))
                file.write(str('0\n'))
                file.write(f'{len(final_array)}\n')
                file.write(str('1\n'))
                file.write(str('0\n'))
                
                if sp100.get():  # Если чекпоинт активен (True)

                    for item in final_array:
                        file.write(f'{int(item[0])}\t{float(item[1]):.1f}\t{float(item[2]):.1f}\t'
                                   f'{float(item[3]):.1f}\t{float(item[4]):.1f}\t{float(item[5]):.1f}\t'
                                   f'{float(item[6]):.1f}\t{100 + float(item[8]):.3f}\n')
                    
                    label_5['text'] = 'Сохранено (100 + ВП) вместо КС'
                    
                else:  # Если чекпоинт неактивен (False)

                    for item in final_array:
                        file.write(f'{int(item[0])}\t{float(item[1]):.1f}\t{float(item[2]):.1f}\t'
                                   f'{float(item[3]):.1f}\t{float(item[4]):.1f}\t{float(item[5]):.1f}\t'
                                   f'{float(item[6]):.1f}\t{float(item[8]):.3f}\n')

                    label_5['text'] = 'Сохранено ВП вместо КС'

                file.write(str('0\n0\n0\n0\n0\n0\n'))
    else:
        label_5['text'] = 'Сохранено невозможно'





def helper():
    
    with open('text_helper.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()
        
    # Создаем новое окно
    new_window = tk.Toplevel(root)
    new_window.title('Helper')
    new_window.geometry('650x400')

    # Создаем текстовый виджет
    text_widget = tk.Text(new_window, wrap='word', font=('Arial', 10))
    text_widget.pack(fill='both', expand=True, padx=10, pady=10)

    # Вставляем текст из файла
    text_widget.insert('1.0', file_content)

    # Отключаем возможность редактирования
    text_widget.config(state='disabled')





# Загружаем состояние
state = load_state()

rksp = tk.IntVar(value=state['check1'])
sp100 = tk.IntVar(value=state['check2'])



# Создаем и размещаем метки
label = tk.Label(root, text='Сначала выбираем НИЗКУЮ частоту, потом ВЫСОКУЮ', justify='left')
label_3 = tk.Label(root, text='File: ')
label_4 = tk.Label(root, text='File: ')


label_5 = tk.Label(root, text='')
label_5.grid(column=0, row=11, sticky=SW)


label.grid(column=0, row=0, sticky=NW)
label_3.grid(column=0, row=2, sticky=NW)
label_4.grid(column=0, row=3, sticky=NW)



# Создаем чекпоинты
checkbutton = tk.Checkbutton(
    root,
    text='Сохранить файл КС и ВП',
    variable=rksp  # Привязываем переменную к чекпоинту
)


checkbutton_100 = tk.Checkbutton(
    root,
    text='+100 к ВП',
    variable=sp100  # Привязываем переменную к чекпоинту
)
checkbutton_100.grid(column=0, row=9, padx=180, pady=0, sticky=NW)
checkbutton.grid(column=0, row=9, padx=0, pady=0, sticky=NW)  


# Создаем кнопки
a = 0


open_button_4 = ttk.Button(root, text='?', command = helper)
open_button_4.grid(column=1, row=0, ipadx=0, ipady=0, padx=20, pady=0, sticky=NE)

open_button_5 = ttk.Button(root, text='Сохранить', state='disabled', command = save_file)
open_button_5.grid(column=1, row=1, ipadx=0, ipady=0, padx=20, pady=0, sticky=NE)


# Функция, которая вызывается при закрытии окна
def on_closing():
    state = {'check1': rksp.get(), 'check2': sp100.get()}  # Сохраняем состояния
    save_state(state)  # Перезаписываем файл
    root.destroy()

# Привязываем событие закрытия окна к функции on_closing
root.protocol('WM_DELETE_WINDOW', on_closing)


'''
    
