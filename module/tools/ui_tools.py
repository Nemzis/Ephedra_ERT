# -*- coding: utf-8 -*-
'''
Created on 02.07.2025

@author: Vladimir
'''


#Нужно переименовать в VolDiff

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import copy 
import gpxpy
import csv
from utils.path import get_path

class tools:
    def __init__(self, parent, ui):
       
        self.parent = parent  # Главное окно
        self.ui = ui  # Сохраняем ссылку на UI
        

        # Создаем интерфейс
        self.frame = self.create_tools_tab()



    def create_tools_tab(self):
        self.tools_body_tab = ttk.Frame(self.parent)




        w = 25
        
        # Заголовок
        label = tk.Label(self.tools_body_tab, text='Tools (version v0.2.1 2026)')
        label.grid(row=0, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        
        # ============ ПЕРВЫЙ ФРЕЙМ ============
        self.customer_frame = tk.LabelFrame(self.tools_body_tab, text='Фланговая расстановка')
        self.customer_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        
        # Label с описанием
        label = tk.Label(
            self.customer_frame,
            text='Расстояние между электродами'
        )
        label.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        
        
        # Label с описанием
        label = tk.Label(
            self.customer_frame,
            text='1'
        )
        label.grid(row=1, column=0, sticky='w', pady=5, padx=5)
        
        # Поле ввода
        self.step_var = tk.StringVar(value="2.5")
        self.step = tk.Entry(
            self.customer_frame,
            textvariable=self.step_var,
            width=10
        )
        self.step.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        
    
        
        # Кнопка
        button_load_array_1 = ttk.Button(self.customer_frame, width=w, text='protocol>flank_protocol', command=self.flank)
        button_load_array_1.grid(row=2, column=1, ipadx=1, ipady=0, padx=5, pady=2, sticky='w')
        # Label с описанием
        
        label = tk.Label(
            self.customer_frame,
            text='2'
        )
        label.grid(row=2, column=0, sticky='w', pady=5, padx=5)    

        
        # ============ ВТОРОЙ ФРЕЙМ ============
        self.customer_frame_2 = tk.LabelFrame(self.tools_body_tab, text='Преобразование GPX')
        self.customer_frame_2.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        
        # Кнопка
        button_load_array_2 = ttk.Button(self.customer_frame_2, width=w, text='GPX > CSV (point)', command=self.GPX_to_CSV)
        button_load_array_2.grid(row=0, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='w')
        
        # ============ КНОПКА ПОМОЩИ ============
        open_button_ask = ttk.Button(self.tools_body_tab, width=5, text='?', command=self.helper)
        open_button_ask.grid(row=3, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='w')
        

        return self.tools_body_tab
    
    
    def get_frame(self):
        return self.frame    
    


    def test_file(self, file):
        # ПРОВЕРКА: выбран ли файл
        if not file:  # Если пользователь нажал "Отмена" или закрыл диалог
            self.ui.update_message('Файл не выбран')
            return  # Выходим из функции
        
        # ПРОВЕРКА: существует ли файл
        if not os.path.exists(file):
            self.ui.update_message(f'Файл не найден: {file}')
            return
        
        # ПРОВЕРКА: является ли это файлом (не папкой)
        if not os.path.isfile(file):
            self.ui.update_message(f'Указанный путь не является файлом: {file}')
            return
        
        return file  
    
    
    def flank(self):
        filetypes = [
            ('Текстовые файлы', '*.txt'),
        ]
        
        self.filepath = filedialog.askopenfilename(filetypes=filetypes)
        
        try:
            # Загружаем файл
            self.filepath = self.test_file(self.filepath)
            self.array = self.ui.controller.load_file_simple(self.filepath)
            
        except Exception as e:
            self.ui.update_message(f'Ошибка при загрузке файла: {e}')
            return  # Важно прервать выполнение при ошибке
        
        
        # Если код дошел сюда - файл успешно загружен
        self.ui.update_message(f'Файл успешно загружен: {os.path.basename(self.filepath)}')
        

        #Работа со строкой
        name_file_safe = 0
        path_safe = 0
        i = len(self.filepath)-1
        dl = len(self.filepath)
        while True:
            if self.filepath[i] == '/':
                name_file_safe = self.filepath[i+1:dl]
                break
                
            path_safe = self.filepath[0:i]
            i-=1
            
        name_file_safe = name_file_safe.replace('.txt', '')
        #print(f'{name_file_safe} - Входной файл') 
        #print(f'{path_safe} - путь') 
            
        kosa = []
         
        a = 1
        b = 48
         
        for index in range(4):
        
            #index = c
            kosa = []
            
            
            if index == 0:
                #print('index =', index)
                a = 1
                b = 48
                name = path_safe + name_file_safe + '_flank_(1el=0m).txt'
                for i in range(1, 25):
                    kosa.append([a, 0])
                    kosa.append([b, 0])
                    a+=1
                    b-=1
            elif index == 1:
                #print('index =', index)    
                a = 1
                b = 48
            
                name = path_safe + name_file_safe + '_flank_(48el=0m).txt'
                for i in range(1, 25):
                    kosa.append([b, 0])
                    kosa.append([a, 0])
                    a+=1
                    b-=1
                    
            elif index == 2:
                #print('index =', index)
                a = 24
                b = 25
                
                
                name = path_safe + name_file_safe + '_flank_(24el=0m).txt'
                for i in range(1, 25):
                    kosa.append([a, 0])
                    kosa.append([b, 0])
                    a-=1
                    b+=1  
            
            elif index == 3:
                #print('index =', index)
                a = 24
                b = 25
                
                name = path_safe + name_file_safe + '_flank_(25el=0m).txt'
                for i in range(1, 25):
                    kosa.append([b, 0])
                    kosa.append([a, 0])
                    a-=1
                    b+=1  
            
            for i in range(len(kosa)):
                kosa[i][1] = i+1.1   
                    
                
            #геометрия
            x=0
            step = float(self.step_var.get())
            
            xyz = []
            for item in kosa:
                xyz.append([item[0], x, 0, 0])
                x+=step
            xyz.sort(key=lambda x: x[0])
            

            data = copy.deepcopy(self.array[48:])

            for item in data:
                item[0] = int(item[0])
                item[1] = item[1] + 0.1
                item[2] = item[2] + 0.1
                item[3] = item[3] + 0.1
                item[4] = item[4] + 0.1    
                #print(item)
            
            for i in range(len(kosa)):
                for c in range(len(data)):
            
                    if kosa[i][1] == data[c][1]:
                        data[c][1] = kosa[i][0]
            
                    
                    if data[c][2] == 0.1:
                        data[c][2] = 0
                    else:
                        if kosa[i][1] == data[c][2]:
                            data[c][2] = kosa[i][0]
            
                        
                    if kosa[i][1] == data[c][3]:
                        data[c][3] = kosa[i][0]
            
                    if kosa[i][1] == data[c][4]:
                        data[c][4] = kosa[i][0]
            
            file = open(name, "w")
            file.write('#\tX\tY\tZ\n')
            
            for item in xyz:
                file.write(f'{int(item[0])}\t{float(item[1])}\t{float(item[2])}\t{float(item[3])}\n')
                
            file.write('#\tA\tB\tM\tN\n')
            for item in data:
                tmp = '\t'.join(str(int(x)) for x in item)
                file.write(tmp + '\n')
                
            file.close()
            
            self.ui.update_message(f'Преобразование файла акончено {name}, {index + 1} из 4')





        
        
    def GPX_to_CSV(self):
        #на вход GPX на выход CSV
    
        filetypes = [('Текстовые файлы', '*.gpx')]
        
        self.filepath = filedialog.askopenfilename(filetypes=filetypes)

        try:
            # Загружаем файл
            self.filepath = self.test_file(self.filepath)
            
            #Работа со строкой
            name_file_safe = ''
            path_safe = ''
            i = len(self.filepath)-1
            dl = len(self.filepath)
            while True:
                
                if self.filepath[i] == '/':
                    name_file_safe = self.filepath[i+1:dl]
                    break
                    
                path_safe = self.filepath[0:i]
                i-=1
            
            #print(f'{name_file_safe} - Входной файл') 
            name_file_safe = name_file_safe.replace('.gpx', '.csv')
            #print(f'{name_file_safe} - Сохраеннный файл')     
            
            
            # Открываем и парсим GPX файл
            with open(self.filepath) as gpx_file:
                gpx = gpxpy.parse(gpx_file)
            
            
            with open(path_safe + name_file_safe, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'latitude', 'longitude', 'elevation', 'time', 'comment', 'sym']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                
                writer.writeheader()
                
                # Сохраняем waypoints (отдельные точки)
                for waypoint in gpx.waypoints:
                    writer.writerow({
                        'name': waypoint.name if waypoint.name else '',
                        'latitude': waypoint.latitude,
                        'longitude': waypoint.longitude,
                        'elevation': waypoint.elevation if waypoint.elevation else '',
                        'time': waypoint.time.strftime("%Y-%m-%d %H:%M:%S") if waypoint.time else '',
                        'comment': waypoint.comment if waypoint.comment else '',
                        'sym': waypoint.symbol if waypoint.symbol else ''
                    })                  
            
            
            # Если код дошел сюда - файл успешно загружен
            self.ui.update_message(f'Файл {os.path.basename(self.filepath)} преобразован.')
            self.ui.update_message(f'{name_file_safe} - Сохраеннный файл')
            
        except Exception as e:
            self.ui.update_message(f'Ошибка при загрузке файла: {e}')
            return  # Важно прервать выполнение при ошибке
        
        

        
    def helper(self):
        with open(
            get_path("module", "tools", "helper_tools.txt"),
            "r",
            encoding="utf-8"
        ) as file:
            file_content = file.read()
    
        new_window = tk.Toplevel(self.tools_body_tab)
        new_window.title('Helper')
        new_window.geometry('650x400')
    
        text_widget = tk.Text(new_window, wrap='word', font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
    
        text_widget.insert('1.0', file_content)
        text_widget.config(state='disabled')
    
        
        
        
        
        
        
            
        
        
        
       
        
       
        
       
        
       
        
       
        
        