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
        
        label = tk.Label(self.tools_body_tab, text='Tools (version v0.0.0 2026)')
        label.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, columnspan=50,  sticky='nw')
        a += 1

        button_load_array_1 = ttk.Button(self.tools_body_tab, width=w, text='Загрузить массив ?')
        button_load_array_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=5, pady=2, sticky='nw')
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
        
        
     
       
        
        
        
        
        
        
        
        
        
        
        
            
        
        
        
       
        
       
        
       
        
       
        
       
        
        