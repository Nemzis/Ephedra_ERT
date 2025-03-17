# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 01:47:27 2025

@author: Vladimir
"""


from controller.controller import Controller
from view.ui import UI
import tkinter as tk


#Nuitka
#MVC (Model-View-Controller)

if __name__ == "__main__":
    
    # Создаем UI
    root = tk.Tk()
    ui = UI(root, None)
    
    # Создаем контроллер и передаем ему UI
    controller = Controller(ui)
    
    # Обновляем ссылку на контроллер в UI
    ui.controller = controller
    

    # Запускаем приложение
    ui.run()


