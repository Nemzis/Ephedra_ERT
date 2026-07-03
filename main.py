# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 01:47:27 2025

@author: Vladimir
'''

# nuitka-project: --standalone
# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --windows-console-mode=disable

# nuitka-project: --include-data-dir=module=module
# nuitka-project: --include-data-dir=icon=icon

# nuitka-project: --output-filename=Ephedra_ERT

# nuitka-project: --company-name=Vladimir Stepchenkov
# nuitka-project: --product-name=Ephedra ERT
# nuitka-project: --file-description=Ephedra ERT
# nuitka-project: --file-version=2.8.7.0
# nuitka-project: --product-version=2.8.7.0
# nuitka-project: --file-description=Software for electrical resistivity tomography processing


from controller.controller import Controller
from view.ui import UI
import tkinter as tk



#MVC (Model-View-Controller)

def main():
    root = tk.Tk()
    ui = UI(root, None)
    controller = Controller(ui)
    ui.controller = controller
    ui.run()



if __name__ == "__main__":
    main()



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
    
   
Как заливать на гит
GIT
cd C:/Users/nemzi/.spyder-py3/Ephedra_ERT
git status
git add .

git commit -m "коммит"

git push


как компелировать: 
поставил Nuitka
pip install nuitka

python -m nuitka --version

в итоге: 
python -m nuitka main.py - из проекта

'''
