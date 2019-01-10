import json

#Importando o token de configuração com o telegram
arquivo = open("token.json").read()
content = json.loads(arquivo)

token = content['token']


import telebot
from datetime import datetime

bot = telebot.TeleBot(token)

#Implementando alguns comandos de ação..

@bot.message_handler(commands=['teste', 'ola'])
def send_welcome(message):
    bot.reply_to(message, u"Olá")

@bot.message_handler(commands=['horas'])
def send_horas(message):
    h = datetime.now()
    bot.reply_to(message, u"{}:{}:{}".format(h.hour, h.minute, h.second))

@bot.message_handler(commands=['help'])
def show_commands(message):
    bot.reply_to(message, u"{}\n{}\n{}".format("/teste", "/horas", "/show"))

bot.polling()




