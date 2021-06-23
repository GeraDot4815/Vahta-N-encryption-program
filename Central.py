import os, pyAesCrypt
from PyQt5.QtWidgets import QMessageBox
from GUI import Ui_MainWindow
class Messages(Ui_MainWindow):
    def small_Messages(self, TITLE, TEXT,  ICON):
        msg=QMessageBox()
        msg.setWindowTitle(TITLE)
        msg.setText(TEXT)
        if ICON=="Crit":
            msg.setIcon(QMessageBox.Critical)
        elif ICON=="Quest":
            msg.setIcon(QMessageBox.Question)
        elif ICON=="Inf":
            msg.setIcon(QMessageBox.Information)
        elif ICON=="Warn":
            msg.setIcon(QMessageBox.Warning)

        x=msg.exec_()

MSG=Messages()
class Cryptography(Messages):

    # Записывает двумерный массив в текстовый файл
    def ListInTXT(self, List, Password):
        buffer_size = 512 * 1024
        pyAesCrypt.decryptFile(str("Ram\DRSG.txt.crp"), str(os.path.splitext("Ram\DRSG.txt.crp")[0]), Password, buffer_size)
        os.remove("Ram\DRSG.txt.crp")

        f = open('Ram\DRSG.txt', 'w')
        for i in List:
            for j in i:
                f.write(j)
                f.write('\n')
        f.write('=')
        f.close()

        pyAesCrypt.encryptFile(str("Ram\DRSG.txt"), str("Ram\DRSG.txt") + ".crp", Password, buffer_size)
        os.remove("Ram\DRSG.txt")



    # Формирует из txt двумерный массив с двумя элементами во вложенном
    def txtInList(self, Password):
        buffer_size = 512 * 1024
        pyAesCrypt.decryptFile(str("Ram\DRSG.txt.crp"), str(os.path.splitext("Ram\DRSG.txt.crp")[0]), Password, buffer_size)
        os.remove("Ram\DRSG.txt.crp")

        f = open('Ram\DRSG.txt', 'r')
        List = []
        c = 0
        file = []
        for line in f:
            element = line[:-1]
            if c < 2:
                file.append(element)
                c += 1
            else:
                List.append(file)
                c = 1
                file = [line[:-1]]
        f.close()

        pyAesCrypt.encryptFile(str("Ram\DRSG.txt"), str("Ram\DRSG.txt") + ".crp", Password, buffer_size)
        os.remove("Ram\DRSG.txt")

        return (List)



    # Функция шифрования файла
    def encryption(self, file, password, Informate):
        # задаем размер буфера
        buffer_size = 512 * 1024
        # вызываем метод шифрования
        pyAesCrypt.encryptFile(str(file), str(file) + ".crp", password, buffer_size)
        # чтобы видеть результат выводим на печать имя зашифрованного файла
        if Informate=="Yes":
            MSG.small_Messages("Успех!", "Файл '" + str(os.path.splitext(file)[0]) + "' зашифрован!", "Inf")
        # удаляем исходный файл
        os.remove(file)



    # функция дешифровки файла
    def decryption(self, File, Password, Informate):
        try:
            # задаём размер буфера
            buffer_size = 512 * 1024
            f=File+".crp"
            # вызываем метод расшифровки
            pyAesCrypt.decryptFile(str(f), str(os.path.splitext(f)[0]), Password, buffer_size)
            # удаляем исходный файл
            os.remove(f)
        except ValueError:
            if Informate=="Yes":
                MSG.small_Messages("Внимание!", "Файл '" + str(os.path.splitext(File)[0]) + "' не был зашифрован!", "Warn")