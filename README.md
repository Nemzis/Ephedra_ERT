Всем привет! Меня зовут Степченков Владимир. 
Я работаю в лаборатории инженерной электроразведки в МГУ. Для некоторых нужд я пишу небольшую программу, которой готов поделиться с вами.

Программа обрабоки и подготовки к инверсии файлов площадной электротомографии Ephedra_ERT.
- Планируется выход файла .exe
- Расширение функционала до редактирование и сохранение файлов различных установок
- Отдельное сохранение кажущегося сопротивления  для каждой установки в виде формата XYZRho

v1:
• Загрузка файлов типа .txt 
Формат:
Rho Spa.1 Spa.2 Spa.3 Spa.4 PassTime DutyCycle Vp In Dev.  K   Phase   Ay  By  My  Ny
Rho	M1	M2	M3	M4	M5	M6	M7	M8	M9	M10	M11	M12	M13	M14	M15	M16	M17	M18	M19	M20	M	Spa.1	Spa.2	Spa.3	Spa.4	PassTime	DutyCycle	Vp	In	K	Phase	Ay	By	My	Ny
- Разделение файлов на разные установки (Pole-Dipole, Dipole-Dipole, Schlumberge)
- Простая фильтрация 
- Сохранение файла без разделения на установки

v0:
Полностью написана и реализована на языке Python в програмной среде Anaconda в редакторе JupyterLab.
Ввиду узости и срецефичности настроек выкладыватся не будет.
Постепенно её функционал дорабатывается и переносится в v1
