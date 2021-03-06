# darvis Project
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

<div align="center">
  <img src="assets/darvis.png">
</div> 

-----------------

Projeto com objetivo de explorar o ambiente de desenvolvimento e utilizar a integração com o [Telegram](https://web.telegram.org/).

O projeto pretende reunir uma série de técnicas de Inteligência Artificial como prática para tais.


## Projeto Não Comercial, apenas para uso pessoal e aprendizagem


## Como responder as primeiras mensagens com o bot?

* Para criar um Bot no [Telegram](https://web.telegram.org/#/login), realize o login e Acesse o canal [@BotFather](https://telegram.me/botfather).
	- Envie uma mensagem com ```/newbot``` e siga as instruções fornecidas até concluir. Após criar, o BotFather irá lhe fornecer o *Token* de acesso.

* Com o Bot criado, vamos configurar o ambiente de desenvolvimento. Neste projeto fora utilizado python e a biblioteca [telebot](https://github.com/eternnoir/pyTelegramBotAPI) para conexão com o Telegram.
	
	- Instale o [python](https://www.python.org/downloads/).	

	- Abra o terminal e instale a biblioteca via [pip](https://pypi.org/project/pip/):
		```$ pip install pyTelegramBotAPI```


* Para maiores detalhes, utilize a documentação contida no [github](https://github.com/eternnoir/pyTelegramBotAPI)


## Referências


* API de conexão com Telegram [telebot](https://github.com/eternnoir/pyTelegramBotAPI)
* Datasets:
	- [MovieLens](https://grouplens.org/datasets/movielens/)


## Docker

* Suporte incluido baseado neste [link](http://www.easy-analysis.com/dockerizing-python-flask-app-and-conda-environment/).

```$ docker build -t darvis:1.0 .```
### Para rodar
```$ docker run --name darvis -p 5001:443 --rm darvis:1.0```
* A porta ```443``` foi usada por conta do telegram.
