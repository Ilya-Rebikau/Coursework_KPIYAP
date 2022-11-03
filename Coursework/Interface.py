from tkinter import *
from Coursework import *
from tkinter.messagebox import showerror
import math
import matplotlib.pyplot as plt
from celluloid import Camera

#Создаю основное окно
window = Tk()
window.title("Определение параметров регрессионной зависимости")
window.geometry("1400x750")
window.config(bg = "MediumSpringGreen")
window.resizable(width = False, height = False)

#Отступы
global marginX, marginY
marginX = 10
marginY = 8

#Деление окна на сетку
for i in range(1):
    for j in range(2):
        frame = Frame(master=window)
        frame.grid(row=i, column=j)

#Присваиваю фреймам их места в окне
frame1 = Frame(window)
frame1.grid(row = 0, column = 0, padx = marginX, pady = marginY, sticky="nw")
frame2 = Frame(window)
frame2.grid(row = 0, column = 1, padx = marginX, pady = marginY, sticky="n")
frame3 = Frame(window)
frame3.grid(row = 0, column = 2, padx = marginX, pady = marginY, sticky="ne")
frame4 = Frame(window)
frame4.grid(row = 1, column = 1, padx = marginX, pady = marginY, sticky="s")

#Функция чтения из файла
def Read():
    text.config(state = NORMAL)
    text.delete(1.0, END)
    try:
        number, x, y = ReadFile()
        text.insert(END, "{:>25s}".format('Общехозяйственные') + "{:>11s}".format('Полная') + '\n' + "{:>26s}".format('и производственные') + "{:>15s}".format('фактическая') + '\n' + "{:>15s}".format('расходы') + "{:>28s}".format('себестоимость') + '\n' + "{:>5s}".format("№ п/п") + "{:>6s}".format('(x)') + "{:>22s}".format('(y)') + '\n')
        for i in range(len(number)):
            text.insert(END, "{:>3d}".format(number[i]) + "{:<5s}".format('.') + "{:<21s}".format(str(round(x[i], 3))) + ' ' + "{:<}".format(str(round(y[i], 3))) + '\n')
    except:
        showerror(title="Ошибка", message="Файл не найден!")
    text.config(state = DISABLED)

#Функция добавления строки в файл
def Add():
    #Создаю окно для ввода новой строки
    helpWindow = Tk()
    helpWindow.title("Добавление новой строки")
    helpWindow.config(bg = "MediumSpringGreen")
    helpWindow.resizable(width = False, height = False)
    helpWindow.geometry("190x120")

    #Делю окно на сетку
    for i in range(2):
        for j in range(1):
            helpFrame = Frame(master=helpWindow)
            helpFrame.grid(row=i, column=j)

    #Лабели и текстовые окна для ввода новых данных
    xLabel = Label(helpWindow, text="Введите x:", font=("TimesNewRoman", 10))
    xLabel.grid(row = 0, column = 0, padx = marginX, pady = marginY, sticky = "nw")
    xText = Entry(helpWindow, width = 11)
    xText.grid(row = 1, column = 0, padx = marginX, pady = marginY, sticky = "nw")
    yLabel = Label(helpWindow, text="Введите y:", font=("TimesNewRoman", 10))
    yLabel.grid(row = 0, column = 1, padx = marginX, pady = marginY, sticky = "nw")
    yText = Entry(helpWindow, width = 11)
    yText.grid(row = 1, column = 1, padx = marginX, pady = marginY, sticky = "nw")

    #Функция чтения из текстовых полей
    def ReadNew():
        try:
            newX = xText.get()
            newX = float(newX)
            newY = yText.get()
            newY = float(newY)
            try:
                if newX > 0 and newY > 0:
                    number, x, y = ReadFile()
                    AddLineInFile(number, newX, newY)
                    Read()
                else:
                    showerror(title="Ошибка", message="Введённые данные должны быть больше 0!")
            except:
                showerror(title="Ошибка", message="Файл не найден!")
        except:
            showerror(title="Ошибка", message="Введённые данные должны быть числами!")
        helpWindow.destroy()

    #Кнопка вызова функции чтения новых данных и закрытия вспомогательного окна
    button = Button(helpWindow, text="Добавить", font=("TimesNewRoman", 10), width = 7, command = ReadNew, bg = "LightGray")
    button.grid(row = 2, column = 1, padx = marginX, pady = marginY, sticky = "ne")
    helpWindow.mainloop()

#Функция удаления строки из файла
def Remove():
    #Создаю окно для ввода новой строки
    helpWindow = Tk()
    helpWindow.title("Удаление строки")
    helpWindow.config(bg = "MediumSpringGreen")
    helpWindow.resizable(width = False, height = False)
    helpWindow.geometry("240x120")

    #Делю окно на сетку
    for i in range(2):
        for j in range(0):
            helpFrame = Frame(master=helpWindow)
            helpFrame.grid(row=i, column=j)
    numberLabel = Label(helpWindow, text="Введите номер удаляемой строки:", font=("TimesNewRoman", 10))
    numberLabel.grid(row = 0, column = 0, padx = marginX, pady = marginY, sticky = "nw")
    numberText = Entry(helpWindow, width = 35)
    numberText.grid(row = 1, column = 0, padx = marginX, pady = marginY, sticky = "nw")

    #Функция чтения из текстовых полей
    def Delete():
        try:
            removeNumber = numberText.get()
            removeNumber = int(removeNumber)
            try:
                number, x, y = ReadFile()
                if removeNumber > 0 and removeNumber <= len(number):
                    DeleteLineInFile(number, x, y, removeNumber)
                    Read()
                else:
                    showerror(title="Ошибка", message="Введённой строки нет в файле!")
            except:
                showerror(title="Ошибка", message="Файл не найден!")
        except:
            showerror(title="Ошибка", message="Введённые данные должны быть порядковым номером строки!")
        helpWindow.destroy()

    #Кнопка вызова функции удаления строки и закрытия вспомогательного окна
    button = Button(helpWindow, text="Удалить", font=("TimesNewRoman", 10), width = 7, command = Delete, bg = "LightGray")
    button.grid(row = 2, column = 0, padx = marginX, pady = marginY, sticky = "ne")
    helpWindow.mainloop()

#Функция вывода результатов и вывода
def Results():
    try:
        number, x, y = ReadFile()
        result.config(state = NORMAL)
        result.delete(1.0, END)
        PairCorrelationCoefficientt = PairCorrelationCoefficient(x, y)
        result.insert(1.0, "Коэффициент парной корреляции: " + str(round(PairCorrelationCoefficientt, 3)))
        if math.fabs(PairCorrelationCoefficientt) > 0.5:
            result.insert(END, " - cвязь между х и у сильная\n\n")
            regression1, regression2 = Regressions(x, y)
            result.insert(END, "{:>25s}".format('Общехозяйственные') + "{:>11s}".format('Полная') + "{:>18s}".format('Значения') + "{:>13s}".format('Значения') + '\n' + "{:>26s}".format('и производственные') + "{:>15s}".format('фактическая') + "{:>11s}".format('первой') + "{:>13s}".format('второй') + '\n' + "{:>15s}".format('расходы') + "{:>28s}".format('себестоимость') +  "{:>12s}".format('регрессии') + "{:>13s}".format('регрессии') + '\n' + "{:>5s}".format("№ п/п") + "{:>6s}".format('(x)') + "{:>22s}".format('(y)') + "{:>16s}".format('(ŷ)') + "{:>13s}".format('(ỹ)') + '\n')
            for i in range(len(number)):
                result.insert(END, "{:>3d}".format(number[i]) + "{:5s}".format('.') + "{:<22s}".format(str(round(x[i], 3))) + "{:<16s}".format(str(round(y[i], 3))) + "{:<13s}".format(str(round(regression1[i], 3))) + "{:<}".format(str(round(regression2[i], 3))) + '\n')
            CoefficientOfTheFisher1, CoefficientOfTheFisher2 = CoefficientsOfTheFisher(x, y, regression1, regression2)
            result.insert(END, "\nКоэффициент Фишера 1-й регрессии:\n" + str(round(CoefficientOfTheFisher1, 3)) + '\n')
            result.insert(END, "Коэффициент Фишера 2-й регрессии:\n" + str(round(CoefficientOfTheFisher2, 3)) + '\n')
            if CoefficientOfTheFisher1 > CoefficientOfTheFisher2:
                result.insert(END, "Вывод: первая регрессия лучше")
            else:
                result.insert(END, "Вывод: вторая регрессия лучше")
        else:
            result.insert(END, " - cвязь слабая\n")
    except:
        showerror(title="Ошибка", message="Файл не найден!")
    result.config(state = DISABLED)

#Функция построения графика
def Graphics():
    try:
        number, x, y = ReadFile()
        regression1, regression2 = Regressions(x, y)
        x, y, regression1, regression2 = SortLists(x, y, regression1, regression2)
        CoefficientOfTheFisher1, CoefficientOfTheFisher2 = CoefficientsOfTheFisher(x, y, regression1, regression2)
        if math.fabs(PairCorrelationCoefficient(x, y)) > 0.5:
            #Создаю окно с графиком
            fig = plt.figure()
            plt.title('Зависимость полной фактической себестоимости\n от общехозяйственных и производственных расходов', fontsize=16, fontname='Times New Roman')
            plt.xlabel('Общехозяйственные и производственные расходы (х), BYN')
            plt.ylabel('Полная фактическая себестоимость (у), BYN')
            plt.grid(True)
            camera = Camera(fig)
            if CoefficientOfTheFisher1 > CoefficientOfTheFisher2:
                color1 = 'b'
                color2 = 'r'
                for i in range(len(x)):
                    point, = plt.plot(x[i], regression1[i], 'ko')
                    camera.snap()
            else:
                color1 = 'r'
                color2 = 'b'
                for i in range(len(x)):
                    point, = plt.plot(x[i], regression2[i],'ko')
                    camera.snap()
            animation = camera.animate(interval = 1, repeat = True, repeat_delay = 1)
            graph1, = plt.plot(x, y, '.g')
            graph2, = plt.plot(x, regression1, color1)
            graph3, = plt.plot(x, regression2, color2)
            plt.legend([graph1, graph2, graph3, point], ['y=f(x)', '1-я регрессия', '2-я регрессия', 'Бегущая точка по лучшей из регрессии'])
            plt.show()
        else:
            showerror(title="Ошибка", message="Связь между х и у слабая!")
    except:
        showerror(title="Ошибка", message="Файл не найден!")
        
#Лабель задачи
myself = Label(frame1, text="Определение параметров регрессионной\n зависимости полной фактической\n себестоимости (X) от общехозяйственных \nи производственных расходов (Y) \nПО «Гомелькабель»\n_________________________________________", font=("TimesNewRoman", 10))
myself.grid(padx = 0, pady = 0)

# Меню
menu = Label(frame1, text="Выберите пункт меню:\n________________________________", font=("TimesNewRoman", 12))
menu.grid(sticky = "n", pady = marginY)
menu_1 = Button(frame1, text="1. Вывести данные из файла на экран", font=("TimesNewRoman", 10), width = 35, command = Read, bg = "LightGray")
menu_1.grid(padx = marginX, pady = marginY)
menu_2 = Button(frame1, text="2. Добавить новую строку данных в файл", font=("TimesNewRoman", 10), width = 35, command = Add, bg = "LightGray")
menu_2.grid(padx = marginX, pady = marginY)
menu_3 = Button(frame1, text="3. Удалить строку данных из файла", font=("TimesNewRoman", 10), width = 35, command = Remove, bg = "LightGray")
menu_3.grid(padx = marginX, pady = marginY)
menu_4 = Button(frame1, text="4. Визуализация рассчитанных данных:\n коэффициент парной корреляции,\nзначения регрессий,\n коэффициенты Фишера.\n Сделать вывод, какая регрессия лучше", font=("TimesNewRoman", 10), width = 35, command = Results, bg = "LightGray")
menu_4.grid(padx = marginX, pady = marginY)
menu_5 = Button(frame1, text="5. Графическое представление зависимостей", font=("TimesNewRoman", 10), width = 35, command = Graphics, bg = "LightGray")
menu_5.grid(padx = marginX, pady = marginY)
menu_6 = Button(frame1, text="6. Выход из программы", font=("TimesNewRoman", 10), width = 35, command = window.destroy, bg = "LightGray")
menu_6.grid(padx = marginX, pady = marginY)

#Текстовое окно исходных данных
textLabel = Label(frame2, text="Исходные данные:\n________________________________________", font=("TimesNewRoman", 12))
textLabel.grid(sticky = "n", pady = marginY)
text = Text(frame2, width = 45, height = 37, state=DISABLED)
text.grid(padx = marginX, pady = marginY)
for i in range(1):
    for j in range(1):
        extraFrame = Frame(master=frame2)
        extraFrame.grid(row=i, column=j)
scroll = Scrollbar(frame2, command=text.yview)
scroll.grid(row = 1, column = 1, sticky="ns")
text.config(yscrollcommand=scroll.set)

#Текстовое окно результатов
resultLabel = Label(frame3, text="Результаты:\n__________________________________________________________________", font=("TimesNewRoman", 12))
resultLabel.grid(sticky = "n", pady = marginY)
result = Text(frame3, width = 73, height = 37, state=DISABLED)
result.grid(padx = marginX, pady = marginY)
for i in range(1):
    for j in range(1):
        extraFrame2 = Frame(master=frame2)
        extraFrame2.grid(row=i, column=j)
scroll = Scrollbar(frame3, command=result.yview)
scroll.grid(row = 1, column = 1, sticky="ns")
result.config(yscrollcommand=scroll.set)

#Лабель разработчика
myself = Label(frame4, text="Разработал:\nРебиков Илья Геннадьевич, группа ИТП-21", font=("TimesNewRoman", 12))
myself.grid(padx = 0, pady = 0)

window.mainloop()