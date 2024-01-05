from config import token
import telebot
import sqlite3

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['largest_area'])
def largest_area(message):
    n = telebot.util.extract_arguments(message.text)
    try: n = int(n)
    except: n = 1

    conn = sqlite3.connect('world_information.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT country, area FROM countries ORDER BY area DESC")
        
        res = cursor.fetchmany(n)
        res = "\n".join([f"{x[0]} - {x[1]} кв.км." for x in res])
        bot.send_message(message.chat.id, res)

@bot.message_handler(commands=['smallest_area'])
def smallest_area(message):
    n = telebot.util.extract_arguments(message.text)
    try: n = int(n)
    except: n = 1

    conn = sqlite3.connect('world_information.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT country, area FROM countries ORDER BY area")
        
        res = cursor.fetchmany(n)
        res = "\n".join([f"{x[0]} - {x[1]} кв.км." for x in res])
        bot.send_message(message.chat.id, res)




@bot.message_handler(func=lambda message: True)
def text_handler(message):
    country = message.text
    print(country)
    conn = sqlite3.connect('world_information.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("Запрос SQL для получения всех данных из таблицы, где страна - это то, что ввел пользователь ", (country,) )
        res = cursor# результат запроса
        if res:
            bot.send_message(message.chat.id, f'{res[1]} \nПлощадь страны: {res[3]} кв.км. \nПлотность населения на 1 кв.км.: {res[2]} чел.\nЧисленность населения: {res[4]} чел. \nПроцент от всего населения Земли: {res[5]} %')
        else:
            bot.send_message(message.chat.id, "Я не знаю такую страну")

bot.infinity_polling()
