# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 02:19:56 2025

@author: Vladimir
"""

# ui_KomarovSP.py
import tkinter as tk
from tkinter import ttk



def komarov_tab(parent):

    settings_tab = ttk.Frame(parent)
    
    # Добавляем содержимое вкладки
    label = tk.Label(settings_tab, text='!!!')
    label.pack(pady=20)

    # Выпадающее меню
    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(settings_tab, textvariable=dropdown_var)
    dropdown['values'] = ["Вариант 1", "Вариант 2", "Вариант 3"]
    dropdown.current(0)
    dropdown.pack(pady=10)

    # Кнопка для обработки выбора
    button = tk.Button(settings_tab, text="Выбрать", command=lambda: on_dropdown_select(dropdown_var))
    button.pack(pady=10)

    return settings_tab

def on_dropdown_select(dropdown_var):
    """
    Обрабатывает выбор из выпадающего меню.
    """
    selected_value = dropdown_var.get()
    print(f"Выбран: {selected_value}")
    
    
