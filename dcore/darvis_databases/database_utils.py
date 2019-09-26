
import os
import logging
import json

def get_train_commands():
    arq = os.path.join('.', 'dcore/darvis_databases/chatbot/chatbot.json')

    com = []
    try:
        with open(arq) as arq_:
            js = json.loads(arq_.read())
            com = js['commands']['train']
    except Exception as err:
        logging.error('An error occured in try open (chatbot.json), return []. More details: {}'.format(err))
    
    return com