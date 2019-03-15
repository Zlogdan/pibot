import serial
import telebot
import time


token = '449042193:AAG_rxZQdbcTot2NmL1rZJSUtcdHReoIgYs'
bot = telebot.TeleBot(token)

# change ACM number as found from ls /dev/tty/ACM*
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600


def sendToArduino(data="on"):
    print(repr(data))
    # data = "on"
    bdata = str.encode(data)
    ser.write(bdata)


@bot.message_handler(commands=['led'])
def set_led_color(message):
    msg_args = message.text.split(' ')  # /led 1 1 0
    bot.send_message(message.chat.id, 'Начинаю...')
    data = msg_args[0]
    sendToArduino(data+"\n")
    # r = int(msg_args[1])
    # g = int(msg_args[2])
    # b = int(msg_args[3])
    time.sleep(1)
    data = msg_args[1]
    sendToArduino(data+"\n")
    bot.send_message(message.chat.id, 'Готово')


@bot.message_handler(commands=['rgb'])
def set_rgb_color(message):
    msg_args = message.text.split(' ')  # /led 1 1 0

    bot.send_message(message.chat.id, 'Начинаю...')
    #data = msg_args[0]
    #sendToArduino(data+"\n")
    r = msg_args[1]+" "
    sendToArduino(r)
    g = msg_args[2]+" "
    sendToArduino(g)
    b = msg_args[3]+"\n"
    sendToArduino(b)

    bot.send_message(message.chat.id, 'Готово')


bot.polling()


'''
while(True):
    data = input()
    bdata = str.encode(data) + b'\n'
    # print(bdata)
    ser.write(bdata)

    read_ser = ser.readline()
    print(read_ser.decode())
'''
