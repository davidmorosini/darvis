import json
import telebot
from decodificador import Decode
import logging

if __name__ == '__main__':
    log_path = 'Logs/log.log'
    print('Iniciando Servidor...')
    print('Configurando arquivo de Log...')
    logging.basicConfig( filename = log_path, filemode = 'a', \
                             level = logging.DEBUG,\
                             format = '%(levelname)s: %(message)s -- %(asctime)s ', \
                             datefmt = '%d/%m/%Y %I:%M:%S %p' )
    logging.debug('Arquivo de Log Inicializado')
    print('Importando o token de sincronizacao com o telegram...')
    try:
        arquivo = open("token.json").read()
        content = json.loads(arquivo)
        token = content['token']
        bot = telebot.TeleBot(token)

        d = Decode()

        d.start_model_decode()
        
        print('Definindo Listener de entrada...')
        #Listener para receber mensagens, incialmente toda mensagen sera tratada pelo decodificador,
        #As unicas excecoes sao as mensagens com comando, ex: /command, estas terao um destino especial
        #pois podem ser uteis.
        #Para tratar os comandos:  (commands=['comando'])
        @bot.message_handler(func = lambda m: not((len(m.text.split('/')) > 1)))
        def decodifica(message):
            d.decode_msg(message, bot)

        @bot.message_handler(commands=['treinar'])
        def train(message):
            d.TrainMode = not(d.TrainMode)
            msg_reply = "Ok, desativei o modo de treino"
            msg_log = message.chat.username + " desativou o modo de treino."
            if(d.TrainMode):
                msg_reply = "Beleza " + message.chat.first_name + ", Modo de Treino ativo"
                msg_log = message.chat.username + " ativou o modo de treino."
            bot.reply_to(message, u"{}".format(msg_reply))
            logging.debug(msg_log)
            #print(message.chat.username)
            #print(message.chat.first_name)
            #print(message.chat.id)
            
        print('Bot sincronizado com servidor do Telegram. Iniciando Poolling.')
        logging.debug('Bot sincronizado, inciando Polling.')
    
        bot.polling()

    except FileNotFoundError:
        print('\t# Arquivo com token não encontrado, abortando servidor.')
        logging.debug('# ERRO: Arquivo com token não encontrado, abortando servidor.')
    except IOError:
        print('\t# ERRO: I/O Erro, abortando servidor.')
        logging.debug('# ERRO: I/O Erro, abortando servidor.')
    except:
        print('\t# Erro desconhecido, abortando servidor')
        logging.debug('# # Erro desconhecido, abortando servidor')












    


    
