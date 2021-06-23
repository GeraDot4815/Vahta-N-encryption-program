import random, pyAesCrypt, os, hashlib

def Generate():
    chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    password=''
    Len=random.randint(8, 13)
    for i in range(Len):
        password+=random.choice(chars)

    return password

def Protect(password):
    try:
        # задаем размер буфера
        buffer_size = 512 * 1024
        # вызываем метод шифрования
        pyAesCrypt.encryptFile(str("Ram\DRSG.txt"), str("Ram\DRSG.txt") + ".crp", password, buffer_size)
        # удаляем исходный файл
        os.remove("Ram\DRSG.txt")

        key = hashlib.md5(password.encode('utf-8'))
        f = open('Ram\mstein.txt', 'w')
        f.close()
        f = open('Ram\mstein.txt', 'a')
        f.write(str(key.hexdigest()))
        f.close()
    except ValueError:
        print("!"*10+"Пароль уже установлен"+"!"*10)
        c=input()

def Dialog():
    print("*"*50+"\nВведите 'W', чтобы самостоятельно ввести пароль.\nВведите 'G', чтобы сгенерировать пароль автоматически.\n"+"*"*50)
    answer=input("Введите ответ: ")
    while answer!="W" and answer!="G":
        print("Ответ был введен не верно.")
        answer = input("Введите ответ: ")

    if answer=="W":
        password = input("Введите свой пароль: ")
        while len(password)<8:
            print("!!!Длина пароля должна быть не менее 8 символов!!!")
            password = input("Введите свой пароль: ")
        Protect(password)
        print("=" * 50 + "\nВаш пароль: " + password + "\nЗапомните этот пароль, теперь вы будете вводить его каждый раз при запуске основного приложения.\n" + "=" * 50)
        c=input()
    elif answer=="G":
        password = Generate()
        Protect(password)
        print("="*50+"\nВаш пароль был сгенерирован автоматически.\nВаш пароль: " + password + "\nЗапомните этот пароль, теперь вы будете вводить его каждый раз при запуске основного приложения.\n" + "=" * 50)
        c=input()

Dialog()