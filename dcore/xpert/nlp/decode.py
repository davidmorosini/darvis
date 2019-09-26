#Modulo de decodificação de comandos
import sys
import logging

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

from darvis_databases.database_utils import get_train_commands

class Decode:

    def __init__(self):
        self.bot_ = ChatBot('darvis')
        
        commands = get_train_commands()

        self.bot = ListTrainer(self.bot_)  
        self.bot.train(commands)
        logging.info('Bot decoder sucess trained.')

    def decode_msg(self, message):
        resposta = self.bot_.get_response(message)
        txt = 'Ainda não sei responder isso..'
        if(float(resposta.confidence) > 0.5):
            txt = resposta
        
        return txt


if __name__ == '__main__':
    d = Decode()

