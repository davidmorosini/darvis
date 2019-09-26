import json
import telebot
#from decodificador import Decode
import logging
import sys
import os

import _thread

from telegram.telegram_server import TelegramServer

sys.path.append(os.path.join('.', 'dcore/telegram'))

def main(conf):
    try:
        log_path = conf['log']['path']
        if(not(os.path.isdir(log_path))):
            os.mkdir(log_path)
        
        log_path = os.path.join(log_path, conf['log']['name'])
        logging.basicConfig(filename = log_path, filemode = conf['log']['filemode'], \
                            level = logging.INFO,\
                            format = conf['log']['format'], \
                            datefmt = conf['log']['dtformat'] )

        logging.info('darvis initializing.')

     
        tserver = TelegramServer(conf)

        #_thread.start_new_thread( print_time, ("Thread-1", 2, ) )
        _thread.start_new_thread( tserver.run, () )
        
        while(True):
            pass
    
    except Exception as err:
        logging.info(err)

    logging.info('darvis end process.')


if __name__ == '__main__':

    arquivo = open(sys.argv[1]).read()
    content = json.loads(arquivo)
    main(content)
        










    


    
