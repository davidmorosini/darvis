import logging

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

class Decode:

    def __init__(self):
        self.bot = ChatBot('TW Chat Bot')
        
        conversa = ['Oi', 'Olá', 'Tudo bem?', 'Tudo ótimo', 
            'Você gosta de programar?', 'Sim, eu programo em Python']

        self.bot.set_trainer(ListTrainer)
        self.bot.train(conversa)
        logging.info('Bot decoder sucess trained.')

    def decode_msg(self, message):
        resposta = self.bot.get_response(message)
        txt = 'Ainda não sei responder isso..'
        if(float(resposta.confidence) > 0.5):
            txt = resposta
        return txt