import numpy as np
import pandas as pd

def recomenda(title):
    colunas = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv('datasets/u.data', sep='\t', names=colunas)
    titulos = pd.read_csv('datasets/Movie_Id_Titles')

    df = pd.merge(df, titulos, on='item_id')

    ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
    ratings['count'] = pd.DataFrame(df.groupby('title')['rating'].count())

    df_pivot = df.pivot_table(index='user_id', columns='title', values='rating')

    user_ratings = df_pivot[title]

    recommend = df_pivot.corrwith(user_ratings)

    correlation = pd.DataFrame(recommend, columns=['correlation'])
    correlation.dropna(inplace=True)

    correlation = correlation.join(ratings['count'])

    num_counts = 100
    testee = correlation[correlation['count'] > num_counts].sort_values('correlation', ascending=False).head(10)

    testee = testee.reset_index()

    text = ""
    for i in range(1, 10):
        text += testee['title'][i] + "\n"

    return text


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
    bot.reply_to(message, u"{}\n{}\n{}\n{}".format("/teste", "/horas", "/show", "/filmes"))

@bot.message_handler(commands=['filmes'])
def show_filmes(message):
    string = "Star Wars (1977)  /1\nContact (1997)  /2\nFargo (1996)  /3\nReturn of the Jedi (1983)  /4\nLiar Liar (1997)  /5\nEnglish Patient, The (1996)  /6\nScream (1996)  /7\nToy Story (1995)  /8\nAir Force One (1997)  /9\nIndependence Day (ID4) (1996)  /10"
    bot.reply_to(message, string)


@bot.message_handler(commands=['1'])
def show_filmes(message):
    filme = recomenda('Star Wars (1977)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['2'])
def show_filmes(message):
    filme = recomenda('Contact (1997)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['3'])
def show_filmes(message):
    filme = recomenda('Fargo (1996)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['4'])
def show_filmes(message):
    filme = recomenda('Return of the Jedi (1983)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['5'])
def show_filmes(message):
    filme = recomenda('Liar Liar (1997)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['6'])
def show_filmes(message):
    filme = recomenda('English Patient, The (1996)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['7'])
def show_filmes(message):
    filme = recomenda('Scream (1996)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['8'])
def show_filmes(message):
    filme = recomenda('Toy Story (1995)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['9'])
def show_filmes(message):
    filme = recomenda('Air Force One (1997)')
    bot.reply_to(message, u"{}".format(filme))

@bot.message_handler(commands=['10'])
def show_filmes(message):
    filme = recomenda('Independence Day (ID4) (1996)')
    bot.reply_to(message, u"{}".format(filme))

bot.polling()


    
    






