# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 23:39:39 2025

@author: Vladimir
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class SHL:
    def __init__(self, schlumberger):
        self.schlumberger = schlumberger  # Сохраняем ссылку на UI
        
        
        
        
        
    def filter_array(array, min_ROK, max_ROK):
        i = len(array) - 1
        while i >= 0:
            if array[i][1] < min_ROK:
                del array[i]
            elif array[i][1] > max_ROK:
                del array[i]
            i -= 1
        return array
    

        
    # простая диаграмма
    def gistogramma (array, a, title):
        # выбираем массив, индекс и подпись 
        data = []
        for i in range(len(array)):
            data.append(array[i][a])
        
        n = int((len(array))**(0.5))
        plt.title(title)
        plt.grid(which='major')
        plt.grid(which='minor', linestyle=':')
        plt.hist(data, bins = n)
        plt.xscale('log')
        plt.tight_layout()
        plt.show()