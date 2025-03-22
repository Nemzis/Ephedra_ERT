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
import json
import os



class Komarov_SP:
    def __init__(self, parent, ui):
        self.parent = parent  # Главное окно
        self.ui = ui  # Сохраняем ссылку на UI


        # Инициализация переменных для чекбоксов
        self.rksp = tk.IntVar()
        self.sp100 = tk.IntVar()

        # Загружаем состояния чекбоксов
        self.state = self.load_state()
        self.rksp.set(self.state.get('check1', 0))  # По умолчанию 0, если ключа нет
        self.sp100.set(self.state.get('check2', 0))  # По умолчанию 0, если ключа нет

        # Создаем интерфейс
        self.frame = self.create_komarov_tab()



    def create_komarov_tab(self):
        self.komarov_body_tab = ttk.Frame(self.parent)

        a = 0
        w = 20

        label = tk.Label(self.komarov_body_tab, text='Вызванная поляризация методом Комарова (V 1.2.2 2025) (В разработке)')
        label.grid(row=a, column=0, sticky='nw', padx=5, pady=5)
        a += 1

        button_safe_file = ttk.Button(self.komarov_body_tab, text='Сохранить')
        button_safe_file.grid(row=a, column=0, sticky='nw', ipadx=1, ipady=0, padx=1, pady=1)
        a += 1

        button_open_file_1 = ttk.Button(self.komarov_body_tab, text='Низкая частота', command=self.array_low)
        button_open_file_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=1, pady=1, sticky='nw')
        a += 1

        button_open_file_2 = ttk.Button(self.komarov_body_tab, text='Высокая частота', command=self.array_high)
        button_open_file_2.grid(row=a, column=0, ipadx=1, ipady=0, padx=1, pady=1, sticky='nw')
        a += 1

        button_rasschet = ttk.Button(self.komarov_body_tab, text='Рассчитать')
        button_rasschet.grid(row=a, column=0, ipadx=1, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1

        open_button_ask = ttk.Button(self.komarov_body_tab, text='?', command=self.helper)
        open_button_ask.grid(row=a, column=0, ipadx=0, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1
        
        open_button_safe_chek = ttk.Button(self.komarov_body_tab,  text='Cохранить настройки модуля', command=self.on_closing)
        open_button_safe_chek.grid(row=a, column=0, ipadx=0, ipady=0, padx=0, pady=1, sticky='nw')
        
        

        # Создаем чекпоинты
        checkbutton = tk.Checkbutton(
            self.komarov_body_tab,
            text='Сохранить файл КС и ВП',
            variable=self.rksp
        )
        checkbutton.grid(row=9, column=0, padx=0, pady=0, sticky='nw')

        checkbutton_100 = tk.Checkbutton(
            self.komarov_body_tab,
            text='+100 к ВП',
            variable=self.sp100
        )
        checkbutton_100.grid(row=10, column=0, padx=0, pady=0, sticky='nw')

        return self.komarov_body_tab
    
    
    def get_frame(self):
        return self.frame
    
    
    
    def array_low(self):
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'),
            ('Res2Dinv', '*.dat')
        ]
    
        filepath = filedialog.askopenfilename(filetypes=filetypes)
    
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
    
        filepath = filedialog.askopenfilename(filetypes=filetypes)
    
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
    
    


    def save_state(self, state):
        '''Сохраняет состояния чекбоксов в файл.'''
        try:
            settings_dir = 'module/komarov_sp'
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)  # Создаем каталог, если его нет

            settings_path = os.path.join(settings_dir, 'settings.json')
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(state, file, indent=4)
            print('Состояния успешно сохранены.')
        except Exception as e:
            print(f'Ошибка при сохранении состояний: {e}')
            
            

    def load_state(self):
        '''Загружает состояния чекбоксов из файла.'''
        try:
            settings_path = os.path.join('module/komarov_sp', 'settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                print('Файл настроек не найден, используются значения по умолчанию.')
                return {'check1': 0, 'check2': 0}
        except Exception as e:
            print(f'Ошибка при загрузке состояний: {e}')
            return {'check1': 0, 'check2': 0}




    def on_closing(self):
        '''Обрабатывает закрытие окна.'''
        self.state = {'check1': self.rksp.get(), 'check2': self.sp100.get()}
        self.save_state(self.state)
        #self.parent.destroy()  # Закрываем главное окно
        
        
        
        
        
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















# Создаем и размещаем метки

label_3 = tk.Label(root, text='File: ')
label_4 = tk.Label(root, text='File: ')


label_5 = tk.Label(root, text='')
label_5.grid(column=0, row=11, sticky=SW)


label.grid(column=0, row=0, sticky=NW)
label_3.grid(column=0, row=2, sticky=NW)
label_4.grid(column=0, row=3, sticky=NW)












'''
    
