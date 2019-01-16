from random import randint
from utilidades import number_on_string
from utilidades import search_string
from recomenda import show_movies
from recomenda import search_titles
import logging

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

    ##Informações necessarias para predicao dos comandos
    modelo_comandos_ = None
    bow_transformer_ = None
    tfidf_transformer_ = None


    #melhorar isso aqui
    pendencias = None
    label_pendencia = None
    ultimo_comando = None
    

    def __init__(self):
        #Iniciando o Log de treinamentos
        try:
            log_treinos = open('Logs/log_train.log', 'a')
            logging.debug('Arquivo de de Log de Treinos lido com sucesso.')
        except:
            logging.debug('Problemas ao ler o arquivo de Log de Treinos, criando um novo.')
            log_treinos = open('Logs/log_train.log', 'w')
        log_treinos.write('# LOG DE TREINO #\n')
        log_treinos.close()
            
    
    def write_log_train(self, msg):
        try:
            log_treinos = open('Logs/log_train.log', 'a')
            log_treinos.write(msg + '\n')
            log_treinos.close()
        except:
            pass

    def write_dataset_comandos(self, txt):
        try:
            dataset_comandos = open('datasets/comandos', 'a')
            dataset_comandos.write(txt + '\n')
            dataset_comandos.close()
        except:
            pass


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
        comandos = pd.read_csv('datasets/comandos', sep='\t', names=['label', \
                                                                     'comando'])
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
        if(string == None):
            return None
        else:
            bow_predict = self.bow_transformer_.transform([string])
            tfidf_predict = self.tfidf_transformer_.transform(bow_predict)
            return self.modelo_comandos_.predict(tfidf_predict)[0]
    

    def decode_msg(self, msg, bot):
        if(self.TrainMode):
            
            if(self.pendencias != None):
                if(msg.text.lower() == 'recomendar'):
                    self.write_dataset_comandos('recomendar\t' + self.ultimo_comando)
                    self.ultimo_comando = None
                    self.pendencias = None
                    self.start_model_decode()
                    bot.send_message(msg.chat.id, 'Ja anotei no meu rascunho para nao esquecer mais!')
                    
                elif(msg.text.lower() == 'listar'):
                    self.write_dataset_comandos('listar\t' + self.ultimo_comando)
                    self.ultimo_comando = None
                    self.pendencias = None
                    self.start_model_decode()
                    bot.send_message(msg.chat.id, 'Ja anotei no meu rascunho para nao esquecer mais!')

                elif(msg.text.lower() == 'nada'):
                    self.write_dataset_comandos('nada\t' + self.ultimo_comando)
                    self.ultimo_comando = None
                    self.pendencias = None
                    self.start_model_decode()
                    bot.send_message(msg.chat.id, 'Ja anotei no meu rascunho para nao esquecer mais!')

                else:
                   bot.send_message(msg.chat.id, 'Vish.. Acho que voce errou ein.. Manda de novo por gentileza o comando correto :D') 
                
            else:
                if(msg.text.lower() == 'n' and self.ultimo_comando != None):
                    bot.send_message(msg.chat.id, 'Poxa, me desculpe, estou aprendendo ainda..'+\
                                     ' Me ajude a melhorar me indicando qual seria o comando correto:\n'+\
                                     '[recomendar, listar, nada]')
                    self.pendencias = self.ultimo_comando
                    self.label_pendencia = None
                    
                elif(msg.text.lower() == 's' and self.ultimo_comando != None):
                    bot.send_message(msg.chat.id, 'SHOW!')
                    self.write_dataset_comandos(self.label_pendencia + '\t' + self.ultimo_comando)
                    self.ultimo_comando = None
                    self.pendencias = None
                    self.label_pendencia = None
                    self.start_model_decode()
                else:
                    comando_predito = self.prediz_comando(msg.text)
                    self.ultimo_comando = msg.text
                    self.label_pendencia = comando_predito
                    bot.send_message(msg.chat.id, \
                                     '{}, entendi que se trata do comando: {}'.format(\
                                         msg.chat.first_name, comando_predito))
                    bot.send_message(msg.chat.id, 'Entendi certo? (s/n)')

        else:
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

