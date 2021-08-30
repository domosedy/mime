from PIL import Image
from flask import Flask, request
import requests
import telebot
from datetime import *
import os


token = '1975301368:AAG8FTrB3nbavr2MPnqTo0DNLbyLfjFc04o'


letters = 'абвг'
diff = 938 - 272
stroki = [272, 1004, 1736, 2468, 3200, 4006, 4812]

stolb = [0, 816, 1575, 2334, 3093]

bot = telebot.TeleBot(token)


app = Flask(__name__)
bot.set_webhook(url="https://tralalalalal.herokuapp.com/")

@app.route('/')
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"
    
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
    
    photo = open('rasp.png', 'rb')
    bot.send_message(chatid, 'Привет, я помогу тебе узнать расписание в АМТЭКе', reply_markup=keyboard)

a = []
for i in range(5, 12):
    for let in letters:
        a.append(str(i) + let)
        
        
@bot.message_handler(content_types=["text"])
def send_mine(message):
    try:
        download_image()
    except:
        bot.send_message(message.chat.id, 'Прости, но на этот день расписания нет(((')
        return
    chatid = message.chat.id
    text = message.text.lower()
    if text == 'для всех':
        fil = open('rasp.png', 'rb')
        bot.send_photo(chatid, fil)
        return
    
    if text not in a:
        bot.send_message(chatid, 'Я тебя не понимаю')
        return
    fil = open(text + '.png', 'rb')
    bot.send_photo(chatid, fil)

def download_image():
    url = 'https://амтэк35.рф/wp-content/uploads/shedule/2021-2022/'
    dae = datetime(2021, 9, 1)
    date = datetime.now()
    if(date.weekday() == 6):
        dat = timedelta(days = 1)
        date += dat
    date = max(date, dae)
    url += date.strftime("%d.%m.20%y.png")
    #print(url)
    
    res = requests.get(url)
    with open("rasp.png", "wb") as f:
        f.write(res.content)
    im = Image.open('rasp.png')
    for i in range(len(stroki)):
        for let in range(1, 5):
            ij = im.crop((stolb[let - 1], stroki[i], stolb[let], stroki[i] + diff))
            ij.save(str(i + 5) + letters[let - 1] + '.png')


#bot.polling()
if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
