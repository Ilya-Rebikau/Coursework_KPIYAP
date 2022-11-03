import math
#Функция чтения из файла, возвращает списки с номерами строк, значениями x и у
def ReadFile():
    readFile = open('TextInfo.txt', 'r')
    number = [] #Список с номерами строк
    x = [] #Список со значениями x
    y = [] #Список со значениями y
    stroka = [] #Вспомогательный список для деления строки на Number, x, y
    #Цикл для обработки строк и деления данных на списки
    for line in readFile:
        stroka = line.split()
        stroka[0] = stroka[0].replace('.', '') #Удаляю точку из номера строки, чтобы потом преобразовать в int
        number.append(int(stroka[0]))
        x.append(float(stroka[1]))
        #Условие проверяет является ли число целым, если да, то откидывает десятичную часть .0
        #if (x[len(x) - 1].is_integer()):
            #x[len(x) - 1] = int(x[len(x) - 1])
        y.append(float(stroka[2]))
        #if (y[len(y) - 1].is_integer()):
            #y[len(y) - 1] = int(y[len(y) - 1])
        stroka.clear()
    readFile.close()
    return number, x, y

#Функция добавления новой строки в файл, принимает списки с номерами строк, значениями x и у, значения новых х и у
def AddLineInFile(number, newX, newY):
    if (newX.is_integer()):
        newX = int(newX)
    if (newY.is_integer()):
        newY = int(newY)
    number.append(int(len(number)+1))
    addLine = open('TextInfo.txt', 'a')
    addLine.write(str(number[len(number)-1]) + '. ' + str(newX) + ' ' + str(newY) + '\n')
    addLine.close()

#Функция удаления строки из файла, принимает списки с номерами строк, значениями x и у, номером строки, которую нужно удалить
def DeleteLineInFile(number, x, y, removeNumber):
    number.pop(len(number)-1)
    x.pop(removeNumber-1)
    y.pop(removeNumber-1)
    removeLine = open('TextInfo.txt', 'w')
    for i in range(len(number)):
        removeLine.write(str(number[i]) + '. ' + str(x[i]) + ' ' + str(y[i]) + '\n')
    removeLine.close()

#Функция подсчёта среднего арифметического значений, принимает список значений и возвращает среднее арифметическое этого списка
def AverageArifmetic(list):
    sum = 0
    for i in range(len(list)):
        sum += list[i]
    return sum/len(list)

#Функция подсчёта среднеквадратического отклонения значений, принимает список значений и возвращает его среднеквадратическое отклонение
def StandardDeviation(list):
    sum = 0
    for i in range(len(list)):
        sum += (list[i]-AverageArifmetic(list))**2
    return math.sqrt(sum/(len(list)-1))

#Функция подсчёта коэффициента парной корреляции, принимает значения двух списков и возвращает их коэффициент парной корреляции
def PairCorrelationCoefficient(x, y):
    sum = 0
    for i in range(len(x)):
        sum += (x[i]-AverageArifmetic(x))*(y[i]-AverageArifmetic(y))
    StandardDeviation_x = StandardDeviation(x)
    StandardDeviation_y = StandardDeviation(y)
    return sum/((len(x)-1)*StandardDeviation_x*StandardDeviation_y)

#Функция для подсчёта теоритических значений у, принимает значения из списка х, возвращает список с теоритическими значениями у1
def Function1(x):
    yTheory1 = []
    for i in range(len(x)):
        yTheory1.append(x[i]**2/math.exp(1/x[i]))
    return yTheory1

#Функция для подсчёта теоритических значений у, принимает значения из списка х, возвращает список с теоритическими значениями у2
def Function2(x):
    yTheory2 = []
    for i in range(len(x)):
        yTheory2.append(math.sqrt(x[i])*(math.log(x[i]))**2)
    return yTheory2

#Функция для подсчёта коэффициентов регрессий, принимает списки со значениями x и y, возвращает коэффициенты a0, a1 для обоих регрессий
def Coefficients(x, y):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0
    sum6 = 0
    sum7 = 0
    yTheory1 = Function1(x)
    yTheory2 = Function2(x)
    for i in range(len(x)):
        sum1 += y[i]
        sum2 += yTheory1[i]
        sum3 += yTheory2[i]
        sum4 += yTheory1[i]**2
        sum5 += yTheory2[i]**2
        sum6 += y[i]*yTheory1[i]
        sum7 += y[i]*yTheory2[i]
    a0_1 = (sum1*sum4 - sum2*sum6)/(len(x)*sum4-sum2**2) #a0 1-й регрессии
    a0_2 = (sum1*sum5 - sum3*sum7)/(len(y)*sum5-sum3**2) #a0 2-й регрессии
    a1_1 = (len(x)*sum6 - sum1*sum2)/(len(x)*sum4-sum2**2) #a1 1-й регрессии
    a1_2 = (len(x)*sum7 - sum1*sum3)/(len(y)*sum5-sum3**2) #a1 2-й регрессии
    return a0_1, a0_2, a1_1, a1_2

#Функция вычисления значений 1-й и 2-й регрессии, принимает списки со значениями x и y, возвращает списки со значениями 1-й и 2-й регрессии
def Regressions(x, y):
    regression1 = []
    regression2 = []
    a0_1, a0_2, a1_1, a1_2 = Coefficients(x, y)
    yTheory1 = Function1(x)
    yTheory2 = Function2(x)
    for i in range(len(x)):
        regression1.append(a0_1 + a1_1 * yTheory1[i])
        regression2.append(a0_2 + a1_2 * yTheory2[i])
    return regression1, regression2

#Функция подсчёта остаточных дисперсий, принимает списки со значениями x, у и регрессий, возвращает остаточные дисперсии 1-й и 2-й функции
def ResidualDispersion(x, y, regression1, regression2):
    sum1 = 0
    sum2 = 0
    for i in range(len(x)):
        sum1 += (y[i] - regression1[i])**2
        sum2 += (y[i] - regression2[i])**2
    return (1/(len(x)-1))*sum1, (1/(len(x)-1))*sum2

#Функция подсчёта коэффициентов Фишера, принимает списки со значениями x, у и регрессий, возвращает коэффициенты Фишера 1-й и 2-й функции
def CoefficientsOfTheFisher(x, y, regression1, regression2):
    ResidualDispersion1, ResidualDispersion2 = ResidualDispersion(x, y, regression1, regression2)
    StandartDeviationn = StandardDeviation(y)
    return StandartDeviationn**2/ResidualDispersion1, StandartDeviationn**2/ResidualDispersion2

#Функция сортировки списка x по возрастанию, при этом пары (x, y), (x, regression1), (x, regression2) не изменяется
def SortLists(x, y, regression1, regression2):
    for i in range(len(x)-1):
        for j in range(len(x)-i-1):
            if x[j] > x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                y[j], y[j+1] = y[j+1], y[j]
                regression1[j], regression1[j+1] = regression1[j+1], regression1[j]
                regression2[j], regression2[j+1] = regression2[j+1], regression2[j]
    return x, y, regression1, regression2
