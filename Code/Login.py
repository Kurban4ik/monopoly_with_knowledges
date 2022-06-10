# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
import sqlite3
from Registration import Reg
from PyQt5 import QtWidgets


class Example(QDialog):
    def __init__(self):
        super(Example, self).__init__()
        loadUi('Login.ui', self)
        self.pushButton.clicked.connect(self.login)
        self.conection = sqlite3.connect('login.db')
        self.cur = self.conection.cursor()
        self.pushButton_2.clicked.connect(self.register)
        self.name = ''

    # Переход в окно Registration.py
    def register(self):
        dialog = Reg()
        dialog.exec_()
        try:
            if dialog.name != '' and dialog.password != '':
                self.name = dialog.name
                self.coins = 0
                self.close()
        except:
            pass

    # Вход
    def login(self):
        sqlquery = 'SELECT * FROM USERS'
        for i in self.cur.execute(sqlquery).fetchall():
            if self.lineEdit.text() == str(i[2]) and self.lineEdit_2.text() == str(i[0]):
                self.name = i[0]
                self.coins = i[1]
                self.conection.close()
                self.close()

        s = QMessageBox(QtWidgets.QMessageBox.Information,
                        "Ошибка",
                        "Вы ввели некорректное имя или пароль!",
                        QtWidgets.QMessageBox.Ok,
                        self)
        s.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
