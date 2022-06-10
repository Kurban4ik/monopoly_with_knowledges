#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtWidgets


# Класс регистрации

class Reg(QDialog):
    def __init__(self):
        super(Reg, self).__init__()
        loadUi('register.ui', self)
        self.pushButton.clicked.connect(self.register)
        self.conection = sqlite3.connect('login.db')
        self.cur = self.conection.cursor()
        self.a = ''

    # Единственная функция регистрации
    def register(self):
        is_right = True
        for i in self.lineEdit.text():

            # Проверка корректности ввода имени
            if i in '0123456789.+-/=*':
                s = QMessageBox(QtWidgets.QMessageBox.Information,
                                "Ошибка",
                                "Вы не ввели имя или пароль!",
                                QtWidgets.QMessageBox.Ok,
                                self)
                s.show()
                is_right = False
                break
            pass
        # Ввод верный
        if is_right:
            if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_3.text != '':
                # Добавление нового пользователя, при заполненных полях
                self.cur.execute(f'''INSERT INTO USERS VALUES ("{self.lineEdit.text()}", 0, "{self.lineEdit_2.text()}",
                 0, "{self.lineEdit_3.text()}", 0, 0, 0, 0, 0, 0, 0, 0)''')

                self.name = self.lineEdit.text()

                self.coins = 0

                self.conection.commit()
                self.conection.close()
                self.close()
            else:
                s = QMessageBox(QtWidgets.QMessageBox.Information, "Ошибка", "Вы не ввели имя или пароль!",
                                QtWidgets.QMessageBox.Ok, self)
                s.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Reg()
    w.show()
    sys.exit(app.exec_())
