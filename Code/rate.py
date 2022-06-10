# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3


# Рейтинговая таблица
class Rate(QDialog):
    def __init__(self):
        super(Rate, self).__init__()
        loadUi('rating.ui', self)
        self.pushButton.clicked.connect(self.out)
        self.rat_tabke.setColumnCount(3)
        self.connect = sqlite3.connect('login.db')
        self.cur = self.connect.cursor()
        self.cur.execute('''SELECT * FROM USERS ORDER BY COINS DESC''')
        rows = self.cur.fetchall()

        for row in rows:
            inx = rows.index(row)
            self.rat_tabke.insertRow(inx)
            self.rat_tabke.setItem(inx, 0, QTableWidgetItem(str(row[0])))  # Получение имени
            self.rat_tabke.setItem(inx, 1, QTableWidgetItem(str(row[1])))  # Получение баллов
            self.rat_tabke.setItem(inx, 2, QTableWidgetItem(str(row[4])))  # Получение класса

    def out(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Rate()
    w.show()
    sys.exit(app.exec_())
