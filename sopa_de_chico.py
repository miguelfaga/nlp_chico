# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests


mainpage_response = requests.get("https://www.letras.com.br/chico-buarque")
mainpage = mainpage_response.content

soup = BeautifulSoup(mainpage, 'html.parser')

titles = soup.find_all(attrs = {'class':"lyric-name title-default weight-normal"})
#Retorna todas as tags identificadas com a classe

links = soup.find_all(attrs = {'class': "item-box item-list"})
#Retorna todas as tags identificadas com a classe

main = zip(titles, links)

data_chico = {}

for title, link in main:
    title = title.string
    link = link['href'] #pega o link dentro da tag 'a'
    data_chico[title] = link

chico_data = []

for title in data_chico:
    lyric_page_url = data_chico[title]
    lyric_page_response = requests.get(lyric_page_url)
    lyric_page = lyric_page_response.content
    
    lyric_soup = BeautifulSoup(lyric_page, 'html.parser')
    lyric = lyric_soup.find_all("print-component")[0][':lyrics']
    data_chico[title] = lyric
    chico_data.append([title, lyric])
    
    print("{} salvo.".format(title))

df = pd.DataFrame(chico_data, columns = ["title", "lyrics"])
df.to_csv("chico_data.csv")