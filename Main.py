from PyQt5.QtCore import pyqtRemoveInputHook
from PyQt5.QtWidgets import QListWidgetItem, QFileDialog
from  Central import Cryptography, Messages
from GUI import Ui_MainWindow, QtWidgets
from EnterPassword import Ui_EnterPasswordWin
import getpass, os, sys, hashlib, webbrowser, pyAesCrypt, datetime
USER_NAME = getpass.getuser()


Crypt=Cryptography()
MSG=Messages()

List=[]
Password=""

# Функция для кнопки шифрования
def EncryptionBtt():
    global List
#LIST=[[x, y]...], где x-путь, y-пароль
    LIST=Crypt.txtInList(Password)
    path = ui.EncryptDirLineedit.text()
    password = ui.PasswordlineEdit.text()

    if password == "":
        MSG.small_Messages("Недостаточно данных.","Укажите пароль!","Warn")
    else:
        try:
            Crypt.encryption(path, password, "Yes")
            element=[path, password]
            LIST.append(element)
            Crypt.ListInTXT(LIST, Password)
            ui.listWidget.clear()
            List=CreateListOfFiles()
            ui.EncryptDirLineedit.setText("")
            ui.PasswordlineEdit.setText("")
        except FileNotFoundError:
            MSG.small_Messages("Ошибка в указанных данных.", "Не удается перейти по указанному пути","Warn")

#Кнопка добавления зашифрованного файла
def AddBttDef():
    global List
#LIST=[[x, y]...], где x-путь, y-пароль
    LIST=Crypt.txtInList(Password)
    path = ui.OpenDirLineEdit.text()
    password = ui.PasswordlineEdit_2.text()
    path=path[:-4]
    print(path)

    if password == "":
        MSG.small_Messages("Недостаточно данных.","Укажите пароль!","Warn")
    else:
        try:
            element=[path, password]
            LIST.append(element)
            Crypt.ListInTXT(LIST, Password)
            ui.listWidget.clear()
            List=CreateListOfFiles()
            ui.OpenDirLineEdit.setText("")
            ui.PasswordlineEdit_2.setText("")
        except FileNotFoundError:
            MSG.small_Messages("Ошибка в указанных данных.", "Не удается перейти по указанному пути","Warn")


#шифрует файл перед выходом из программы
def OUT_encryption():
    LIST = Crypt.txtInList(Password)
    newList=[]
    for i in LIST:
        newList.append(i[0])
    for i in newList:
        slesh=i.rfind("\\")
        dir_name =i[:slesh]
        file=i[slesh+1:]
        dir=os.listdir(dir_name)
        for item in dir:
            if os.path.join(item)==file and not item.endswith(".crp"):
                Crypt.encryption(i, LIST[newList.index(i)][1], "No")
    MSG.small_Messages("Успех!", "Все файлы успешно зашифрованы!", "Inf")

####
#Кусок, отвечающий за виджет списка
#Извлекает пути
def ViewDirs():
    LIST = Crypt.txtInList(Password)
    newList = []
    for i in LIST:
        newList.append(i[0])
    return newList

def OpenItem(item):
    for i in List:
        if i == item.text():
            LIST = Crypt.txtInList(Password)
            Crypt.decryption(LIST[List.index(i)][0], LIST[List.index(i)][1], "Yes")
            path = LIST[List.index(i)][0]
            path = os.path.realpath(path)
            os.startfile(path)

def DeliteItem(item):
    # Получить строку, соответствующую ему по элементу
    row = ui.listWidget.indexFromItem(item).row()  # !!!
    # дешифруем и удаляем элемент из обего списка
    LIST = Crypt.txtInList(Password)
    Crypt.decryption(LIST[row][0], LIST[row][1], "Yes")
    LIST.pop(row)
    # Удалить item
    ui.listWidget.takeItem(row)
    # удаляем элемент из хранилища
    Crypt.ListInTXT(LIST, Password)

def  CreateListOfFiles():
    List = ViewDirs()
    nlist=[]
    for text in List:
        slesh = text.rfind("\\")
        text = text[slesh + 1:]
        nlist.append(text)

        QListWidgetItem(text, ui.listWidget)
    List=nlist
    return List

###

def ChangePassword():
    global Password
    if ui.OldPasswordLineedit.text()=="" or ui.NewPasswordLineedit.text()=="":
        MSG.small_Messages("Недостаточно данных!","Заполните все поля!","Warn")
    elif len(ui.NewPasswordLineedit.text())<8:
        MSG.small_Messages("Ненадежный пароль!", "Длина пароля должна быть не менее 8 символов!", "Warn")
    else:
        key = hashlib.md5(ui.OldPasswordLineedit.text().encode('utf-8'))
        f = open('Ram\mstein.txt', 'r')
        hesh = f.read()
        f.close()
        if str(key.hexdigest()) == hesh:
            buffer_size = 512 * 1024
            pyAesCrypt.decryptFile(str("Ram\DRSG.txt.crp"), str(os.path.splitext("Ram\DRSG.txt.crp")[0]), Password, buffer_size)
            os.remove("Ram\DRSG.txt.crp")
            Password=ui.NewPasswordLineedit.text()
            pyAesCrypt.encryptFile(str("Ram\DRSG.txt"), str("Ram\DRSG.txt") + ".crp", Password, buffer_size)
            os.remove("Ram\DRSG.txt")
            key = hashlib.md5(Password.encode('utf-8'))
            f = open('Ram\mstein.txt', 'w')
            f.close()
            f = open('Ram\mstein.txt', 'a')
            f.write(str(key.hexdigest()))
            f.close()
            MSG.small_Messages("Успех!","Ваш пароль '"+ui.OldPasswordLineedit.text()+"'изменен на '"+Password+"'!","Inf")
            ui.OldPasswordLineedit.setText("")
            ui.NewPasswordLineedit.setText("")
        else:
            MSG.small_Messages("Неверный пароль!","Вы ввели неверный старый пароль! Повторите попытку.","Warn")
            ui.OldPasswordLineedit.setText("")
            ui.NewPasswordLineedit.setText("")

def getFilePath():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFile)
    filePath=dialog.getOpenFileName()
    filePath=filePath[0]
    SleshCount=filePath.count("/")
    filePath=filePath.replace("/","\\", SleshCount)
    ui.EncryptDirLineedit.setText(filePath)
def getFilePath2():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFile)
    filePath=dialog.getOpenFileName()
    filePath=filePath[0]
    SleshCount=filePath.count("/")
    filePath=filePath.replace("/","\\", SleshCount)
    ui.OpenDirLineEdit.setText(filePath)

def Donate():
    now = datetime.datetime.now()
    if now.strftime('%m-%d')=='04-01':
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        MSG.small_Messages("Внимание!!!", "Внимание! Вас затролили! Настоящая ссылка: 'https://vk.com/donate_app?mid=-194828393'", "Crit")
    else:
        webbrowser.open('https://vk.com/donate_app?mid=-194828393')


def CheckPassword():
    global List
    global Password
    if widget.lineEdit.text()=="":
        MSG.small_Messages("Недостаточно данных!","Введите пароль в строку!", "Inf")
    else:
        key = hashlib.md5(widget.lineEdit.text().encode('utf-8'))
        f=open('Ram\mstein.txt', 'r')
        hesh=f.read()
        f.close()
        if str(key.hexdigest())==hesh:
            Password=widget.lineEdit.text()
            EnterPasswordWin.close()
            MainWindow.show()
            # List widget
            # Построение списка
            List = CreateListOfFiles()
            # Открыть файл
            ui.listWidget.itemClicked.connect(OpenItem)
            # снять защиту
            ui.listWidget.itemDoubleClicked.connect(DeliteItem)
            # Кнопка зашифровки файла
            ui.EncryptDirBtt.clicked.connect(EncryptionBtt)
            # Кнопка зашифровки перед выходом
            ui.pushButton_2.clicked.connect(OUT_encryption)
            # Кнопка обзора файлов
            ui.ViewDirsBtt.clicked.connect(getFilePath)
            ui.ViewDirsBtt_2.clicked.connect(getFilePath2)
            #Кнопка дополнения списка
            ui.AddBtt.clicked.connect(AddBttDef)
            #Кнопка доната
            ui.pushButton.clicked.connect(Donate)
            #Смена пароля
            ui.ChangePasswordBtt.clicked.connect(ChangePassword)
        else:
            MSG.small_Messages("Неверный пароль!", "Вы ввели неверный пароль! Повторите попытку.", "Warn")
            widget.lineEdit.setText("")



pyqtRemoveInputHook()
app = QtWidgets.QApplication(sys.argv)

EnterPasswordWin = QtWidgets.QWidget()
widget = Ui_EnterPasswordWin()
widget.setupUi(EnterPasswordWin)
EnterPasswordWin.show()
widget.pushButton.clicked.connect(CheckPassword)
widget.lineEdit.returnPressed.connect(CheckPassword)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
sys.exit(app.exec_())