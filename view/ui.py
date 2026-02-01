# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:51:23 2025
@author: Vladimir
'''
import tkinter as tk
from tkinter import ttk, filedialog
from view.ui_tab import DataTab  # Импортируем класс DataTab для вкладок
from module.komarov_sp.ui_KomarovSP import Komarov_SP
from module.Sim.ui_Sim import Sim



class UI:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title('Ephedra_ERT v2.3.2 2025')
        
        # Устанавливаем минимальные размеры окна
        self.root.minsize(width=850, height=700)
        
        # Создаем Notebook (контейнер для вкладок)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Создаем вкладку для основной программы
        self.create_main_tab()
        

        # Создаем текстовое поле для сообщений с прокруткой
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=15)
        
        
    
        self.message_area = tk.Text(self.message_frame, height=5, wrap=tk.WORD)
        self.message_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    
        # Добавляем прокрутку
        scrollbar = tk.Scrollbar(self.message_frame, command=self.message_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_area.config(yscrollcommand=scrollbar.set)
        

        

        # Создаем вкладку модуля Комаров ВП
        komarov_tab_instance = Komarov_SP(self.notebook, self)
        self.notebook.add(komarov_tab_instance.get_frame(), text='ВП методом вычитания КС')
    
        # Создаем вкладку модуля Sim
        Sim_tab_instance = Sim(self.notebook, self)
        self.notebook.add(Sim_tab_instance.get_frame(), text='VolDiff')
  
    
        
    def create_main_tab(self): 
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text='Обработка 3D прямоугольная сетка')
        
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
        #Создает псевдоменю 'Файл' внутри вкладки.
        # Фрейм для псевдоменю
        menu_frame = tk.Frame(parent)
        menu_frame.grid(row=0, column=0, padx = 5, pady = 5, sticky='wn')
        
        open_button = ttk.Button(menu_frame, text='Выбрать директорию\nс файлами', command = self.open_directory)
        open_button.grid(row=0, column=0, padx = 5, pady = 5, ipadx=5, ipady=5, sticky='nsew')
        

        #поле домножение шага
        self.customer_frame_step = tk.LabelFrame(menu_frame, text='Множитель X Y R перед загрузкой')
        self.customer_frame_step.grid(row=0, column = 2, rowspan = 3, padx=5, pady=5, sticky='nsew')
        
        self.entry_step_x = tk.Entry(self.customer_frame_step, width = 6)
        self.entry_step_x.grid(row=0, column=2, sticky='wn', pady = 5, padx = 5)
        
        self.entry_step_y = tk.Entry(self.customer_frame_step, width = 6)
        self.entry_step_y.grid(row=0, column=3, sticky='wn', pady = 5, padx = 5)
        
        self.entry_step_r = tk.Entry(self.customer_frame_step, width = 6)
        self.entry_step_r.grid(row=0, column=4, sticky='wn', pady = 5, padx = 5)
        
        
        
        # main
        self.nested_frame = tk.Frame(parent)
        self.nested_frame.grid(row=1, column=0, padx = 5, pady = 5, sticky='wn')
             
        # Создаем вложенный Notebook
        self.nested_notebook = ttk.Notebook(self.nested_frame)
        self.nested_notebook.grid(row=0, column=0, pady = 5, padx = 5, sticky='wn')
        

        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню 'File'
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='About')
        menubar.add_cascade(label = 'About', menu = file_menu)
        # Добавляем меню в окно
        self.root.config(menu = menubar)
      
        
        
        
    def open_directory(self):
        #Открывает директорию и создаёт вкладки с данными.
        # Очищаем данные
        self.pole_dipole = list()
        
        self.pole_dipole_X_sistem = list() 
        self.pole_dipole_L_sistem = list()
        
        self.dipole_dipole = list()
        self.dipole_dipole_X_sistem = list()
        self.dipole_dipole_L_sistem = list()
        
        self.schlumberger = list()
        self.data = list()
        
        
        x = self.entry_step_x.get()
        y = self.entry_step_y.get()
        r = self.entry_step_r.get()
        
        self.pl_messege = 0
    
        try:
            # Выбираем директорию
            selected_dir = filedialog.askdirectory(title='Выберите директорию')
            if not selected_dir:
                self.update_message('Директория не выбрана')
                return
    
            self.input_dir.set(selected_dir)
            self.controller.process_files(input_dir=selected_dir)
    
            # Очищаем все существующие вкладки
            for tab_id in self.nested_notebook.tabs():
                self.nested_notebook.forget(tab_id)
    
            # Получаем данные
            try:
                self.pole_dipole, self.pole_dipole_X_sistem, self.pole_dipole_L_sistem,\
                    self.dipole_dipole, self.dipole_dipole_L_sistem, self.dipole_dipole_X_sistem,\
                        self.schlumberger, self.pl_messege, self.data = self.controller.processing_file(x,y,r)
                        
                        
    
                # Создаём вкладки
                if self.data:
                    body_tab_instance = DataTab(self.notebook, self, self.data, self.controller, 'all_data')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Весь Массив')
    
                if self.dipole_dipole:
                    body_tab_instance = DataTab(self.notebook, self, self.dipole_dipole, self.controller, 'Dipole-Dipole')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Dipole-Dipole')
                                      
                if self.dipole_dipole_X_sistem:
                    body_tab_instance = DataTab(self.notebook, self, self.dipole_dipole_X_sistem, self.controller, 'Dipole-Dipole_X_sistem')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Dipole-Dipole_X_sistem')
                    
                if self.dipole_dipole_L_sistem:
                    body_tab_instance = DataTab(self.notebook, self, self.dipole_dipole_L_sistem, self.controller, 'Dipole-Dipole_L_sistem')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Dipole-Dipole_L_sistem')
                    

    
                if self.schlumberger:
                    body_tab_instance = DataTab(self.notebook, self, self.schlumberger, self.controller, 'Schlumberge')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Schlumberge')
    

    
                if self.pole_dipole:
                    body_tab_instance = DataTab(self.notebook, self, self.pole_dipole, self.controller, 'Pole-Dipole')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Pole-Dipole')
                
                if self.pole_dipole_X_sistem:
                    body_tab_instance = DataTab(self.notebook, self, self.pole_dipole_X_sistem, self.controller, 'Pole_dipole_X_sistem')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Pole_dipole_X_sistem')
                    
                if self.pole_dipole_L_sistem:
                    body_tab_instance = DataTab(self.notebook, self, self.pole_dipole_L_sistem, self.controller, 'Pole_dipole_L_sistem')
                    self.nested_notebook.add(body_tab_instance.get_frame(), text='Pole_dipole_L_sistem')
                    

    
                # Обновляем сообщение
                self.update_message(
                    f'Данные разделены\n'
                    f'{len(self.dipole_dipole)} - дипольная\n'
                    f'{len(self.dipole_dipole_X_sistem)} - дипольная система Х\n'
                    f'{len(self.dipole_dipole_L_sistem)} - дипольная система L\n'
                    f'{len(self.schlumberger)} - шлюмберже\n'
                    f'{len(self.pole_dipole)} - трехэлектродка\n'
                    f'{len(self.pole_dipole_X_sistem)} - трехэлектродка система Х\n'
                    f'{len(self.pole_dipole_L_sistem)} - трехэлектродка система L\n'
                    f'{self.pl_messege} - Удалено элекродов M и N равноудаленных от A (Pole-Dipole)\n'

                )
    
            except Exception as e:
                self.update_message(f'Ошибка при разделении данных: {e}')
    
        except Exception as e:
            self.update_message(f'Ошибка при выборе директории: {e}')
            
    
            
    # Метод для обновления сообщения
    def update_message(self, message):
        # Добавляем сообщение в текстовое поле
        self.message_area.insert(tk.END, message + '\n')
        # Прокручиваем до конца, чтобы новое сообщение было видно
        self.message_area.see(tk.END)
        
        
    def run(self):
        self.root.mainloop()