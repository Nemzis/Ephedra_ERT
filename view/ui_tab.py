# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 01:50:15 2025

@author: Vladimir
"""

# ui_tab.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class DataTab:
    
    def __init__(self, parent, ui, data):
        self.parent = parent
        self.ui = ui  # Сохраняем ссылку на UI
        self.data = data
        self.frame = self.create_data_tab()

    def create_data_tab(self):
        """
        Создает содержимое вкладки
        """
        body_tab = ttk.Frame(self.parent)
        
        # Добавляем содержимое вкладки
        
        a = 0
        w = 20
        
        label = tk.Label(body_tab, text='test')
        label.grid(row=a, column=0, sticky='nw', padx=5, pady=5)
        a += 1
        
        # Отображение первых 5 строк данных
        if self.data:
            for i, row in enumerate(self.data[:5]):  # Ограничиваемся 5 строками
                row_label = tk.Label(body_tab, text=f"Строка {i + 1}: {row}")
                row_label.grid(row=a, column=0, sticky='nw', padx=5, pady=2)
                a += 1
        else:
            no_data_label = tk.Label(body_tab, text="Нет данных")
            no_data_label.grid(row=a, column=0, sticky='nw', padx=5, pady=5)

        print(len(self.data))
    
        return body_tab
    

    def get_frame(self):
        """
        Возвращает фрейм вкладки.
        """
        return self.frame



  