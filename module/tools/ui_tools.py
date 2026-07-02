# -*- coding: utf-8 -*-
'''
Created on 02.07.2025

@author: Vladimir
'''


#Нужно переименовать в VolDiff

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import math
import json
import os
import copy 


class tools:
    def __init__(self, parent, ui):
       
        self.parent = parent  # Главное окно
        self.ui = ui  # Сохраняем ссылку на UI
        

        # Создаем интерфейс
        self.frame = self.create_tools_tab()



    def create_tools_tab(self):
        self.tools_body_tab = ttk.Frame(self.parent)

        a = 0
        w = 20
        
        label = tk.Label(self.tools_body_tab, text='Tools (version v0.1.0 2026)')
        label.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, columnspan=50,  sticky='nw')
        a += 1

        button_load_array_1 = ttk.Button(self.tools_body_tab, width=w, text='protocol > flank_protocol', command=self.open_file)
        button_load_array_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1


        label = tk.Label(
            self.tools_body_tab,
            text='Введите итоговое минимальное расстояние\n между электродами'
        )
        label.grid(row=a, column=0, sticky='nsew', pady=5, padx=5)
        a += 1
        
        self.step_var = tk.StringVar(value="2.5")
        
        self.step = tk.Entry(
            self.tools_body_tab,
            textvariable=self.step_var,
            width=5
        )
        self.step.grid(row=a, column=0, sticky='nsew', pady=5, padx=5)
        a += 1


        open_button_ask = ttk.Button(self.tools_body_tab, width = w, text='?', command=self.helper)
        open_button_ask.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
        a += 1
        
        

        return self.tools_body_tab
    
    
    def get_frame(self):
        return self.frame    
    

    
    def helper(self):
        with open('module/tools/helper_tools.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()

        new_window = tk.Toplevel(self.tools_body_tab)
        new_window.title('Helper')
        new_window.geometry('650x400')

        text_widget = tk.Text(new_window, wrap='word', font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)

        text_widget.insert('1.0', file_content)
        text_widget.config(state='disabled')
        
        
        
        
        
    def open_file(self):
        filetypes = [
            ('Текстовые файлы', '*.txt'),
        ]
        
        self.filepath = filedialog.askopenfilename(filetypes=filetypes)
        self.array = self.ui.controller.load_file_simple(self.filepath)


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
            file.write(f'#\tX\tY\tZ\n')
            
            for item in xyz:
                file.write(f'{int(item[0])}\t{float(item[1])}\t{float(item[2])}\t{float(item[3])}\n')
                
            file.write(f'#\tA\tB\tM\tN\n')
            for item in data:
                tmp = '\t'.join(str(int(x)) for x in item)
                file.write(tmp + '\n')
                
            file.close()
            
            self.ui.update_message(f'Преобразование файла акончено {name},уe файл {index + 1} из 4')

                
            

            
        
        
        
        
        
        
        
        
        
        
            
        
        
        
       
        
       
        
       
        
       
        
       
        
        