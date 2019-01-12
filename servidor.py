import json
from utilidades import number_on_string
from utilidades import search_string
from recomenda import show_movies
from recomenda import search_titles


#Importando o token de configuração com o telegram
arquivo = open("token.json").read()
content = json.loads(arquivo)
token = content['token']

import telebot

bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda txt: (len(txt.text.upper().split('LISTAR')) > 1))
def show_listar(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Um segundo, deixe me ver os que tenho aqui...")

    text_ = ""
    
    #Listar Filmes
    qtd_filmes = number_on_string(message.text)
    if(qtd_filmes == -1):
        #colocar a quantidade default
        qtd_filmes = 10
        text_ += "Listando uma quantidade default de filmes: \n\n"
    else:
        text_ += "Listando os " + str(qtd_filmes) + " como você pediu: \n\n"

    filmes = show_movies(qtd=qtd_filmes)

    for i in range(0, qtd_filmes):
        text_ += filmes[i] + '\n'

    text_ += '\n\nrecomendar [nome do filme] <para recomendações..>'
    
    bot.reply_to(message, u"{}".format(text_))

@bot.message_handler(func=lambda txt: (len(txt.text.upper().split('RECOMENDAR')) > 1))
def show_listar(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Deixe me pensar...")

    title = message.text.split('recomendar ')[1]
    text = search_titles(title)

    bot.reply_to(message, u"Aqui estão, espero que goste:\n\n{}".format(text))
    
#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)


bot.polling()
