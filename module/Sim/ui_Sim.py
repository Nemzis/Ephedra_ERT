# -*- coding: utf-8 -*-
'''
Created on Fri Mar 21 17:20:08 2025

@author: Vladimir
'''


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import os



class Sim:
    def __init__(self, parent, ui):
       
        self.parent = parent  # Главное окно
        self.ui = ui  # Сохраняем ссылку на UI
        
        self.filepath_1 = '1'
        self.filepath_2 = '2'

        self.result_data = list()
        self.array_1 = list()
        self.array_2 = list()
        
        # Создаем интерфейс
        self.frame = self.create_sim_tab()



    def create_sim_tab(self):
        self.sim_body_tab = ttk.Frame(self.parent)

        a = 0
        w = 20
        
        label = tk.Label(self.sim_body_tab, text='Сравнение моделей методом Sim (V 0.1.1 2025) (В разработке)')
        label.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, columnspan=50,  sticky='nw')
        a += 1

        button_load_array_1 = ttk.Button(self.sim_body_tab, width=w, text='Загрузить массив A', command = self.open_file_1)
        button_load_array_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
          
        button_load_array_2 = ttk.Button(self.sim_body_tab, width=w, text='Загрузить массив B', command = self.open_file_2)
        button_load_array_2.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        button_rasschet = ttk.Button(self.sim_body_tab, width=w, text='Рассчитать', command = self.proccesing)
        button_rasschet.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        button_safe = ttk.Button(self.sim_body_tab, width=w, text='Сохранить')
        button_safe.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        button_reset = ttk.Button(self.sim_body_tab, width=w, text='Сброс', command = self.reset)
        button_reset.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        self.label_text_info = tk.Label(self.sim_body_tab, text='Основная формула ((A-B)*100/B)+100')
        self.label_text_info.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, columnspan=50, sticky='w')
        a += 1
        
        
        
        b = 1
        self.label_text_load_1 = tk.Label(self.sim_body_tab, text='Файл...')
        self.label_text_load_1.grid(row=b, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        b += 1
        
        self.label_text_load_2 = tk.Label(self.sim_body_tab, text='Файл...')
        self.label_text_load_2.grid(row=b, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        b += 1
        
        self.label_text_result = tk.Label(self.sim_body_tab, text='Результат...')
        self.label_text_result.grid(row=b, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        b += 1



        return self.sim_body_tab
    
    
    def get_frame(self):
        return self.frame
    
    
    def open_file_1(self):
        
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'),
            ('Res2Dinv', '*.dat')
        ]
        
        self.filepath_1 = filedialog.askopenfilename(filetypes=filetypes)
        if self.filepath_1 != self.filepath_2:
            self.array_1 = self.ui.controller.load_file(self.filepath_1)
            
            self.label_text_load_1['text'] = (f'{self.filepath_1}')
            self.ui.update_message(f'Первый массив загружен длина {len(self.array_1)}')
        else:
            self.ui.update_message('Один и тот же файл')
            


    def open_file_2(self):
        
        filetypes = [
            ('Все форматы', '*'),
            ('Текстовые файлы', '*.txt'),
            ('Res2Dinv', '*.dat')
        ]

        self.filepath_2 = filedialog.askopenfilename(filetypes=filetypes)
        if self.filepath_1 != self.filepath_2:
            self.array_2 = self.ui.controller.load_file(self.filepath_2)
            
            self.label_text_load_2['text'] = (f'{self.filepath_2}')
            self.ui.update_message(f'Первый массив загружен длина {len(self.array_2)}')
        else:
            self.ui.update_message('Один и тот же файл')
        
        
    def reset(self):
        self.filepath_1 = '1'
        self.filepath_2 = '2'
        self.label_text_load_1['text'] = ('Файл...')
        self.label_text_load_2['text'] = ('Файл...')
        self.label_text_result ['text'] = ('Результат...')
        self.array_1 = list()
        self.array_2 = list()
        self.result_data = list()
        
       
    def proccesing(self):
        
        
        for i in range(len(self.array_1)):
            for d in range(len(self.array_2)):
                if self.array_1[i][0] == self.array_2[d][0] and\
                    self.array_1[i][1] == self.array_2[d][1] and\
                    self.array_1[i][2] == self.array_2[d][2]:
                        try:
                            result = ((self.array_1[i][3] - self.array_2[d][3]) * (100/self.array_2[d][3])+100)
                            self.result_data.append([self.array_1[i][0], self.array_1[i][1], self.array_1[i][2], result])
                        except ValueError:
                            continue
            
        
        a = len(self.array_1) - len(self.result_data)
        b = len(self.array_2) - len(self.result_data)
        self.label_text_result ['text'] = (f'Разница между результатом и массивом А - {a}, и массивом B - {b}')
        self.ui.update_message(f'Рассчет выполнен {len(self.result_data)}')      
            
        
        
        
       
        
       
        
       
        
       
        
       
        
        