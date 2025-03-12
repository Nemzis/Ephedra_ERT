# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:51:23 2025
@author: Vladimir
'''
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#импорт других модулей программы
import view.ui_KomarovSP as KSP


class UI:
    
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title('Ephedra_ERT')
        
        # Устанавливаем минимальные размеры окна
        self.root.minsize(width = 800, height = 600)  # Минимальная ширина 600, высота 400
        
        # Создаем Notebook (контейнер для вкладок)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Создаем вкладку для основной программы
        self.create_main_tab()
        
        self.create_settings_tab()  # Добавляем вкладку с настройками
        
        
    def create_main_tab(self): 
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text='Обработка 3D')
        
        # Создаем меню
        self.create_menu()
        
        # Создаем псевдоменю 'Файл' внутри вкладки
        self.create_menu_tab(main_tab)
    
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        # Frame для основного содержимого
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #текстовое поле
        self.message_var = tk.StringVar(value = '')
        label_message = tk.Label(self.root, textvariable=self.message_var, bg='lightgray')
        label_message.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
       
        
    def create_menu_tab(self, parent):
        #Создает псевдоменю 'Файл' внутри вкладки.
        # Фрейм для псевдоменю
        menu_frame = tk.Frame(parent)
        menu_frame.grid(pady = 5, padx = 5)
        
        open_button = tk.Button(menu_frame, text='Выбрать директорию', command = self.open_directory)
        open_button.grid(row=0, column=0, padx = 5, pady = 5, sticky='wn')
        
           
        # Фрейм для вложенных вкладок
        nested_frame = tk.Frame(parent)
        nested_frame.grid(pady = 5, sticky='w')
        # Создаем вложенный Notebook
        self.nested_notebook = ttk.Notebook(nested_frame)
        self.nested_notebook.grid(row=1, column=0, sticky='w')
        
        # Общая вкладка 
        self.nested_tab_all = ttk.Frame(self.nested_notebook)
        self.nested_notebook.add(self.nested_tab_all, text='Весь массив данных')
        self.button_safe_all = tk.Button(self.nested_tab_all, 
                                         state='disabled',
                                         text = 'Сохранить файл (Res3Dinv)', 
                                         command = self.safe_data)
        self.button_safe_all.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')
                
        
        # Поле ввода для заголовка файла
        label_zagolovok = tk.Label(self.nested_tab_all, text='Заголовок файла \n Res3Dinv:')
        label_zagolovok.grid(row=2, column=0, sticky='wn')
        self.entry_zagolovok = tk.Entry(self.nested_tab_all)
        self.entry_zagolovok.grid(row=3, column=0, sticky='w')
        
        # Поле ввода для параметра шага
        label_a = tk.Label(self.nested_tab_all, text='Половина расстояния \n между электродами')
        label_a.grid(row=4, column=0, sticky='wn')
        self.entry_a = tk.Entry(self.nested_tab_all)
        self.entry_a.grid(row=5, column=0, sticky='wn')
                
        
        label_diap = tk.Label(self.nested_tab_all, text='\n Диапазон данных:')
        label_diap.grid(row=6, column=0, sticky='wn')
          
        label_Rok_min = tk.Label(self.nested_tab_all, text='Минимум')
        label_Rok_min.grid(row=7, column=0, sticky='wn')
        self.entry_Rok_min = tk.Entry(self.nested_tab_all)
        self.entry_Rok_min.grid(row=8, column=0, sticky='wn')
               
        label_Rok_max = tk.Label(self.nested_tab_all, text='Максимум')
        label_Rok_max.grid(row=9, column=0, sticky='wn')
        self.entry_Rok_max = tk.Entry(self.nested_tab_all)
        self.entry_Rok_max.grid(row=10, column=0, sticky='wn')
        
        open_rasschet = tk.Button(self.nested_tab_all, text='Рассчитать')
        open_rasschet.grid(row=11, column=0, padx = 5, pady = 5, sticky='wn')
        
        
        
        
        # Добавляем содержимое во вторую вложенную вкладку
        self.nested_tab_SHL = ttk.Frame(self.nested_notebook)
        label_SHL = tk.Label(self.nested_tab_SHL)
        label_SHL.grid(pady = 2)
        
        
        # Добавляем содержимое во вторую вложенную вкладку
        self.nested_tab_PD = ttk.Frame(self.nested_notebook)
        label_PD = tk.Label(self.nested_tab_PD)
        label_PD.grid(pady = 2)
        
        #DD
        self.nested_tab_DD = ttk.Frame(self.nested_notebook)
        # Добавляем содержимое во вторую вложенную вкладку
        label_DD = tk.Label(self.nested_tab_DD)
        label_DD.grid(pady = 2)
        
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню 'File'
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='About')
        menubar.add_cascade(label = 'About', menu = file_menu)
        
        # Добавляем меню в окно
        self.root.config(menu = menubar)
        
    
    def open_directory(self):
        try:
            selected_dir = filedialog.askdirectory(title='Выберите директорию')
            if selected_dir:
                self.input_dir.set(selected_dir)
                self.controller.process_files(input_dir = selected_dir)
             
                try:
                    self.pole_dipole, self.dipole_dipole, self.schlumberger, self.data  = self.controller.processing_file()
                    
                    self.show_histogram(self.nested_tab_all, self.data, 1, 'KC')
                    self.button_safe_all.config(state='normal')
                   
            
                    if len(self.dipole_dipole) != 0:
                        self.nested_notebook.add(self.nested_tab_DD, text='Дипольная')
                        # Добавляем гистограмму 
                        self.show_histogram(self.nested_tab_DD, self.dipole_dipole, 1, 'KC')
                        
                        
                    if len(self.schlumberger) != 0:
                        self.nested_notebook.add(self.nested_tab_SHL, text='Шлюмберже')
                        # Добавляем гистограмму
                        self.show_histogram(self.nested_tab_SHL, self.schlumberger, 1, 'KC')
                        
                        
                        
                    if len(self.pole_dipole) != 0:
                        self.nested_notebook.add(self.nested_tab_PD, text='Трехэлектроджная установка') 
                        # Добавляем гистограмму
                        self.show_histogram(self.nested_tab_PD, self.pole_dipole, 1, 'KC')
                      
                    self.message_var.set(f'Данные разделены\n {len(self.pole_dipole)} - трехэлектродка\n'\
                                         f'{len(self.dipole_dipole)} - дипольная\n'\
                                         f'{len(self.schlumberger)} - шлюмберже')
                        
                except Exception as e:
                    self.message_var.set(f'Ошибка при разделении данных: {e}')
                
            else:
                self.message_var.set('Директория не выбрана')
                
        except Exception as e:
            self.message_var.set(f'Ошибка при выборе директории: {e}')
            
    
    
    
    def show_histogram(self, parent, data, n, title):
        
        #histogram_frame = tk.Frame(parent)
        #histogram_frame.grid(row=0, column=1, columnspan=3, sticky='nsew')
        # Получаем гистограмму от контроллера
        fig = self.controller.get_histogram(data, n, title)  # Используем данные и параметры
        # Встраиваем гистограмму в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, padx = 5, pady = 5, columnspan = 5, rowspan = 5, sticky='wn')
       
        
        # Настройка grid для растягивания
        
        parent.grid_rowconfigure(1, weight=1)  # Вторая строка
        parent.grid_columnconfigure(0, weight=1)  # Первый столбец
        
        
        
        parent.grid_rowconfigure(0, weight=1, minsize=100)  # Минимальная высота 100 пикселей
        parent.grid_columnconfigure(0, weight=1, minsize=100)  # Минимальная ширина 100 пикселей
        
        
    def create_settings_tab(self):
        #Создает вкладку используя код из ui_KomarovSP.py.
        settings_tab = KSP.komarov_tab(self.notebook)
        self.notebook.add(settings_tab, text='Комаров ВП')
        
        
        
        
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
            self.message_var.set(f'Файл сохранен: {path}')  # Сообщение об успешном сохранении
        else:
            self.message_var.set('Сохранение отменено')  # Сообщение, если пользователь отменил сохранение
            
        
    # Метод для обновления сообщения
    def update_message(self, message):
        self.message_var.set(message)
    def run(self):
        self.root.mainloop()