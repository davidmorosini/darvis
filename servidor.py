import json
import telebot
from decodificador import decode_msg


#Importando o token de configuração com o telegram
arquivo = open("token.json").read()
content = json.loads(arquivo)
token = content['token']


bot = telebot.TeleBot(token)


#Recebe qualquer mensagem
@bot.message_handler(func=lambda m: not((len(m.text.split('/')) > 1)))
def msg(message):
    resp = decode_msg(message, bot)
    bot.send_message(message.chat.id, resp)


@bot.message_handler(commands=['teste'])
def echo_all(message):
	bot.reply_to(message, 'comando...')


bot.polling()
