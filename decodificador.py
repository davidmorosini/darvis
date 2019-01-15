from random import randint
from utilidades import number_on_string
from utilidades import search_string
from recomenda import show_movies
from recomenda import search_titles

def decode_msg(msg, bot):
    if(len(msg.text.upper().split('LISTAR')) > 1):
        bot.send_message(msg.chat.id, 'Tudo bem, vou selecionar alguns aqui..')
        text_ = ""
    
        #Listar Filmes
        qtd_filmes = number_on_string(msg.text)
        if(qtd_filmes == None):
            #colocar a quantidade default
            qtd_filmes = 10
            text_ += "Listando uma quantidade default de filmes: \n\n"
        else:
            text_ += "Listando os " + str(qtd_filmes) + " como você pediu: \n\n"

        filmes = show_movies(qtd=qtd_filmes)

        for i in range(0, qtd_filmes):
            text_ += filmes[i] + '\n'

        text_ += '\n\nrecomendar [nome do filme] <para recomendações..>'

        return text_
    elif(len(msg.text.upper().split('RECOMENDAR')) > 1):
        bot.send_message(msg.chat.id, "Deixe me pensar...")

        title = msg.text.split('recomendar ')[1]
        text = "Aqui estão, espero que goste:\n\n"
        text += search_titles(title)
        return text
    else:
        fail_msg = ['Não entendi..', 'Rapaz, não vou poder ajudar', 'Acho que não entendi o que quer', 'Não sei fazer isso']
        return fail_msg[randint(0, len(fail_msg) - 1)]
