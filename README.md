Всем привет! Меня зовут Степченков Владимир. 
Я работаю в лаборатории инженерной электроразведки в МГУ. Для некоторых нужд я пишу небольшую программу, которой готов поделиться с вами.

-----------------------------------------

На данный момент. чтобы программа работала её нужно поместить в среду, например Spyder

- Ephedra_ERT v2.3.2 2025
Модули: 
- Komarov_Sp v1.2.2 2025
- Sim v0.1.1 2025

-----------------------------------------

version 2.4.2:
- введен формат вывода данных PyGimli
- проработан модуль Sim (v0.1.1 2025)



version 2.3.2:

- добавлен график и параметры работы с ним 
- введена функция поправки данных во время загрузки
- добавлен модуль Sim (v0.0.0 2025)
- испралена ошибка неправильного умножения при работе с функцией "умножить xyr"
- исправленна ошибка пропуска данных когда А и B == 9999.99999, M или N == 9999.99999


version 2:

- Возможность читать файлы с ВП
- Переработана стуктура: 
- Теперь вкладки создаются из отдельного файла шаблона
- Добавлена возможность умножения координат
- Сделан фильтр данных
- Добавлена возможность восстановления данных без перезагрузки
- Возможность сохранять файлы XYZR для программ типа Voxler

- метод Комарова выделен в отдельный модуль (v1.2.2 2025)
- Возможность загрузки файлов .txt и .dat
- Возможность сохранения настроек


version 1:
- Загрузка файлов типа .txt
  
Формат:

Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny

Rho	M1	M2	M3	M4	M5	M6	M7	M8	M9	M10	M11	M12	M13	M14	M15	M16	M17	M18	M19	M20	M	Spa.1	Spa.2	Spa.3	Spa.4	PassTime	DutyCycle	Vp	In	K	Phase	Ay	By	My	Ny
- Разделение файлов на разные установки (Pole-Dipole, Dipole-Dipole, Schlumberge)
- Простая фильтрация 
- Сохранение общего файла в формате программы Res3Dinv


version 0:

Полностью написана и реализована на языке Python в програмной среде Anaconda в редакторе JupyterLab.
Постепенно её функционал будет переноситься в данную программу
