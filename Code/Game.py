import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi, loadUiType
from PyQt5 import QtGui
from sqlite3 import connect
import matplotlib.pyplot as plt
import sys

from rate import Rate
import Tasks
from Login import Example


class Game(QMainWindow):
    def __init__(self):
        self.background_black = '''QPushButton{border-radius: 15px;\n 
          background: rgb(20,25,120);\n 
          box-shadow: 0 3px rgb(33,147,90) inset;}'''
        dialog = Example()
        self.conn = connect('login.db')
        self.cur = self.conn.cursor()

        dialog.exec_()

        self.palyer_name = dialog.name
        flag = True
        try:
            self.coins = dialog.coins
        except AttributeError:
            flag = False
        if flag:
            super(Game, self).__init__()
            loadUi('name.ui', self)
        else:
            sys.exit(0)
        self.setWindowTitle('Монополия с умом')
        self.stat_btn.clicked.connect(self.statistic)
        # Активный
        self.enable = ("QPushButton:hover {background: rgb(53, 167, 110)}\n"
                       "QPushButton{\n"
                       "  color: white;\n"
                       "  text-decoration: none;\n"
                       "  border-radius: 15px;\n"
                       "  background: rgb(64,199,129);\n"
                       "  box-shadow: 0 -3px rgb(53,167,110) inset;\n"
                       "  transition: 0.2s;\n"
                       "}\n"
                       "QPushButton:pressed {\n"
                       "  background: rgb(33,147,90);\n"
                       "  box-shadow: 0 3px rgb(33,147,90) inset;\n"
                       "}\n"
                       "")
        self.disable = ("QPushButton{border-radius: 15px;\n"
                        "background-color: black; color:black}\n"
                        "QPushButton:hover {-webkit-transform: translate(8px,0);\n"
                        " -moz-transform: translate(8px,0);\n"
                        " -o-transform: translate(8px,0);\n"
                        " color: #1FA2E1;}\n"
                        "QPushButton:pressed { background-color: yellow; }\n"
                        "QPushButton:disabled{ color: white }")
        self.grey = ("QPushButton{border-radius: 15px;\n"
                     "background-color: grey}\n"
                     "QPushButton:hover {-webkit-transform: translate(8px,0);\n"
                     " -moz-transform: translate(8px,0);\n"
                     " -o-transform: translate(8px,0);\n"
                     " color: #1FA2E1;}\n"
                     "QPushButton:pressed { background-color: yellow; }\n"
                     "QPushButton:disabled{ color: white }")
        self.step = int(self.cur.execute(f'''SELECT STOP_POS FROM USERS WHERE 
        USERNAME = "{self.palyer_name}"''').fetchall()[0][0])
        self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
        self.buttonGroup.buttons()[0].setEnabled(False)
        self.out_btn.clicked.connect(self.save_out)
        self.throwing.clicked.connect(self.dice_throw)
        self.name_lb_2.setText(str(self.coins))
        self.name_lb.setText(str(self.palyer_name))
        self.rate_table.clicked.connect(self.rating)

        for i in list(self.buttonGroup.buttons()[0:10]):
            i.clicked.connect(self.get_math_task)
        for i in list(self.buttonGroup.buttons()[10:20]):
            i.clicked.connect(self.get_rus_task)
        for i in list(self.buttonGroup.buttons()[20:30]):
            i.clicked.connect(self.get_phys_task)
        for i in list(self.buttonGroup.buttons()[30:39]) + [self.buttonGroup.buttons()[39]]:
            i.clicked.connect(self.get_inf_task)

        for i in list(self.buttonGroup.buttons()[:self.step]):
            i.setEnabled(False)
            i.setStyleSheet(self.disable)

        self.end_btn.clicked.connect(self.game_over)
        self.black.clicked.connect(self.blackf)

    def whitef(self):
        loadUi('name.ui', self)
        self.background_black = '''QPushButton{border-radius: 15px;\n 
                  background: rgb(20,25,120);\n 
                  box-shadow: 0 3px rgb(33,147,90) inset;}'''
        self.conn = connect('login.db')
        self.cur = self.conn.cursor()
        self.setWindowTitle('Монополия с умом')
        self.stat_btn.clicked.connect(self.statistic)
        # Активный
        self.enable = ("QPushButton:hover {background: rgb(53, 167, 110)}\n"
                       "QPushButton{\n"
                       "  color: white;\n"
                       "  text-decoration: none;\n"
                       "  border-radius: 15px;\n"
                       "  background: rgb(64,199,129);\n"
                       "  box-shadow: 0 -3px rgb(53,167,110) inset;\n"
                       "  transition: 0.2s;\n"
                       "}\n"
                       "QPushButton:pressed {\n"
                       "  background: rgb(33,147,90);\n"
                       "  box-shadow: 0 3px rgb(33,147,90) inset;\n"
                       "}\n"
                       "")
        self.disable = ("QPushButton{border-radius: 15px;\n"
                        "background-color: black; color:black}\n"
                        "QPushButton:hover {-webkit-transform: translate(8px,0);\n"
                        " -moz-transform: translate(8px,0);\n"
                        " -o-transform: translate(8px,0);\n"
                        " color: #1FA2E1;}\n"
                        "QPushButton:pressed { background-color: yellow; }\n"
                        "QPushButton:disabled{ color: white }")
        self.grey = ("QPushButton{border-radius: 15px;\n"
                     "background-color: grey}\n"
                     "QPushButton:hover {-webkit-transform: translate(8px,0);\n"
                     " -moz-transform: translate(8px,0);\n"
                     " -o-transform: translate(8px,0);\n"
                     " color: #1FA2E1;}\n"
                     "QPushButton:pressed { background-color: yellow; }\n"
                     "QPushButton:disabled{ color: white }")
        self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
        self.buttonGroup.buttons()[0].setEnabled(False)
        self.out_btn.clicked.connect(self.save_out)
        self.throwing.clicked.connect(self.dice_throw)
        self.name_lb_2.setText(str(self.coins))
        self.name_lb.setText(str(self.palyer_name))
        self.rate_table.clicked.connect(self.rating)
        self.black.clicked.connect(self.blackf)
        for i in list(self.buttonGroup.buttons()[0:10]):
            i.clicked.connect(self.get_math_task)
        for i in list(self.buttonGroup.buttons()[10:20]):
            i.clicked.connect(self.get_rus_task)
        for i in list(self.buttonGroup.buttons()[20:30]):
            i.clicked.connect(self.get_phys_task)
        for i in list(self.buttonGroup.buttons()[30:39]) + [self.buttonGroup.buttons()[39]]:
            i.clicked.connect(self.get_inf_task)

        for i in list(self.buttonGroup.buttons()[:self.step]):
            i.setEnabled(False)
            i.setStyleSheet(self.disable)

        self.end_btn.clicked.connect(self.game_over)
        self.black.clicked.connect(self.blackf)

    # ретрансляция всего в темном формате
    def blackf(self):
        loadUi('black_game.ui', self)
        self.background_black = '''QPushButton{border-radius: 15px;\n 
                  background: rgb(20,25,120);\n 
                  box-shadow: 0 3px rgb(33,147,90) inset;}'''
        self.conn = connect('login.db')
        self.cur = self.conn.cursor()
        self.setWindowTitle('Монополия с умом')
        self.stat_btn.clicked.connect(self.statistic)
        # Активный
        self.enable = ('''QPushButton:hover {background: rgb(40,50,180);}\nQPushButton{\n  color: white;\n 
         text-decoration: none;\n  border-radius: 15px;\n  background:#3c51fa;\n
          box-shadow: 0 -3px rgb(53,167,110) inset;\n  
          transition: 0.2s;\n}\nQPushButton:pressed {\n 
           background: rgb(20,25,120);\n  box-shadow: 0 3px rgb(33,147,90) inset;\n}\n''')
        self.disable = ('''QPushButton{border-radius: 15px;\n 
         background: rgb(20,25,120);\n  box-shadow: 0 3px rgb(33,147,90) inset;}\n''')
        self.grey = ("QPushButton{border-radius: 15px;\n"
                     "background-color: grey}\n"
                     "QPushButton:hover {-webkit-transform: translate(8px,0);\n"
                     " -moz-transform: translate(8px,0);\n"
                     " -o-transform: translate(8px,0);\n"
                     " color: #1FA2E1;}\n"
                     "QPushButton:pressed { background-color: yellow; }\n"
                     "QPushButton:disabled{ color: white }")
        self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
        self.buttonGroup.buttons()[0].setEnabled(False)
        self.out_btn.clicked.connect(self.save_out)
        self.throwing.clicked.connect(self.dice_throw)
        self.name_lb_2.setText(str(self.coins))
        self.name_lb.setText(str(self.palyer_name))
        self.rate_table.clicked.connect(self.rating)

        for i in list(self.buttonGroup.buttons()[0:10]):
            i.clicked.connect(self.get_math_task)
        for i in list(self.buttonGroup.buttons()[10:20]):
            i.clicked.connect(self.get_rus_task)
        for i in list(self.buttonGroup.buttons()[20:30]):
            i.clicked.connect(self.get_phys_task)
        for i in list(self.buttonGroup.buttons()[30:39]) + [self.buttonGroup.buttons()[39]]:
            i.clicked.connect(self.get_inf_task)

        for i in list(self.buttonGroup.buttons()[:self.step]):
            i.setEnabled(False)
            i.setStyleSheet(self.disable)

        self.end_btn.clicked.connect(self.game_over)
        self.white.clicked.connect(self.whitef)

    def rating(self):
        s = Rate()
        s.exec_()

    def save_out(self):
        self.cur.execute(f'''UPDATE USERS SET STOP_POS = {self.step} WHERE USERNAME = "{self.palyer_name}"''')
        self.conn.commit()
        self.close()

    def restart(self):
        for i in self.buttonGroup.buttons():
            i.setEnabled(False)
            i.setStyleSheet(self.grey)
        self.throwing.setEnabled(True)
        self.end_btn.setEnabled(False)
        self.end_btn.setStyleSheet(self.grey)
        self.step = 0

    def game_over(self):
        msgbox = QMessageBox()
        msgbox.setText('Вы завершили круг!')
        restartbtn = msgbox.addButton('Играть заново', QMessageBox.ActionRole)
        changebtn = msgbox.addButton('Пожалуй, хватит', QMessageBox.ActionRole)
        msgbox.exec_()
        if msgbox.clickedButton() == restartbtn:
            self.restart()
            self.coins += 5
            self.name_lb_2.setText(str(self.coins))
            self.cur.execute(F"""UPDATE USERS SET COINS = {self.coins} WHERE USERNAME = "{self.palyer_name}"
                            """)
            self.conn.commit()
        elif msgbox.clickedButton() == changebtn:
            self.coins += 5
            self.cur.execute(F"""UPDATE USERS SET COINS = {self.coins} WHERE USERNAME = "{self.palyer_name}"
                            """)
            self.conn.commit()
            self.close()

    # Вывод статистики
    def statistic(self):
        plot_info = self.cur.execute(F'''SELECT WRONG_MATH, RIGHT_MATH, WRONG_RUS, RIGHT_RUS,
         WRONG_PHYS, RIGHT_PHYS, WRONG_INF, RIGHT_INF FROM USERS WHERE USERNAME = "{self.palyer_name}"''').fetchall()[0]
        labels = 'Неправильные ответы математики', 'Правильные ответы математики',  \
                 'Неправильные ответы русского языка', 'Правильные ответы русского языка', \
                 'Неправильные ответы физики', 'Правильные ответы физики', 'Неправильные ответы информатики', \
                 'Правильные ответы информатики',
        y = plot_info if sum(plot_info) != 0 else [1 for _ in range(8)]
        plt.pie(y, labels=labels)
        plt.show()

    def get_math_task(self):
        target = random.randint(0, len(Tasks.math) - 1)
        text, result = QtWidgets.QInputDialog.getText(None, "Задание",
                                                      f"<html style='font-size:12p"
                                                      f"t; font-family: Comic Sans MS;'>{Tasks.math[target]}",
                                                      QtWidgets.QLineEdit.Normal)
        if result:
            # Ответ верный
            if text.upper() == Tasks.math_ans[target]:
                msg = QMessageBox()
                msg.font()
                msg.setWindowTitle("Ответ")
                msg.setText("Правильно!   \nПлюс один шаг вперед")
                msg.setIcon(QMessageBox.Information)
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.exec_()
                self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                self.step += 1
                if self.step < 40:
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                self.throwing.setEnabled(True)

                self.coins += 1
                self.name_lb_2.setText(str(self.coins))
                self.cur.execute(
                    f'''UPDATE USERS SET RIGHT_MATH = RIGHT_MATH + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.cur.execute(F"""UPDATE USERS SET COINS = {self.coins} WHERE USERNAME = "{self.palyer_name}"
                """)

                self.conn.commit()
            else:
                # Ответ неверный
                msg = QMessageBox()
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setWindowTitle("Ответ")
                msg.setText("Неправильно :(  \nВы отправляетесь на шаг назад")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.cur.execute(f'''UPDATE USERS SET WRONG_MATH = WRONG_MATH + 1 WHERE
                 USERNAME = "{self.palyer_name}"''')
                self.conn.commit()
                if self.step != 1:
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.grey)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.step -= 1
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.throwing.setEnabled(True)
                else:
                    self.buttonGroup.buttons()[0].setEnabled(False)
                    self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
                    self.throwing.setEnabled(True)

    def dice_throw(self):
        # Тут мы присваиваем шаг к общему колчиеству шагов, отключаем возмодность броска,
        # проходимся по доступным точкам и подрубаем их
        self.cur.execute(f'UPDATE USERS SET STOP_POS = {self.step} WHERE USERNAME = "{self.palyer_name}"')
        self.conn.commit()
        self.throwing.setEnabled(False)
        self.gotten = random.randint(1, 5)
        self.step += self.gotten
        self.dice_place.setText(str(self.gotten))
        if self.step <= 40:
            for i in range(self.step):
                self.buttonGroup.buttons()[i].setStyleSheet(self.disable)
                self.buttonGroup.buttons()[i].setEnabled(False)
            self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.enable)
            self.buttonGroup.buttons()[self.step - 1].setEnabled(True)

        else:
            for i in self.buttonGroup.buttons():
                i.setEnabled(False)
                i.setStyleSheet(self.disable)
            self.end_btn.setStyleSheet(self.enable)
            self.end_btn.setEnabled(True)

    def get_rus_task(self):
        target = random.randint(0, len(Tasks.rus) - 1)
        text, result = QtWidgets.QInputDialog.getText(None, "Задание",
                                                      f"<html style='font-size:12pt; "
                                                      f"font-family: Comic Sans MS;'>{Tasks.rus[target]}",
                                                      QtWidgets.QLineEdit.Normal)
        if result:
            # Ответ верный
            if text.upper() == Tasks.rus_ans[target]:
                msg = QMessageBox()
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setWindowTitle("Ответ")
                msg.setText("Правильно!   \nПлюс один шаг вперед")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                self.step += 1
                if self.step < 40:
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.buttonGroup.buttons()[self.step - 1]. setStyleSheet(self.disable)
                self.throwing.setEnabled(True)

                self.coins += 1
                self.name_lb_2.setText(str(self.coins))
                self.cur.execute(F"""UPDATE USERS SET COINS = {self.coins} WHERE USERNAME = "{self.palyer_name}"
                """)
                self.cur.execute(
                    f'''UPDATE USERS SET RIGHT_RUS = RIGHT_RUS + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.conn.commit()

            else:
                # Ответ неверный
                msg = QMessageBox()
                msg.setWindowTitle("Ответ")
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setText("Неправильно :(  \nВы отправляетесь на шаг назад")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.cur.execute(
                    f'''UPDATE USERS SET WRONG_RUS = WRONG_RUS + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.conn.commit()
                if self.step != 1:
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.grey)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.step -= 1
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.throwing.setEnabled(True)
                else:
                    self.buttonGroup.buttons()[0].setEnabled(False)
                    self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
                    self.throwing.setEnabled(True)

    def get_inf_task(self):
        target = random.randint(0, len(Tasks.inf) - 1)
        text, result = QtWidgets.QInputDialog.getText(None,
                                                      "Задание",
                                                      f"<html style='font-size:12pt; "
                                                      f"font-family: Comic Sans MS;'>{Tasks.inf[target]}",
                                                      QtWidgets.QLineEdit.Normal)
        if result:
            # Ответ верный
            if text.upper() == Tasks.inf_ans[target]:
                msg = QMessageBox()
                msg.setWindowTitle("Ответ")
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setText("Правильно!   \nПлюс один шаг вперед")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                self.step += 1
                if self.step < 40:
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.buttonGroup.buttons()[self.step - 1]. setStyleSheet(self.disable)
                self.throwing.setEnabled(True)

                self.coins += 1
                self.name_lb_2.setText(str(self.coins))
                self.cur.execute(F"""UPDATE USERS SET COINS = {self.coins} WHERE USERNAME = "{self.palyer_name}"
                """)
                self.cur.execute(
                    f'''UPDATE USERS SET RIGHT_INF = RIGHT_INF + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.conn.commit()
            else:
                # Ответ неверный
                msg = QMessageBox()
                msg.setWindowTitle("Ответ")
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setText("Неправильно :(  \nВы отправляетесь на шаг назад")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.cur.execute(
                    f'''UPDATE USERS SET WRONG_INF = WRONG_INF + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.conn.commit()

                if self.step != 1:
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.grey)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.step -= 1
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.throwing.setEnabled(True)
                else:
                    self.buttonGroup.buttons()[0].setEnabled(False)
                    self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
                    self.throwing.setEnabled(True)

    def get_phys_task(self):
        target = random.randint(0, len(Tasks.physics) - 1)
        text, result = QtWidgets.QInputDialog.getText(None,
                                                      "Задание",
                                                      f"<html style='font-size:12pt;"
                                                      f" font-family: Comic Sans MS;'>{Tasks.physics[target]}",
                                                      QtWidgets.QLineEdit.Normal)
        if result:
            # Ответ верный
            if text.upper() == Tasks.physics_ans[target]:
                msg = QMessageBox()
                msg.setWindowTitle("Ответ")
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setText("Правильно!   \nПлюс один шаг вперед")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                self.step += 1
                if self.step < 40:
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.buttonGroup.buttons()[self.step - 1]. setStyleSheet(self.disable)
                self.throwing.setEnabled(True)

                self.coins += 1
                self.name_lb_2.setText(str(self.coins))
                self.cur.execute(F"""UPDATE USERS SET COINS = {self.coins} WHERE USERNAME = "{self.palyer_name}"
                """)
                self.cur.execute(
                    f'''UPDATE USERS SET RIGHT_PHYS = RIGHT_PHYS + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.conn.commit()

            else:
                # Ответ неверный
                msg = QMessageBox()
                font = QtGui.QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                msg.setFont(font)
                msg.setWindowTitle("Ответ")
                msg.setText("Неправильно :(  \nВы отправляетесь на шаг назад")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                if self.step != 1:
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.grey)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.step -= 1
                    self.buttonGroup.buttons()[self.step - 1].setStyleSheet(self.disable)
                    self.buttonGroup.buttons()[self.step - 1].setEnabled(False)
                    self.throwing.setEnabled(True)
                else:
                    self.buttonGroup.buttons()[0].setEnabled(False)
                    self.buttonGroup.buttons()[0].setStyleSheet(self.grey)
                    self.throwing.setEnabled(True)

                self.cur.execute(
                    f'''UPDATE USERS SET WRONG_PHYS = WRONG_PHYS + 1 WHERE USERNAME = "{self.palyer_name}"''')
                self.conn.commit()


def start():
    app = QApplication(sys.argv)
    w = Game()
    w.show()
    sys.exit(app.exec_())


start()
