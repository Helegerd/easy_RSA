# Coding:utf-8
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
import sys

def isSimple(n):
    '''простое ли число n'''
    i = 2
    while i ** 2 <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def areTogSimple(m, n):
    '''являются ли эти числа взаимно простыми'''
    i = 2
    while i ** 2 <= n or i ** 2 <= m:
        if n % i == m % i == 0:
            return False
        i += 1
    return True

class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.linedis = 10  # в пикселях длина меж строк
        
        # начальный экран с вводом
        # лабел p=
        self.pislab = QLabel(self)
        self.pislab.resize(50, 20)
        self.pislab.move(10, 10)
        self.pislab.setText('p = ')
        # ввод p
        self.pisedit = QLineEdit(self)
        self.pisedit.resize(200, 20)
        self.pisedit.move(self.pislab.x() + self.pislab.width() + 10, self.pislab.y())
        # лабел q=
        self.qislab = QLabel(self)
        self.qislab.resize(50, 20)
        self.qislab.move(self.pisedit.x() + self.pisedit.width() + 10, self.pisedit.y())
        self.qislab.setText('q = ')
        # ввод q
        self.qisedit = QLineEdit(self)
        self.qisedit.resize(200, 20)
        self.qisedit.move(self.qislab.x() + self.qislab.width() + 10, self.qislab.y())
        # кнопка для запуска процесса
        self.nextbtn = QPushButton(self)
        self.nextbtn.resize(100, 50)
        self.nextbtn.move(690, 740)
        self.nextbtn.setText('ДАЛЕЕ')
        self.nextbtn.clicked.connect(self.changeToNext)
        # лабел для ошибок
        self.errlab = QLabel(self)
        self.errlab.resize(680, 50)
        self.errlab.move(10, 740)
        # эдит с сообщением
        self.messageedit = QLineEdit(self)
        self.messageedit.resize(780, 20)
        self.messageedit.move(10, self.errlab.y() - 30)
        # лабел "сообщение:"
        self.messagelab = QLabel(self)
        self.messagelab.resize(self.messageedit.width(), self.messageedit.height())
        self.messagelab.move(10, self.messageedit.y() - 30)
        self.messagelab.setText('СООБЩЕНИЕ:')
        
        # окно с шифровкой и дешифровкой
        # кнопка возврата к выбору
        self.backbtn = QPushButton(self)
        self.backbtn.resize(100, 50)
        self.backbtn.move(690, 740)
        self.backbtn.setText('НАЗАД')
        self.backbtn.clicked.connect(self.changeToBack)
        self.backbtn.hide()
        # лабелы для отображения, о них чуть позже
        self.showlist = []
        for i in range(13):
            self.showlist.append(QLabel(self))
            self.showlist[-1].resize(780, 20)
            self.showlist[-1].move(10, i * (self.showlist[-1].height() + self.linedis))
            self.showlist[-1].hide()
        self.showlist[0].setText('<p style="color: rgb(10, 155, 10);">I Подготовка ключей</p>')
        self.showlist[8].setText('<p style="color: rgb(10, 155, 10);">II Шифрование</p>')
        self.showlist[11].setText('<p style="color: rgb(10, 155, 10);">III Расшифровка</p>')
        
    def changeToNext(self):
        '''меняет окно ввода на окно иллюстрации'''
        try:
            self.p = int(self.pisedit.text())
            self.q = int(self.qisedit.text())
            self.message = self.messageedit.text()
            if not(isSimple(self.p) and isSimple(self.q)) or self.p <= 2 or self.q <= 2:
                raise SyntaxError  # не спрашивайте
            self.errlab.setText("")
            for wid in [self.pislab, self.pisedit, self.qislab, self.qisedit, self.nextbtn,
                        self.errlab, self.messageedit, self.messagelab]: # прячем виджеты
                wid.hide()
            for wid in [self.backbtn] + self.showlist:  # показываем виджеты вывода
                wid.show()
            self.showlist[1].setText('взяты простые числа p = {} и q = {}'.format(self.p, self.q))
            self.n = self.p * self.q  # модуль
            self.showlist[2].setText(f'модуль n = p * q = {self.n}')
            self.fi = (self.p - 1) * (self.q - 1)  # функция эйлера
            self.showlist[3].setText(f'функция эйлера ф = (p - 1) * (q - 1) = {self.fi}')
            self.e = 0  # открытая экспонента
            for i in range(2, self.fi):
                if areTogSimple(i, self.fi):
                    self.e = i
            self.showlist[4].setText(f'открытая экспонента e = {self.e}; e < ф и они взаимнопростые')
            self.showlist[5].setText('{' + str(self.e) + ',' + str(self.n) + '} -- открытый ключ')
            self.d = 0  # скрытая экспонента
            i = self.fi * 2
            while True:
                if (i * self.e) % self.fi == 1:
                    self.d = i
                    break
                i += 1
            self.showlist[6].setText(f'скрытая экспонента d = {self.d}; (d * e) % ф = ({self.d} * {self.e}) % {self.fi} = 1')
            self.showlist[7].setText('{' + str(self.d) + ',' + str(self.n) + '} -- секретный ключ')
            self.P = []
            for sym in self.message:
                self.P.append(ord(sym))
            self.showlist[9].setText('ваше сообщение преобразовано в числовой формат P: ' + str(self.P))
            self.E = [i ** self.e % self.n for i in self.P]
            self.showlist[10].setText('кодировка сообщения в Е = P ^ e % n: ' + str(self.E))
            self.showlist[12].setText('расшифровка через E ^ d % n: ' + str([i ** self.d % self.n for i in self.E]))
        except:
            self.errlab.setText("ПОВТОРИТЕ ВВОД")

    def changeToBack(self):
        '''возвращает окно ввода'''
        for wid in [self.pislab, self.pisedit, self.qislab, self.qisedit, self.nextbtn,
                    self.errlab, self.messageedit, self.messagelab]:
            wid.show()
        for wid in [self.backbtn] + self.showlist:
            wid.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MW()
    mw.show()
    sys.exit(app.exec_())