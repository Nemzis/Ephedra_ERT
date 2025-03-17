# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:51:23 2025
@author: Vladimir
'''
import tkinter as tk
from tkinter import ttk, filedialog
#import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from view.ui_tab import DataTab  # Импортируем класс DataTab


from module.ui_KomarovSP import Komarov_SP


class UI:
    
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title('Ephedra_ERT')
        
        # Устанавливаем минимальные размеры окна
        self.root.minsize(width=800, height=600)  # Минимальная ширина 600, высота 400
        
        # Создаем Notebook (контейнер для вкладок)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Создаем вкладку для основной программы
        self.create_main_tab()
        
        
        
        
        
        #bottom_main
        # Создаем текстовое поле для сообщений с прокруткой
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
        self.message_area = tk.Text(self.message_frame, height=5, wrap=tk.WORD)
        self.message_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        # Добавляем прокрутку
        scrollbar = tk.Scrollbar(self.message_frame, command=self.message_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_area.config(yscrollcommand=scrollbar.set)
        
        
        
        # Создаем вкладку Комаров ВП
        komarov_tab_instance = Komarov_SP(self.notebook, self)  # Передаем self (UI) в Komarov_SP
        self.notebook.add(komarov_tab_instance.get_frame(), text='Комаров ВП')
        
        
        
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
 


        
    def create_menu_tab(self, parent):
        self.array_post_filter = list()
        
        #Создает псевдоменю 'Файл' внутри вкладки.
        # Фрейм для псевдоменю
        menu_frame = tk.Frame(parent)
        menu_frame.grid(row=0, column=0, padx = 5, pady = 5, sticky='wn')
        
        open_button = ttk.Button(menu_frame, text='Выбрать директорию', command = self.open_directory)
        open_button.grid(row=0, column=0, padx = 5, pady = 5, sticky='wn')
        
       
        # main
        self.nested_frame = tk.Frame(parent)
        self.nested_frame.grid(row=1, column=0, padx = 5, pady = 5, sticky='wn')
        

        
        # Создаем вложенный Notebook
        self.nested_notebook = ttk.Notebook(self.nested_frame)
        self.nested_notebook.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')
        
        
        # Общая вкладка 
        self.nested_tab_all = ttk.Frame(self.nested_notebook)
        self.nested_notebook.add(self.nested_tab_all, text='Весь массив данных')
        
        
        a = 0 #row
        
        
        self.button_safe_all = ttk.Button(self.nested_tab_all, 
                                         state='disabled',
                                         text = 'Сохранить файл (Res3Dinv)', 
                                         command = self.safe_data)
        self.button_safe_all.grid(row=a, column=0, pady = 5, padx = 5, sticky='wn')
        a += 1
        
        
        # Customer Details Frame
        self.customer_frame = tk.LabelFrame(self.nested_tab_all, text="Сохранение Файла")
        self.customer_frame.grid(row=a, column=0, padx=5, pady=5, sticky="NSEW")
        a += 1
        
        
        # Поле ввода для заголовка файла
        label_zagolovok = tk.Label(self.customer_frame, text='Заголовок Res3Dinv:')
        label_zagolovok.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        
        
        a += 1
        self.entry_zagolovok = tk.Entry(self.customer_frame, width=15)
        self.entry_zagolovok.grid(row=a, column=0, sticky='w', pady = 5, padx = 5)
        self.entry_zagolovok.insert(0, 'Test')
        
        
        a += 1
        # Поле ввода для параметра шага
        label_a = tk.Label(self.customer_frame, text='Половина расстояния\n между электродами')
        label_a.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        
        a += 1
        self.entry_a = tk.Entry(self.customer_frame, width=15)
        self.entry_a.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        self.entry_a.insert(0, '0.02')
        
        
        a += 1
        # Customer Details Frame
        self.customer_frame_filter = tk.LabelFrame(self.nested_tab_all, text="Фильтр по диапазону")
        self.customer_frame_filter.grid(row=a, column=0, padx=10, pady=10, sticky="NSEW")
        
        
        a += 1
        label_Rho_min = tk.Label(self.customer_frame_filter, text='Минимум')
        label_Rho_min.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        
        
        a += 1
        self.entry_Rho_min = tk.Entry(self.customer_frame_filter, width=10)
        self.entry_Rho_min.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        
        
        a += 1    
        label_Rho_max = tk.Label(self.customer_frame_filter, text='Максимум')
        label_Rho_max.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        
        
        a += 1
        self.entry_Rho_max = tk.Entry(self.customer_frame_filter, width=10)
        self.entry_Rho_max.grid(row=a, column=0, sticky='wn', pady = 5, padx = 5)
        
        
        w = 15
        
        a += 1
        open_rasschet = ttk.Button(self.customer_frame_filter, width = w, text='Рассчитать', command = self.filter_data)
        open_rasschet.grid(row=a, column=0, padx = 5, pady = 5)
        
        
        a += 1
        open_sbros = ttk.Button(self.customer_frame_filter, width = w, text='Сбросить', command = self.reset_filter)
        open_sbros.grid(row=a, column=0, padx = 5, pady = 5)
        
        a += 1
        open_apply = ttk.Button(self.customer_frame_filter, width = w, text='Применить', command = self.apply_filter)
        open_apply.grid(row=a, column=0, padx = 5, pady = 5)
        
        a += 1
        open_apply = ttk.Button(self.customer_frame_filter, width = w, text='Восстановить\nисходный\nмассив', command = self.recovery_filter )
        open_apply.grid(row=a, column=0, padx = 5, pady = 5)
        
        
        #---------------------------
        
        
        # Создаём выпадающий список
        self.param_combobox = ttk.Combobox(self.nested_tab_all, values=['Rho', 'V (mV)', 'I (mA)', 'K'])
        self.param_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='wn')
        self.param_combobox.current(0)  # Устанавливаем значение по умолчанию (Rho)

        # Кнопка для отображения гистограммы
        show_button = ttk.Button(self.nested_tab_all, text='Показать гистограмму', command = self.show_histogram_wrapper)
        show_button.grid(row=0, column=2, padx=5, pady=5, ipadx=1, ipady=0, sticky='wn')
        #---------------------------
        
        
        
        
        # Добавляем содержимое во вложенную вкладку
        self.nested_tab_SHL = ttk.Frame(self.nested_notebook)
        label_SHL = tk.Label(self.nested_tab_SHL)
        label_SHL.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')
        
        
        # Добавляем содержимое во вложенную вкладку
        self.nested_tab_PD = ttk.Frame(self.nested_notebook)
        label_PD = tk.Label(self.nested_tab_PD)
        label_PD.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')
        
        #DD
        self.nested_tab_DD = ttk.Frame(self.nested_notebook)
        # Добавляем содержимое во вложенную вкладку
        label_DD = tk.Label(self.nested_tab_DD)
        label_DD.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')
        
        

        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню 'File'
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='About')
        menubar.add_cascade(label = 'About', menu = file_menu)
        # Добавляем меню в окно
        self.root.config(menu = menubar)
        
        
        
    data_recovery = list()
    def open_directory(self):
        try:
            selected_dir = filedialog.askdirectory(title='Выберите директорию')
            if selected_dir:
                self.input_dir.set(selected_dir)
                self.controller.process_files(input_dir = selected_dir)
             
                try:
                    self.pole_dipole, self.dipole_dipole, self.schlumberger, self.data = self.controller.processing_file()
                    
                    self.data_recovery = self.data
                    self.show_histogram(self.nested_tab_all, self.data, 1, 'Rho')
                    
                    self.button_safe_all.config(state='normal')
                   
            
                    if len(self.dipole_dipole) != 0:
                        
                        #self.nested_notebook.add(self.nested_tab_DD, text='Дипольная')
                        

                        
                        body_tab_instance = DataTab(self.notebook, self, self.dipole_dipole)  
                        self.nested_notebook.add(body_tab_instance.get_frame(), text='Dipole-Dipole')
                        
                        
                        
                    if len(self.schlumberger) != 0:
                        
                        
                        body_tab_instance = DataTab(self.notebook, self, self.schlumberger)  
                        self.nested_notebook.add(body_tab_instance.get_frame(), text='Schlumberge')
                        
                        
                        
                    if len(self.pole_dipole) != 0:
                        self.nested_notebook.add(self.nested_tab_PD, text='Трехэлектроджная установка') 
                        # Добавляем гистограмму
                        self.show_histogram(self.nested_tab_PD, self.pole_dipole, 1, 'Rho')
                        
                        
                      
                    self.update_message(f'Данные разделены\n {len(self.pole_dipole)} - трехэлектродка\n'\
                                         f'{len(self.dipole_dipole)} - дипольная\n'\
                                         f'{len(self.schlumberger)} - шлюмберже')
                        
                except Exception as e:
                    self.update_message(f'Ошибка при разделении данных: {e}')
                
            else:
                self.update_message('Директория не выбрана')
                
        except Exception as e:
            self.update_message(f'Ошибка при выборе директории: {e}')
            
    
    
    def show_histogram_wrapper(self):
        
        #Обёртка для вызова show_histogram с правильным параметром.
        # Получаем выбранный параметр
        selected_param = self.param_combobox.get()
        # Определяем индекс параметра
        param_index = self.get_param_index(selected_param)

        # Вызываем функцию show_histogram
        self.show_histogram(self.nested_tab_all, self.data, param_index, f'Гистограмма для {selected_param}')
    
    
    
    def get_param_index(self, param):
        '''
        Возвращает индекс параметра.
        :param param: Выбранный параметр (Rho, V, I).
        :return: Индекс параметра.
        '''
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
        histogram_frame.grid(row=1, column=1, columnspan=50, rowspan = 50, sticky='nsew', padx=5, pady=5)

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
        self.show_histogram(self.nested_tab_all, self.array_post_filter, param_index , f'Гистограмма для {selected_param}')
        self.update_message(f'Текущее количество строк массива: {len(self.array_post_filter)}')
        
        
        
    def reset_filter(self):
        
        selected_param = self.param_combobox.get()  # Получаем выбранный параметр
        param_index = self.get_param_index(selected_param) # Определяем индекс параметра
        
        self.entry_Rho_min.delete(0, tk.END)
        self.entry_Rho_max.delete(0, tk.END)
        self.array_post_filter = self.data
        
        self.show_histogram(self.nested_tab_all, self.array_post_filter, param_index, selected_param)
        self.update_message(f'Сброс массива, количество строк: {len(self.array_post_filter)}')
        
        
        
    def apply_filter(self):
        if self.array_post_filter:  
            self.data = self.array_post_filter
            self.update_message(f'Массив обрезан, количество строк: {len(self.data)}')
            
            
            
    def recovery_filter (self):
        
        
        selected_param = self.param_combobox.get()  # Получаем выбранный параметр
        param_index = self.get_param_index(selected_param) # Определяем индекс параметра
        
        self.data = self.data_recovery  

        self.array_post_filter = list()
        self.entry_Rho_min.delete(0, tk.END)
        self.entry_Rho_max.delete(0, tk.END)

        
        self.show_histogram(self.nested_tab_all, self.data, param_index, selected_param)
        self.update_message(f'Возврат массива к исходному состоянию, количество строк: {len(self.data)}')

        
    
        
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
            self.update_message(f'Файл сохранен: {path}')  # Сообщение об успешном сохранении
        else:
            self.update_message('Сохранение отменено')  # Сообщение, если пользователь отменил сохранение
    
    
    
 
            
    # Метод для обновления сообщения
    def update_message(self, message):
        # Добавляем сообщение в текстовое поле
        self.message_area.insert(tk.END, message + "\n")
        # Прокручиваем до конца, чтобы новое сообщение было видно
        self.message_area.see(tk.END)
        
        
    def run(self):
        self.root.mainloop()