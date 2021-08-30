from main import download_image, a, letters, remove_prev_images
import telebot
from datetime import datetime, timedelta
import schedule
token = '1989338152:AAHwIteDVwL0L_Fx9xoZfb5_hkn_9WRfaXQ'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        download_image()
    except:
        pass
    chatid = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("5А", "5Б", "5В", "5Г")
    keyboard.row("6А", "6Б", "6В", "6Г")
    keyboard.row("7А", "7Б", "7В", "7Г")
    keyboard.row("8А", "8Б", "8В", " ")
    keyboard.row("9А", "9Б", "9В", " ")
    keyboard.row("10А", "10Б", "10В", "10Г")
    keyboard.row("11А", "11Б", "11В", "11Г")
    keyboard.row("Для всех")
    
    bot.send_message(chatid, 'Привет, я помогу тебе узнать расписание в АМТЭКе', reply_markup=keyboard)

        
@bot.message_handler(content_types=["text"])
def send_mine(message):
    try:
        download_image()
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, 'Прости, но на этот день расписания нет(((')
        return
    chatid = message.chat.id
    text = message.text.lower()
    if text == 'для всех':
        fil = open('rasp.png', 'rb')
        bot.send_photo(chatid, fil)
        fil.close()
        return
    
    if text not in a:
        bot.send_message(chatid, 'Я тебя не понимаю')
        return
    x = datetime.now()
    fil = open(text + str(x.day) + '.png', 'rb')
    bot.send_photo(chatid, fil)
    fil.close()
    

schedule.every().day.at("16:30").do(remove_prev_images)
download_image()
bot.polling()
