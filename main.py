# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:47:27 2025

@author: Vladimir
'''


from controller.controller import Controller
from view.ui import UI
import tkinter as tk


#Nuitka
#MVC (Model-View-Controller)


if __name__ == '__main__':
    
    # Создаем UI
    root = tk.Tk()
    ui = UI(root, None)
    
    # Создаем контроллер и передаем ему UI
    controller = Controller(ui)
    
    # Обновляем ссылку на контроллер в UI
    ui.controller = controller
    
    # Запускаем приложение
    ui.run()

'''
проблемы: 
    иногда не правильноработает функция рассчета шага.. баг пока на нейден 


ближайщая модернизация: 
    функция прибавления файлов со сдвигом или без


    разрезание большой модели на куски
    рисование карты векторов относительно одного питающего электрода 
    
    работа с вп
    
    
ближашая разработка модулей:
    сборка профилей вместе по координатам
    

'''
