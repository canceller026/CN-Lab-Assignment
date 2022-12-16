# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import sys
import os
import PyQt5.QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QTimer  # (, Qt)
from PyQt5.uic import loadUi
import random
from client import Client


class MainWindow(QMainWindow):
    homepage_status = False
    username = ""
    message_index = 0
    acc_friend = 0
    friend_index = 1
    fake_listpeer = []
    friend_namelist = []
    fake_connected = []
    friend_checklist = []

    serverport = random.randint(10000, 12000)
    port = serverport
    peername = "Client"
    start = False

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Chat App")
        print("load_ui")
        self.open_loginpage()
        print("show")

        self.show()
        self.login_button.hide()
        self.register_button.hide()
#        if self.homepage_status:
#            self.home_button_control()
#        else:
#            self.login_button_control()

        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.read_message)
        self.timer.timeout.connect(self.login_success)
        self.timer.start()

    def open_menubar(self):
        print('Do something in open_menubar')

# LOGIN #######################################################

    def open_loginpage(self):
        loadUi("Login.ui", self)
        self.login_button_control()
        self.username_text.setPlainText("")
        self.homepage_status = False
        self.port_text.setPlainText(str(self.serverport))

    def login_button_control(self):
        self.start_button.clicked.connect(lambda: self.start_control())
        self.register_button.clicked.connect(lambda: self.register_control())
        self.login_button.clicked.connect(lambda: self.user_name_control())
        self.exit_btn.clicked.connect(lambda: sys.exit())
        print("login_button_ctrl")

    def start_control(self):
        porttext = str(self.port_text.toPlainText())
        self.serverport = int(porttext)
        self.port = self.serverport
        self.my_client = Client(peername=self.username, serverport=self.serverport)
        print("Port= ", self.serverport)
        self.port_text.setPlainText("")
        self.my_client.run()
        self.login_button.show()
        self.register_button.show()
        self.username = self.username_text.toPlainText()
        self.username_text.setPlainText("")
        if self.username != "":
            self.my_client.name = self.username
            self.my_client.load_peerlist = []

    def register_control(self):
        self.my_client.send_register()

    def user_name_control(self):
        self.my_client.send_login()
        self.start = True

    def login_success(self):
        if self.homepage_status is False:
            if self.start:
                if self.my_client.logincheck:
                    self.my_client.logincheck = False
                    self.open_homepage()


# HOME #######################################################

    def open_homepage(self):
        loadUi("HomePage.ui", self)
        self.lable_username.setText(self.username)
        self.acc_friend = 0
        self.friend_checklist = []
        self.reset_chat()
        self.send_button.hide()
        self.fake_listpeer = self.my_client.load_peerlist
        if self.my_client.load_peerlist.__contains__(self.username):
            self.fake_listpeer.remove(self.username)
        self.my_client.load_peerlist = []
        print("See this: ", self.my_client.load_peerlist)
        self.yes_button.hide()
        self.no_button.hide()
        self.request_button.hide()
        self.home_button_control()
        self.homepage_status = True
        self.message_plainTextEdit.setPlainText("")
        self.search_plainTextEdit.setPlainText("")
        self.file_plainTextEdit.setPlainText("")
        self.real_fresh()
        self.friend_list_update()

    def home_button_control(self):
        print("button_ctrl")
        self.logout_button.clicked.connect(lambda: self.open_loginpage())
        self.search_button.clicked.connect(lambda: self.search_user())
        self.exit_btn.clicked.connect(lambda: sys.exit())
        self.change_friend()
        self.send_button.clicked.connect(lambda: self.send_message())
        self.yes_button.clicked.connect(lambda: self.send_yes())
        self.no_button.clicked.connect(lambda: self.send_no())
        self.request_button.clicked.connect(lambda: self.send_request())
        self.refresh_button.clicked.connect(lambda: self.real_fresh())
        self.group_button.clicked.connect(lambda: self.open_grouppage())


    def search_user(self):
        searchname = self.search_plainTextEdit.toPlainText()
        print("Search for user: ", searchname)
        if searchname != self.user_button_1.text():
            self.Item_1.hide()
        if searchname != self.user_button_2.text():
            self.Item_2.hide()
        if searchname != self.user_button_3.text():
            self.Item_3.hide()
        if searchname != self.user_button_4.text():
            self.Item_4.hide()
        if searchname != self.user_button_5.text():
            self.Item_5.hide()
        if searchname != self.user_button_6.text():
            self.Item_6.hide()
        if searchname != self.user_button_7.text():
            self.Item_7.hide()
        if searchname == "":
            print(self.acc_friend)
            if self.acc_friend > 0:
                self.Item_1.show()
            if self.acc_friend > 1:
                self.Item_2.show()
            if self.acc_friend > 2:
                self.Item_3.show()
            if self.acc_friend > 3:
                self.Item_4.show()
            if self.acc_friend > 4:
                self.Item_5.show()
            if self.acc_friend > 5:
                self.Item_6.show()
            if self.acc_friend > 6:
                self.Item_7.show()

    def friend_list_update(self):
        self.Item_1.hide()
        self.Item_2.hide()
        self.Item_3.hide()
        self.Item_4.hide()
        self.Item_5.hide()
        self.Item_6.hide()
        self.Item_7.hide()
        self.user_button_1.setStyleSheet('color: white')
        self.user_button_2.setStyleSheet('color: white')
        self.user_button_3.setStyleSheet('color: white')
        self.user_button_4.setStyleSheet('color: white')
        self.user_button_5.setStyleSheet('color: white')
        self.user_button_6.setStyleSheet('color: white')
        self.user_button_7.setStyleSheet('color: white')
        self.acc_friend = 0
        for friend in self.fake_listpeer:
            self.acc_friend = self.acc_friend + 1
            self.friend_checklist.append(False)
        if self.acc_friend > 0:
            self.user_button_1.setText(self.fake_listpeer[0])
            self.Item_1.show()
            if self.friend_namelist.__contains__(self.user_button_1.text()):
                self.user_button_1.setStyleSheet('color: green')
        if self.acc_friend > 1:
            self.user_button_2.setText(self.fake_listpeer[1])
            self.Item_2.show()
            if self.friend_namelist.__contains__(self.user_button_2.text()):
                self.user_button_2.setStyleSheet('color: green')
        if self.acc_friend > 2:
            self.user_button_3.setText(self.fake_listpeer[2])
            self.Item_3.show()
            if self.friend_namelist.__contains__(self.user_button_3.text()):
                self.user_button_3.setStyleSheet('color: green')
        if self.acc_friend > 3:
            self.user_button_4.setText(self.fake_listpeer[3])
            self.Item_4.show()
            if self.friend_namelist.__contains__(self.user_button_4.text()):
                self.user_button_4.setStyleSheet('color: green')
        if self.acc_friend > 4:
            self.user_button_5.setText(self.fake_listpeer[4])
            self.Item_5.show()
            if self.friend_namelist.__contains__(self.user_button_5.text()):
                self.user_button_5.setStyleSheet('color: green')
        if self.acc_friend > 5:
            self.user_button_6.setText(self.fake_listpeer[5])
            self.Item_6.show()
            if self.friend_namelist.__contains__(self.user_button_6.text()):
                self.user_button_6.setStyleSheet('color: green')
        if self.acc_friend > 6:
            self.user_button_7.setText(self.fake_listpeer[6])
            self.Item_7.show()
            if self.friend_namelist.__contains__(self.user_button_7.text()):
                self.user_button_7.setStyleSheet('color: green')

    def index_control(self, id):
        if self.message_index == 7:
            self.reset_chat()
        self.message_index = self.message_index + 1

# COMP ########################################

    def send_request(self):
        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.yes_button.show()
        self.no_button.show()

    def send_yes(self):
        print("Yes")
        self.yes_button.hide()
        self.no_button.hide()
        if self.friend_checklist[self.friend_index-1]:
            self.send_button.show()
            print("Chat Request!")
            self.request_button.hide()
        else:
            self.friend_checklist[self.friend_index-1] = True
            self.request_button.show()
        self.my_client.accept_request()
        self.my_client.agree = True

    def send_no(self):
        print("No")
        self.yes_button.hide()
        self.no_button.hide()
        self.my_client.refuse_request()
        self.my_client.agree = False

    def send_message(self):
        m_message = self.message_plainTextEdit.toPlainText()
        if m_message != "":
            self.index_control("m")
            if self.message_index == 1:
                self.my_text_1.setText(m_message)
                self.my_message_1.show()
            if self.message_index == 2:
                self.my_text_2.setText(m_message)
                self.my_message_2.show()
            if self.message_index == 3:
                self.my_text_3.setText(m_message)
                self.my_message_3.show()
            if self.message_index == 4:
                self.my_text_4.setText(m_message)
                self.my_message_4.show()
            if self.message_index == 5:
                self.my_text_5.setText(m_message)
                self.my_message_5.show()
            if self.message_index == 6:
                self.my_text_6.setText(m_message)
                self.my_message_6.show()
            if self.message_index == 7:
                self.my_text_7.setText(m_message)
                self.my_message_7.show()
            self.message_plainTextEdit.setPlainText("")
        file_address = self.file_plainTextEdit.toPlainText()
        print("Send")
        if file_address != "":
            self.my_client.send_file(self.fake_listpeer[self.friend_index-1], file_address)
            self.file_plainTextEdit.setPlainText("")
        self.my_client.send_chat_message(self.fake_listpeer[self.friend_index-1], m_message)

    def read_message(self):
        if self.homepage_status:
            if self.my_client.new_message_check:
                self.my_client.new_message_check = False
                self.receive_message(self.my_client.new_message)
                self.my_client.new_message = ""
                print("Got it")

    def receive_message(self, f_message):
        if f_message != "":
            self.index_control("f")
            if self.message_index == 1:
                self.f_text_1.setText(f_message)
                self.friend_message_1.show()
            if self.message_index == 2:
                self.f_text_2.setText(f_message)
                self.friend_message_2.show()
            if self.message_index == 3:
                self.f_text_3.setText(f_message)
                self.friend_message_3.show()
            if self.message_index == 4:
                self.f_text_4.setText(f_message)
                self.friend_message_4.show()
            if self.message_index == 5:
                self.f_text_5.setText(f_message)
                self.friend_message_5.show()
            if self.message_index == 6:
                self.f_text_6.setText(f_message)
                self.friend_message_6.show()
            if self.message_index == 7:
                self.f_text_7.setText(f_message)
                self.friend_message_7.show()
        print("Receive")

# CHANGE #######################################################

    def change_friend(self):
        self.user_button_1.clicked.connect(lambda: self.change_1())
        self.user_button_2.clicked.connect(lambda: self.change_2())
        self.user_button_3.clicked.connect(lambda: self.change_3())
        self.user_button_4.clicked.connect(lambda: self.change_4())
        self.user_button_5.clicked.connect(lambda: self.change_5())
        self.user_button_6.clicked.connect(lambda: self.change_6())
        self.user_button_7.clicked.connect(lambda: self.change_7())

    def change_1(self):
        self.friend_index = 1
        print("--> ", self.fake_listpeer[self.friend_index-1])
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_1.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()
        else:
            self.yes_button.hide()
            self.no_button.hide()

    def change_2(self):
        self.friend_index = 2
        print("--> ", self.fake_listpeer[self.friend_index-1])
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_2.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()

    def change_3(self):
        self.friend_index = 3
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_3.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()

    def change_4(self):
        self.friend_index = 4
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_4.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()

    def change_5(self):
        self.friend_index = 5
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_5.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()

    def change_6(self):
        self.friend_index = 6
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_6.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()

    def change_7(self):
        self.friend_index = 7
        self.my_client.send_addfriend(self.fake_listpeer[self.friend_index-1])
#        self.my_client.send_chat_request(self.fake_listpeer[self.friend_index-1])
        self.lable_name.setText(self.user_button_7.text())
        self.reset_chat()
        if self.friend_checklist[self.friend_index-1] == False:
            self.yes_button.show()
            self.no_button.show()

    def real_fresh(self):
        self.refresh_chat()
#        self.refresh_chat()

    def refresh_chat(self):
        self.my_client.send_listpeer()
        if self.my_client.load_peerlist.__contains__(self.username):
            self.my_client.load_peerlist.remove(self.username)
        self.fake_listpeer = self.my_client.load_peerlist
        self.my_client.load_peerlist = []
        self.friend_namelist = self.my_client.friendlist
        if self.friend_namelist.__contains__(self.username):
            self.friend_namelist.remove(self.username)
        self.friend_list_update()

    def group_chat(self):
        self.my_client.send_listpeer()
        if self.my_client.load_peerlist.__contains__(self.username):
            self.my_client.load_peerlist.remove(self.username)
        self.fake_listpeer = self.my_client.load_peerlist
        self.my_client.load_peerlist = []
        self.friend_namelist = self.my_client.friendlist
        if self.friend_namelist.__contains__(self.username):
            self.friend_namelist.remove(self.username)
        self.friend_list_update()

    def reset_chat(self):
        print("Reset")
        self.friend_message_1.hide()
        self.friend_message_2.hide()
        self.friend_message_3.hide()
        self.friend_message_4.hide()
        self.friend_message_5.hide()
        self.friend_message_6.hide()
        self.friend_message_7.hide()
        self.my_message_1.hide()
        self.my_message_2.hide()
        self.my_message_3.hide()
        self.my_message_4.hide()
        self.my_message_5.hide()
        self.my_message_6.hide()
        self.my_message_7.hide()
        self.message_index = 0

# GROUP #######################################################

    def open_grouppage(self):
        loadUi("GroupPage.ui", self)
        self.lable_username.setText(self.username)
        self.acc_friend = 0
        self.friend_checklist = []
        self.reset_chat()
        self.send_button.hide()
        self.fake_listpeer = self.my_client.load_peerlist
        if self.my_client.load_peerlist.__contains__(self.username):
            self.fake_listpeer.remove(self.username)
        self.my_client.load_peerlist = []
        print("See this: ", self.my_client.load_peerlist)
        self.yes_button.hide()
        self.no_button.hide()
        self.request_button.hide()
        self.group_button_control()
        self.homepage_status = True
        self.message_plainTextEdit.setPlainText("")
        self.search_plainTextEdit.setPlainText("")
        self.file_plainTextEdit.setPlainText("")
        self.real_fresh()
        self.friend_list_update()

    def group_button_control(self):
        print("button_ctrl")
        self.logout_button.clicked.connect(lambda: self.open_loginpage())
        self.search_button.clicked.connect(lambda: self.search_user())
        self.exit_btn.clicked.connect(lambda: sys.exit())
        self.change_friend()
        self.send_button.clicked.connect(lambda: self.send_message())
        self.yes_button.clicked.connect(lambda: self.send_yes())
        self.no_button.clicked.connect(lambda: self.send_no())
        self.request_button.clicked.connect(lambda: self.send_request())
        self.refresh_button.clicked.connect(lambda: self.real_fresh())
        self.back_button.clicked.connect(lambda: self.open_homepage())


class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        sys.exit(self.app.exec_())


def run_gui():
    gui = GUI()


if __name__ == "__main__":
    run_gui()
