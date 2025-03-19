# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 01:50:15 2025

@author: Vladimir
"""

# ui_tab.py
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from controller.controller import Controller



class DataTab:
    
    def __init__(self, parent, ui, data, controller, type_array):
        self.controller = controller
        self.parent = parent
        self.ui = ui  # Сохраняем ссылку на UI
        self.data = data
        
        self.type_array = type_array
        
        #эта хрень должна быть последней
        self.frame = self.create_data_tab()

        

    def create_data_tab(self):
        self.array_post_filter = list()
        self.data_recovery = self.data
        
        self.body_tab = ttk.Frame(self.parent)
        

        w = 20 #общая ширина кнопок
        
        self.button_safe_all = ttk.Button(self.body_tab, text = 'Сохранить файл (Res3Dinv)', command = self.safe_data)
        self.button_safe_all.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')

        self.button_safe_rho = ttk.Button(self.body_tab, text = 'Сохранить файл XYZR', state='normal', command = self.safe_xyz_rho)
        self.button_safe_rho.grid(row=1, column=0, pady = 5, padx = 5, sticky='wn')

        if self.type_array == 'all_data':
            self.button_safe_rho.config(state='disabled')
            
       
        # -----------------------------------------------------------
        self.customer_frame = tk.LabelFrame(self.body_tab, text="Сохранение Файла")
        self.customer_frame.grid(row=2, rowspan = 4, column=0, padx=5, pady=5, sticky="NSEW")
        
        # Поле ввода для заголовка файла
        label_zagolovok = tk.Label(self.customer_frame, text='Заголовок Res3Dinv:')
        label_zagolovok.grid(row=0, column=0, sticky='wn', pady = 5, padx = 5)
        
        self.entry_zagolovok = tk.Entry(self.customer_frame, width=15)
        self.entry_zagolovok.grid(row=1, column=0, sticky='w', pady = 5, padx = 5)
        self.entry_zagolovok.insert(0, 'Test')
        
        # Поле ввода для параметра шага
        label_a = tk.Label(self.customer_frame, text='Половина расстояния\n между электродами')
        label_a.grid(row=2, column=0, sticky='wn', pady = 5, padx = 5)

        self.entry_a = tk.Entry(self.customer_frame, width=15)
        self.entry_a.grid(row=3, column=0, sticky='wn', pady = 5, padx = 5)
        self.entry_a.insert(0, '0.02')
        
        
        # -----------------------------------------------------------
        self.customer_frame_filter = tk.LabelFrame(self.body_tab, text="Фильтр по диапазону")
        self.customer_frame_filter.grid(row=6,rowspan = 8, column=0, padx=10, pady=10, sticky="NSEW")
        
        label_Rho_min = tk.Label(self.customer_frame_filter, text='Минимум')
        label_Rho_min.grid(row=0, column=0, sticky='wn', pady = 5, padx = 5)
        
        self.entry_Rho_min = tk.Entry(self.customer_frame_filter, width=10)
        self.entry_Rho_min.grid(row=1, column=0, sticky='wn', pady = 5, padx = 5)
        
        label_Rho_max = tk.Label(self.customer_frame_filter, text='Максимум')
        label_Rho_max.grid(row=2, column=0, sticky='wn', pady = 5, padx = 5)
        
        self.entry_Rho_max = tk.Entry(self.customer_frame_filter, width=10)
        self.entry_Rho_max.grid(row=3, column=0, sticky='wn', pady = 5, padx = 5)
        
        open_rasschet = ttk.Button(self.customer_frame_filter, width = w, text='Рассчитать', command = self.filter_data)
        open_rasschet.grid(row=4, column=0, padx = 5, pady = 5)
        
        open_sbros = ttk.Button(self.customer_frame_filter, width = w, text='Сбросить', command = self.reset_filter)
        open_sbros.grid(row=5, column=0, padx = 5, pady = 5)
        
        open_apply = ttk.Button(self.customer_frame_filter, width = w, text='Применить', command = self.apply_filter)
        open_apply.grid(row=6, column=0, padx = 5, pady = 5)
        
        open_apply = ttk.Button(self.customer_frame_filter, width = w, text='Восстановить\nисходный\nмассив', command = self.recovery_filter )
        open_apply.grid(row=7, column=0, padx = 5, pady = 5)
        
        
        
        # -----------------------------------------------------------
        #Гистограмма 
        self.show_histogram(self.body_tab, self.data, 1, 'Rho')
        
        self.customer_frame_histogram = tk.LabelFrame(self.body_tab, text="Управление Гистрограммой")
        self.customer_frame_histogram.grid(row=0, column=1, rowspan = 2, padx=10, pady=10, sticky="NSEW")
        
        # Создаём выпадающий список
        if len(self.data[0]) > 17:
            self.param_combobox = ttk.Combobox(self.customer_frame_histogram, values=['Rho', 'V (mV)', 'I (mA)', 'K', 'M'])
            self.param_combobox.grid(row=0, column=0, padx=5, pady=5, sticky='wn')
            self.param_combobox.current(0)  # Устанавливаем значение по умолчанию (Rho)
        else:
            self.param_combobox = ttk.Combobox(self.customer_frame_histogram, values=['Rho', 'V (mV)', 'I (mA)', 'K'])
            self.param_combobox.grid(row=0, column=0, padx=5, pady=5, sticky='wn')
            self.param_combobox.current(0)  # Устанавливаем значение по умолчанию (Rho)
        
        # Кнопка для отображения гистограммы
        show_button = ttk.Button(self.customer_frame_histogram, text='Обновить гистограмму', command = self.show_histogram_wrapper)
        show_button.grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=0, sticky='wn')
        
        
        # -----------------------------------------------------------
        #исправляем шаг
        self.customer_frame_step = tk.LabelFrame(self.body_tab, text="Множитель координат")
        self.customer_frame_step.grid(row=0, column=2, rowspan = 2, padx=10, pady=10, sticky="NSEW")
        
        self.entry_step = tk.Entry(self.customer_frame_step, width = w)
        self.entry_step.grid(row=0, column=0, sticky='wn', pady = 5, padx = 5)
        
        open_step = ttk.Button(self.customer_frame_step, width = w, text='Умножить')
        open_step .grid(row=1, column=0, padx = 5, pady = 5)

        


        return self.body_tab
    


    
    #Гистрограмма -----------------------------------------------
    # -----------------------------------------------------------
    
    def show_histogram_wrapper(self):
        
        #Обёртка для вызова show_histogram с правильным параметром.
        # Получаем выбранный параметр
        selected_param = self.param_combobox.get()
        # Определяем индекс параметра
        param_index = self.get_param_index(selected_param)

        # Вызываем функцию show_histogram
        self.show_histogram(self.body_tab, self.data, param_index, f'Гистограмма для {selected_param}')
    
    

    def get_param_index(self, param):
        
        #Возвращает индекс параметра.
        
        if len(self.data[0]) > 17:
            param_mapping = {
                'Rho': 1,  # Индекс для Rho
                'V (mV)': 8,    # Индекс для V
                'I (mA)': 9,    # Индекс для I
                'K': 11,
                'M': 17
            }
            
        else:
            param_mapping = {
                'Rho': 1,  # Индекс для Rho
                'V (mV)': 8,    # Индекс для V
                'I (mA)': 9,    # Индекс для I
                'K': 11
            }
            
        return param_mapping.get(param, 1)  # По умолчанию возвращаем индекс для Rho
        
        
     
    def show_histogram(self, parent, data, n, title):
        '''
        Отображает гистограмму.
        :param parent: Родительский виджет.
        :param data: Данные для гистограммы.
        :param n: Индекс параметра.
        :param title: Заголовок гистограммы.
        '''
        
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        # Создаём фрейм для гистограммы
        histogram_frame = tk.Frame(parent)
        histogram_frame.grid(row=2, column=1, columnspan=50, rowspan = 50, sticky='nsew', padx=5, pady=5)

        # Получаем гистограмму от контроллера
        fig = self.controller.get_histogram(data, n, title)

        if fig is None:
            return  # Если гистограмма не создана, выходим

        # Настройка размера и расположения
        fig.set_size_inches(5, 3)  # Увеличиваем размер
        fig.tight_layout()  # Вызываем после изменения размера

        # Встраиваем гистограмму в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=histogram_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
    
    # -----------------------------------------------------------
    #Фильтр------------------------------------------------------
    def filter_data(self):
        #Обрабатывает нажатие кнопки 'Пересчитать'.

        if not self.array_post_filter:  # Проверяем, пуст ли список
            array = self.data
        else:
            array = self.array_post_filter
        
       
        selected_param = self.param_combobox.get()  # Получаем выбранный параметр
        param_index = self.get_param_index(selected_param) # Определяем индекс параметра
        
        min_Rho = self.entry_Rho_min.get()  # Получаем значение из поля ввода
        max_Rho = self.entry_Rho_max.get()  # Получаем значение из поля ввода
        
        # Фильтруем данные
        self.array_post_filter = self.controller.filter_data_c(array, min_Rho, max_Rho, param_index)
    
        # Показываем гистограмму с отфильтрованными данными
        self.show_histogram(self.body_tab, self.array_post_filter, param_index , f'Гистограмма для {selected_param}')
        self.ui.update_message(f'Текущее количество строк массива: {len(self.array_post_filter)}')
        
        
        
    def reset_filter(self):
        
        selected_param = self.param_combobox.get()  # Получаем выбранный параметр
        param_index = self.get_param_index(selected_param) # Определяем индекс параметра
        
        self.entry_Rho_min.delete(0, tk.END)
        self.entry_Rho_max.delete(0, tk.END)
        self.array_post_filter = self.data
        
        self.show_histogram(self.body_tab, self.array_post_filter, param_index, selected_param)
        self.ui.update_message(f'Сброс массива, количество строк: {len(self.array_post_filter)}')
        
        
        
    def apply_filter(self):
        if self.array_post_filter:  
            self.data = self.array_post_filter
            self.ui.update_message(f'Массив обрезан, количество строк: {len(self.data)}')
            
            
            
    def recovery_filter (self):
        
        
        selected_param = self.param_combobox.get()  # Получаем выбранный параметр
        param_index = self.get_param_index(selected_param) # Определяем индекс параметра
        
        self.data = self.data_recovery  

        self.array_post_filter = list()
        self.entry_Rho_min.delete(0, tk.END)
        self.entry_Rho_max.delete(0, tk.END)

        
        self.show_histogram(self.body_tab, self.data, param_index, selected_param)
        self.ui.update_message(f'Возврат массива к исходному состоянию, количество строк: {len(self.data)}')
    
    
    
    
    # -----------------------------------------------------------
    #XYZRho------------------------------------------------------
    
    
    def safe_xyz_rho(self):
        
        path = filedialog.asksaveasfilename(
            defaultextension='.dat', # Автоматически добавляет .dat, если пользователь не указал расширение
            filetypes=[('DAT files', '*.dat'), ('All files', '*.*')],  # Фильтр для расширений
            title='Сохранить файл') #Заголовок
        
        if path:
            array = self.data  # Данные для сохранения
            
            # Вызываем метод контроллера для сохранения данных
            
            
            self.controller.processing_xyzrho(array, self.type_array, path)
            
            
            self.ui.update_message(f'Файл {self.type_array} сохранен: {path}')  # Сообщение об успешном сохранении
        else:
            self.ui.update_message('Сохранение отменено')  # Сообщение, если пользователь отменил сохранение
        
        
        pass
    
    
    
    
    # -----------------------------------------------------------




    def safe_data(self):
        # Получаем значения из полей ввода
        zagolovok_file = self.entry_zagolovok.get()  # Заголовок файла
        a = float(self.entry_a.get())  # Параметр a
        #Открываем диалоговое окно для выбора места сохранения
        path = filedialog.asksaveasfilename(
            defaultextension='.dat', # Автоматически добавляет .dat, если пользователь не указал расширение
            filetypes=[('DAT files', '*.dat'), ('All files', '*.*')],  # Фильтр для расширений
            title='Сохранить файл') #Заголовок
    
        if path:
            array = self.data  # Данные для сохранения
            # Вызываем метод контроллера для сохранения данных
            self.controller.safe_data(path, array, zagolovok_file, a)
            self.ui.update_message(f'Файл сохранен: {path}')  # Сообщение об успешном сохранении
        else:
            self.ui.update_message('Сохранение отменено')  # Сообщение, если пользователь отменил сохранение




    def get_frame(self):
        """
        Возвращает фрейм вкладки.
        """
        return self.frame
  