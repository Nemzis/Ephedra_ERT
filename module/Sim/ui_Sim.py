# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 17:20:08 2025

@author: Vladimir
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import os



class Sim:
    def __init__(self, parent, ui):
        self.parent = parent  # Главное окно
        self.ui = ui  # Сохраняем ссылку на UI

        # Создаем интерфейс
        self.frame = self.create_sim_tab()



    def create_sim_tab(self):
        self.sim_body_tab = ttk.Frame(self.parent)

        a = 0
        w = 20
        
        label = tk.Label(self.sim_body_tab, text='Сравнение моделей методом Sim (V 0.0.0 2025) (В разработке)')
        label.grid(row=a, column=0, ipadx=1, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1

        button_load_array_1 = ttk.Button(self.sim_body_tab, width=w, text='Загрузить массив 1')
        button_load_array_1.grid(row=a, column=0, ipadx=1, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1
          
        button_load_array_2 = ttk.Button(self.sim_body_tab, width=w, text='Загрузить массив 2')
        button_load_array_2.grid(row=a, column=0, ipadx=1, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1
        
        button_rasschet = ttk.Button(self.sim_body_tab, width=w, text='Рассчитать')
        button_rasschet.grid(row=a, column=0, ipadx=1, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1
        
        button_safe = ttk.Button(self.sim_body_tab, width=w, text='Сохранить')
        button_safe.grid(row=a, column=0, ipadx=1, ipady=0, padx=0, pady=1, sticky='nw')
        a += 1



        return self.sim_body_tab
    
    
    def get_frame(self):
        return self.frame