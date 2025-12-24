# -*- coding: utf-8 -*-
'''
Created on Mon Mar 17 01:50:15 2025

@author: Vladimir
'''


import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy 



class DataTab:
    
    def __init__(self, parent, ui, data, controller, type_array):
        self.controller = controller
        self.parent = parent
        self.ui = ui  # Сохраняем ссылку на UI
        self.data = data
        self.data_recovery = copy.deepcopy(self.data)
        
        self.type_array = type_array
        self.array_post_filter = list()
        #эта хрень должна быть последней
        self.frame = self.create_data_tab()


    def create_data_tab(self):
        
        
        self.body_tab = ttk.Frame(self.parent)
        

        w = 20 #общая ширина кнопок
        
        self.button_safe_all = ttk.Button(self.body_tab, width=25, text = 'Сохранить файл (Res3Dinv)', command = self.safe_data)
        self.button_safe_all.grid(row=0, column=0, pady = 5, padx = 5, sticky='nsew')
        

        self.button_safe_rho = ttk.Button(self.body_tab, width=25, text = 'Сохранить файл XYZR', state='normal', command = self.safe_xyz_rho)
        self.button_safe_rho.grid(row=1, column=0, pady = 5, padx = 5, sticky='nsew')
        

        if self.type_array == 'all_data':
            self.button_safe_rho.config(state='disabled')
            
            
        self.button_safe_rho = ttk.Button(self.body_tab, width=25, text = 'Сохранить файл PyGimli', command = self.safe_PyGimli)
        self.button_safe_rho.grid(row=2, column=0, pady = 5, padx = 5, sticky='nsew')
            
        open_apply = ttk.Button(self.body_tab, width=25, text='Восстановить исходный\nмассив', command = self.recovery_filter )
        open_apply.grid(row=3, column=0, padx = 5, pady = 5,  sticky='nsew')
            

       
        # -----------------------------------------------------------
        self.customer_frame = tk.LabelFrame(self.body_tab, text='Сохранение Файла')
        self.customer_frame.grid(row=4, rowspan = 4, column=0, padx=5, pady=5, sticky='nsew')
        
        # Поле ввода для заголовка файла
        label_zagolovok = tk.Label(self.customer_frame, text='Заголовок Res3Dinv:')
        label_zagolovok.grid(row=0, column=0, sticky='wn', pady = 5, padx = 5)
        
        self.entry_zagolovok = tk.Entry(self.customer_frame, width=15)
        self.entry_zagolovok.grid(row=1, column=0, sticky='w', pady = 5, padx = 5)
        self.entry_zagolovok.insert(0, 'Test')
        

        
    
        # -----------------------------------------------------------
        self.customer_frame_filter = tk.LabelFrame(self.body_tab, text='Фильтр по диапазону')
        self.customer_frame_filter.grid(row=8, column=0, rowspan = 8, padx=10, pady=10, sticky='nsew')
        
        
        label_Rho_min = tk.Label(self.customer_frame_filter, text='Минимум')
        label_Rho_min.grid(row=0, column=0, sticky='nsew', pady = 5, padx = 5)
        
        self.entry_Rho_min = tk.Entry(self.customer_frame_filter, width=10)
        self.entry_Rho_min.grid(row=1, column=0, sticky='nsew', pady = 5, padx = 5)
        
        label_Rho_max = tk.Label(self.customer_frame_filter, text='Максимум')
        label_Rho_max.grid(row=2, column=0, sticky='nsew', pady = 5, padx = 5)
        
        self.entry_Rho_max = tk.Entry(self.customer_frame_filter, width=10)
        self.entry_Rho_max.grid(row=3, column=0, sticky='nsew', pady = 5, padx = 5)
        
        
        open_rasschet = ttk.Button(self.customer_frame_filter, width = w, text='Рассчитать', command = self.filter_data)
        open_rasschet.grid(row=4, column=0, padx = 5, pady = 5, sticky='nsew')
        
        open_sbros = ttk.Button(self.customer_frame_filter, width = w, text='Сбросить', command = self.reset_filter)
        open_sbros.grid(row=5, column=0, padx = 5, pady = 5, sticky='nsew')
        
        open_apply = ttk.Button(self.customer_frame_filter, width = w, text='Применить', command = self.apply_filter)
        open_apply.grid(row=6, column=0, padx = 5, pady = 5, sticky='nsew')
        

        
        
        
        # -----------------------------------------------------------
        #Гистограмма 
        self.show_histogram(self.body_tab, self.data, 1, 'Rho')
        
        self.customer_frame_histogram = tk.LabelFrame(self.body_tab, text='Управление гистрограммой')
        self.customer_frame_histogram.grid(row=0, column=1, rowspan = 2, padx=10, pady=10, sticky='nsew')
        
        # Создаём выпадающий список
        if len(self.data[0]) > 17:
            self.param_combobox = ttk.Combobox(self.customer_frame_histogram, values=['Rho', 'V (mV)', 'I (mA)', 'K', 'M'])
            self.param_combobox.grid(row=1, column=0, padx=5, pady=5, sticky='wn')
            self.param_combobox.current(0)  # Устанавливаем значение по умолчанию (Rho)
        else:
            self.param_combobox = ttk.Combobox(self.customer_frame_histogram, values=['Rho', 'V (mV)', 'I (mA)', 'K'])
            self.param_combobox.grid(row=1, column=0, padx=5, pady=5, sticky='wn')
            self.param_combobox.current(0)  # Устанавливаем значение по умолчанию (Rho)
        
        # Кнопка для отображения гистограммы
        show_button = ttk.Button(self.customer_frame_histogram, text='Обновить гистограмму', command = self.show_histogram_wrapper)
        show_button.grid(row=2, column=0, padx=5, pady=5, ipadx=1, ipady=0, sticky='wn')
        
        
        # -----------------------------------------------------------
        #исправляем шаг
        self.customer_frame_step = tk.LabelFrame(self.body_tab, text='Множитель X Y R')
        self.customer_frame_step.grid(row=0, column=2, rowspan = 2, padx=10, pady=10, sticky='nsew')
        
        self.entry_step_x = tk.Entry(self.customer_frame_step, width = 6)
        self.entry_step_x.grid(row=0, column=0, sticky='wn', pady = 5, padx = 5)
        
        self.entry_step_y = tk.Entry(self.customer_frame_step, width = 6)
        self.entry_step_y.grid(row=0, column=1, sticky='wn', pady = 5, padx = 5)
        
        self.entry_step_r = tk.Entry(self.customer_frame_step, width = 6)
        self.entry_step_r.grid(row=0, column=2, sticky='wn', pady = 5, padx = 5)
        
        
        open_step = ttk.Button(self.customer_frame_step, width = w, text='Умножить', command = self.multiply_array)
        open_step .grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=0, sticky='nsew', columnspan = 3)
        

        # -----------------------------------------------------------
        #график
        
        self.customer_frame_plot = tk.LabelFrame(self.body_tab, text='Управление графиком')
        self.customer_frame_plot.grid(row=0, column=4, rowspan = 2, padx=10, pady=10, sticky='nsew')
        

        self.param_plot = ttk.Combobox(self.customer_frame_plot, values=['A', 'B', 'M', 'N', 'Rho(Omm)/V(mV)'])
        self.param_plot.grid(row=0, column=0, padx=5, pady=5, sticky='wn')
        self.param_plot.current(0)  # Устанавливаем значение по умолчанию (Rho)
        
        # Кнопка для отображения гистограммы
        show_button = ttk.Button(self.customer_frame_plot, text='Обновить график', command=self.show_plot_wrapper)
        show_button.grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=0, sticky='nsew')
        
        
        

        return self.body_tab
    

    
    # -----------------------------------------------------------
    #PyGimli ----------------------------------------------------

    
    def safe_PyGimli(self):

    
        path = filedialog.asksaveasfilename(
            defaultextension='.dat', # Автоматически добавляет .dat, если пользователь не указал расширение
            filetypes=[('DAT files', '*.dat'), ('All files', '*.*')],  # Фильтр для расширений
            title='Сохранить файл') #Заголовок
        
        
        self.controller.processing_array_for_PyGimli(path, self.data)
        self.ui.update_message('Файл PyGimli записан')
    
    
    
    
    # -----------------------------------------------------------
    #Умножение --------------------------------------------------
    

    def multiply_array(self):
        
        # Получаем выбранный параметр
        selected_param = self.param_combobox.get()
        # Определяем индекс параметра
        param_index = self.get_param_index(selected_param)
        
        x = self.entry_step_x.get()
        y = self.entry_step_y.get()
        r = self.entry_step_r.get()
        
        
        if not self.array_post_filter:  # Проверяем, пуст ли список
            array = self.data
        else:
            array = self.array_post_filter
        
        if x == '' and y == '' and r == '':
            pass
        else:
            self.array_post_filter = self.controller.multiply(array, x, y, r)
            self.show_histogram(self.body_tab, self.array_post_filter, param_index, f'Гистограмма для {selected_param}')
    
    #Гистрограмма -----------------------------------------------
    # -----------------------------------------------------------
    
    def show_histogram_wrapper(self):
        
        #Обёртка для вызова show_histogram с правильным параметром.
        # Получаем выбранный параметр
        selected_param = self.param_combobox.get()
        # Определяем индекс параметра
        param_index = self.get_param_index(selected_param)
        
        self.entry_Rho_min.delete(0, tk.END)
        self.entry_Rho_max.delete(0, tk.END)

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
        self.histogram_frame = tk.Frame(parent)
        self.histogram_frame.grid(row=2, column=1, columnspan=50, rowspan = 50, sticky='nsew', padx=5, pady=5)

        # Получаем гистограмму от контроллера
        fig = self.controller.get_histogram(data, n, title)

        if fig is None:
            return  # Если гистограмма не создана, выходим

        # Настройка размера и расположения
        fig.set_size_inches(5, 3)  # Увеличиваем размер
        fig.tight_layout()  # Вызываем после изменения размера

        # Встраиваем гистограмму в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        
        

    def show_plot_wrapper(self):
        if self.param_plot.get() == 'A':
            a = 2
            b = 13
        elif self.param_plot.get() == 'B':
            a = 3
            b = 14
        elif self.param_plot.get() == 'M':
            a = 4
            b = 15
        elif self.param_plot.get() == 'N':
            a = 5
            b = 16
        elif self.param_plot.get() == 'Rho(Omm)/V(mV)':
            a = 1
            b = 8


        # Вызываем функцию show_histogram
        self.show_plot(self.histogram_frame, self.data, a, b)


    def show_plot(self, parent, data, a, b):
        

        # Очищаем фрейм перед созданием нового графика
        for widget in parent.winfo_children():
            widget.destroy()

        # Создаём фрейм для графика
        plot_frame = tk.Frame(parent)
        plot_frame.grid(row=2, column=1, columnspan=50, rowspan=50, sticky='nsew', padx=5, pady=5)

        # Получаем график от контроллера
        fig = self.controller.get_plot(data, a, b)

        if fig is None:
            return  # Если график не создан, выходим

        
        
        # Встраиваем график в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        plot_frame.update_idletasks()

    
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
        self.ui.update_message(f'Текущее количество строк: {len(self.array_post_filter)}')
        
        
        
    def reset_filter(self):
        
        selected_param = self.param_combobox.get()  # Получаем выбранный параметр
        param_index = self.get_param_index(selected_param) # Определяем индекс параметра
        
        self.entry_Rho_min.delete(0, tk.END)
        self.entry_Rho_max.delete(0, tk.END)
        self.array_post_filter = self.data
        
        self.show_histogram(self.body_tab, self.array_post_filter, param_index, selected_param)
        self.ui.update_message(f'Сброс, количество строк: {len(self.array_post_filter)}')
        
        
        
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
        
        self.entry_step_x.delete(0, tk.END)
        self.entry_step_y.delete(0, tk.END)
        self.entry_step_r.delete(0, tk.END)

        
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
        

    
    
    
    
    # -----------------------------------------------------------
    def safe_data(self):
        # Получаем значения из полей ввода
        zagolovok_file = self.entry_zagolovok.get()  # Заголовок файла
        
        #Открываем диалоговое окно для выбора места сохранения
        path = filedialog.asksaveasfilename(
            defaultextension='.dat', # Автоматически добавляет .dat, если пользователь не указал расширение
            filetypes=[('DAT files', '*.dat'), ('All files', '*.*')],  # Фильтр для расширений
            title='Сохранить файл') #Заголовок
    
        if path:
            array = self.data  # Данные для сохранения
            # Вызываем метод контроллера для сохранения данных
            self.controller.safe_data(path, array, zagolovok_file)
            self.ui.update_message(f'Файл сохранен: {path}')  # Сообщение об успешном сохранении
        else:
            self.ui.update_message('Сохранение отменено')  # Сообщение, если пользователь отменил сохранение





    def get_frame(self):
        '''
        Возвращает фрейм вкладки.
        '''
        return self.frame
  