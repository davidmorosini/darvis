import numpy as np
import pandas as pd


def series_to_text(series):
    #o primeiro da lista é sempre o próprio filme
    qtd = series.shape[0] - 1
    text = ""
    for i in range(1, qtd):
        text += series['title'][i] + '\n'

    return text

#Cria um dataframe com os filmes
def import_titles():
    colunas = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv('datasets/u.data', sep='\t', names=colunas)
    df_titles = pd.read_csv('datasets/Movie_Id_Titles')

    #Unindo os titulos dos filmes as suas classficiações
    df = pd.merge(df, df_titles, on='item_id')

    return df

#Calcula a correlação entre as avaliações e lista os filmes
def search_titles(title):
    df = import_titles()

    #Agrupando as classificações dos filmes
    df_ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
    #Colocando a contagem de classificações dos filmes
    df_ratings['count'] = pd.DataFrame(df.groupby('title')['rating'].count())

    #Pivontando o dataframe, para ter as relações de quem classificou
    df_pivot = df.pivot_table(index='user_id', columns='title', values='rating')

    #buscando as classificações do filme que queremos usar como base de recomendação
    user_ratings = df_pivot[title]

    #Calculando a correlação entre as avaliações
    recommend = df_pivot.corrwith(user_ratings)

    correlation = pd.DataFrame(recommend, columns=['correlation'])
    #Excluindo os casos que não foram avaliados
    correlation.dropna(inplace=True)

    correlation = correlation.join(df_ratings['count'])

    min_ratings = 100
    qtd_recommends = 10
    
    list_recommend = correlation[correlation['count'] > min_ratings].sort_values('correlation', ascending=False).head(qtd_recommends)
    list_recommend = list_recommend.reset_index()

    
    text = series_to_text(list_recommend)
    
    return text
    

#Lista os filmes
def show_movies(qtd=10, top_view=False, alfabetic=True):
    df = import_titles()

    #Agrupando as classificações dos filmes
    df_ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
    #Colocando a contagem de classificações dos filmes
    df_ratings['count'] = pd.DataFrame(df.groupby('title')['rating'].count())

    

    filmes = df_ratings.sort_values('count', ascending=top_view).head(qtd).sort_values('title', ascending=alfabetic)
    filmes = filmes.reset_index()

    return filmes['title']
    

    










    
