import json
import telebot
import logging

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

from xpert.nlp.decode import Decode

class TelegramServer:
    def __init__(self, configs):
        self.configs = configs
    
    def run(self):
        try:
            with open(self.configs['telegram']['token']) as arq:
                token = json.loads(arq.read())['key']

            bot = telebot.TeleBot(token)

            dec = Decode()
            
            #Listener para receber mensagens, incialmente toda mensagen sera tratada pelo decodificador,
            #As unicas excecoes sao as mensagens com comando, ex: /command, estas terao um destino especial
            #pois podem ser uteis.
            #Para tratar os comandos:  (commands=['comando'])
            @bot.message_handler(func = lambda m: not((len(m.text.split('/')) > 1)))
            def decodifica_msg(message):
                resp = dec.decode_msg(message.text)
                bot.send_message(message.chat.id, resp)

            @bot.message_handler(func = lambda m: ((len(m.text.split('/')) > 1)))
            def decodifica_handler(message):
                #d.decode_handler(message, bot)
                bot.send_message(message.chat.id, 'Teste Frase')
                
            logging.info('Bot sincronizado, inciando Polling.')
        
            bot.polling()

        except FileNotFoundError as filenerr:
            logging.info(filenerr)
        except IOError as ioerr:
            logging.info(ioerr)
        except Exception as err:
            logging.info(err)














    


    
