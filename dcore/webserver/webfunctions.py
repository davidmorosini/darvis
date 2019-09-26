import time
import json
import threading
import multiprocessing
import logging

import sys

from serverbot import start_server
from constants import CONFIGS_, BOTSERVER, TELEGRAM_TOKEN

bot_online = False


svision_response = {
    'name': 'svision-server',
    'status': 'ok',
    'system': 'svision',
    'code': 100,
    'msg':'servidor online'
}

THREADS = {
    'bot': [],
    'objetc-detection': [],
    'queue': []
}

######################## FUNCTIONS ########################
def test():
    response = svision_response
    return json.dumps(response)  

def start_bot():
    global bot_online

    response = svision_response
    response['system'] = 'bot'
    try:
        if(not(bot_online)):
            if(len(THREADS['bot']) > 0):
                response['status'] = 'error'
                response['code'] = 400
                response['msg'] = 'Thread de controle do bot ja iniciada.'
            else:           
                t_id = multiprocessing.Process(target=start_server)#, args=(args, ))
                t_id.start()
                THREADS['bot'].append(t_id)
                #t_id.join()
                response['msg'] = 'Thread de controle do bot iniciada com sucesso.'
                bot_online = not(bot_online)

        else:
            THREADS['bot'][0].terminate()
            response['msg'] = 'Thread de controle do bot encerrada com sucesso.'
            THREADS['bot'] = []
            bot_online = not(bot_online)

    except:
        raise


    return json.dumps(response)