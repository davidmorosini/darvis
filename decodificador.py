from random import randint
from utilidades import *
from recomenda import *
import logging
import json

import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB



class Decode:

    TrainMode = False
    Chats = None
    Commands = None

    ##Informações necessarias para predicao dos comandos
    modelo_comandos_ = None
    bow_transformer_ = None
    tfidf_transformer_ = None

    def __init__(self):
        #Iniciando o Log de treinamentos
        try:
            log_treinos = open('Logs/log_train.log', 'a')
            logging.debug('Arquivo de Log de Treinos lido com sucesso.')
            self.Chats = load_json('datasets/chats.json')
            logging.debug('Arquivo de Chats lido com sucesso.')
            self.Commands = load_json('datasets/commands.json')
            logging.debug('Arquivo de Comandos lido com sucesso.')
            self.start_model_decode()
        except:
            logging.debug('Problemas ao ler o arquivo de Log de Treinos, criando um novo.')
            log_treinos = open('Logs/log_train.log', 'w')
        log_treinos.close()

    def __del__(self):
        #destructor
        logging.debug('Finalizando Decodificador..')
        flush_json('datasets/chats.json', self.Chats)
    


#------------------------------------------------------------------------------------#            
    def processa_comando(self, comando):
        #Retira as pontuações
        aux = [char for char in comando if char not in string.punctuation]
        #Refaz a string
        aux = ''.join(aux)
        #Remove as stopWords
        return [word for word in aux.split() if word.lower() not in \
                stopwords.words('portuguese')]



    def start_model_decode(self): 
        logging.debug('Carregando modelo para predicoes de comando')

        #Ler o dataset de comandos
        comandos = pd.read_csv('datasets/comandos', sep='\t',\
                               names=['label', 'comando'], encoding="Latin-1")
        comandos['tamanho'] = comandos['comando'].apply(len)

        bow_transformer = CountVectorizer(analyzer=self.processa_comando).fit(\
            comandos['comando'])

        self.bow_transformer_ = bow_transformer

        comandos_bow = bow_transformer.transform(comandos['comando'])

        ##analizar itens para estatistica aqui

        #TF-IDF
        tfidf_transformer = TfidfTransformer().fit(comandos_bow)
        self.tfidf_transformer_ = tfidf_transformer
        
        comandos_tfidf = tfidf_transformer.transform(comandos_bow)

        #Naive Bayes para treinamento
        modelo_comandos = MultinomialNB().fit(comandos_tfidf, comandos['label'])
        self.modelo_comandos_ = modelo_comandos

        
    def prediz_comando(self, string):
        label = None
        if(string != None):
            bow_predict = self.bow_transformer_.transform([string])
            tfidf_predict = self.tfidf_transformer_.transform(bow_predict)
            label = self.modelo_comandos_.predict(tfidf_predict)[0]
        return label
#------------------------------------------------------------------------------------#

    def decode_msg(self, msg, bot):
        #Atualiza estado no arquivo de chats
        try:
            ch = self.Chats[msg.chat.username]
        except KeyError:
            create_chat(self.Chats, msg.chat.username, 0, msg.chat.id,\
                        msg.chat.first_name)

        user = self.Chats[msg.chat.username]

        
        if(self.TrainMode):
            retreinar = False

            if(user['last_msg']['pendings']):
                #Se o usuário atual tiver alguma pendencia..
                try:
                    label = self.Commands['not-handlers'][msg.text.lower()]
                    append_arq('datasets/comandos', msg.text.lower() + '\t' + user['last_msg']['msg'])
                    bot.send_message(msg.chat.id, 'Ja anotei no meu rascunho para nao esquecer!')
                    retreinar = True
                except KeyError:
                    bot.send_message(msg.chat.id, 'Vish.. Acho que voce errou ein.. Manda de novo por gentileza o comando correto :D') 
                
            else:
                if(msg.text.lower() == 'n' and user['new_msg']):
                    bot.send_message(msg.chat.id, 'Poxa, me desculpe, estou aprendendo ainda..'+\
                                     ' Me ajude a melhorar me indicando qual seria o comando correto:\n'+\
                                     self.Commands['not-handlers']['comandos_disponiveis'])
                    user['last_msg']['pendings'] = True
                    
                elif(msg.text.lower() == 's' and user['new_msg']):
                    bot.send_message(msg.chat.id, 'SHOW!')
                    append_arq('datasets/comandos', user['last_msg']['label'] + '\t' + user['last_msg']['msg'])
                    retreinar = True
                    
                else:
                    comando_predito = self.prediz_comando(msg.text)
                    user['last_msg']['msg'] = msg.text
                    user['last_msg']['label'] = comando_predito
                    user['last_msg']['pendings'] = False
                    user['new_msg'] = True
                    bot.send_message(msg.chat.id, \
                                     '{}, entendi que se trata do comando: {}'.format(\
                                         msg.chat.first_name, comando_predito))
                    bot.send_message(msg.chat.id, 'Entendi certo? (s/n)')

            if(retreinar):
                self.start_model_decode()
                user['last_msg']['pendings'] = False
                user['new_msg'] = False

        else:
            ##MELHORAR ISSO
            text_ = ""

            if(len(msg.text.upper().split('LISTAR')) > 1):
                bot.send_message(msg.chat.id, 'Tudo bem, vou selecionar alguns aqui..')
            
                #Listar Filmes
                qtd_filmes = number_on_string(msg.text)
                if(qtd_filmes == None):
                    #colocar a quantidade default
                    qtd_filmes = 10
                    text_ += "Listando uma quantidade default de filmes: \n\n"
                else:
                    text_ += "Listando os " + str(qtd_filmes) + " como voce pediu: \n\n"

                filmes = show_movies(qtd=qtd_filmes)

                for i in range(0, qtd_filmes):
                    text_ += filmes[i] + '\n'

                text_ += '\n\nrecomendar [nome do filme] <para recomendacoes..>'

            elif(len(msg.text.upper().split('RECOMENDAR')) > 1):
                bot.send_message(msg.chat.id, "Deixe me pensar...")

                title = msg.text.split('recomendar ')[1]
                text_ += "Aqui estao, espero que goste:\n\n"
                text_ += search_titles(title)
            else:
                fail_msg = ['Nao entendi..', 'Rapaz, nao vou poder ajudar', 'Acho que nao entendi o que quer', 'Nao sei fazer isso']
                text_ += fail_msg[randint(0, len(fail_msg) - 1)]

            bot.send_message(msg.chat.id, text_)

        #Atualizando os valores do chat no banco de dados global
        self.Chats[msg.chat.username] = user
        flush_json('datasets/chats.json', self.Chats)

    def decode_handler(self, handler, bot):
        #Atualiza estado no arquivo de chats
        try:
            ch = self.Chats[handler.chat.username]
        except KeyError:
            create_chat(self.Chats, handler.chat.username, 0, handler.chat.id,\
                        handler.chat.first_name)

        try:
            label = self.Commands['handlers'][handler.text]
            text_ = ""
            if(handler.text == "/help"):
                text_ += handler.chat.first_name + ", os comandos que tenho disponiveis:\n\n"
                text_ += "/help -> Mostra alguns informacoes default\n"
                text_ += "/train -> Ativa e Desativa o Modo de Treino\n"
                text_ += "/statistics -> Informa algumas estatisticas do Bot"
                
            elif(handler.text == "/train"):
                self.TrainMode = not(self.TrainMode)
                text_ = "Ok, desativei o modo de treino"
                msg_log = handler.chat.username + " desativou o modo de treino."
                if(self.TrainMode):
                    text_ = "Beleza " + handler.chat.first_name + ", Modo de Treino ativo"
                    msg_log = handler.chat.username + " ativou o modo de treino."
                logging.debug(msg_log)

            elif(handler.text == "/statistics"):
                text_ = "Ainda nao terminei esta funcionalidade.."
                
            bot.reply_to(handler, text_)           
            
        except KeyError:
            bot.reply_to(handler, handler.chat.first_name + \
                         ", este comando nao e valido\nuse /help" +\
                         " para mais informacoes")
                
