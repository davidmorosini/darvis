from random import randint
from utilidades import number_on_string
from utilidades import search_string
from recomenda import show_movies
from recomenda import search_titles

def decode_msg(msg, bot):

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

        return text_
    elif(len(msg.text.upper().split('RECOMENDAR')) > 1):
        bot.send_message(msg.chat.id, "Deixe me pensar...")

        title = msg.text.split('recomendar ')[1]
        text_ += "Aqui estao, espero que goste:\n\n"
        text_ += search_titles(title)
    else:
        fail_msg = ['Nao entendi..', 'Rapaz, nao vou poder ajudar', 'Acho que nao entendi o que quer', 'Nao sei fazer isso']
        text_ += fail_msg[randint(0, len(fail_msg) - 1)]

    bot.send_message(msg.chat.id, text_)

