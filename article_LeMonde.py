import requests
import bs4
#Import BeautifulSoup 
from bs4 import BeautifulSoup
import pandas as pd

#def recup(domaine):
    
requete = requests.get("https://www.lemonde.fr/entreprises/") 
            
page = requete.content
soup = bs4.BeautifulSoup(page, 'lxml')

  
url = soup.find_all("a",attrs={"class":'teaser__link'})

titre = soup.find_all("h3",attrs={"class":'teaser__title'})


listeUrl = []
listTitre = []

for a in url :
    listeUrl.append(a.get('href'))
    
    if len(listeUrl) ==100 :
        break
    
for a in range(len(titre)) :
    listTitre.append(titre[a].text)
        
    if len(listTitre) ==100 :
        break


pageArticleTot =[]
auteurTot=[]

for i in range(len(listeUrl)):
    paragrapheTot=[]
    
    requeteUrl = requests.get(listeUrl[i])
    pageUrl = requeteUrl.content
    soupUrl = bs4.BeautifulSoup(pageUrl, 'lxml')
    paragraphe = soupUrl.find_all("p",attrs={"class":'article__paragraph'})
    
    auteur = soupUrl.find("meta", {"property": "og:article:author"})
    auteur = auteur['content'] if auteur else 'Inconnu'
        
    auteurTot.append(auteur)
    
    for i in paragraphe:
        paragrapheTot.append(i.text)
            
    pageArticleTot.append(paragrapheTot)


df = pd.DataFrame({'Auteur':auteurTot,'Url':listeUrl ,'Titre':listTitre,'Texte':pageArticleTot})
    
df.to_csv("C:\\Users\\idel\\Desktop\\M2\\Python\\LeMonde.csv",index=False)



for i in range(len(pageArticleTot)):
    globals()["Article_%s"%i]= ''.join(pageArticleTot[i])    




#NLP


#Intallation
#pip install --upgrade pip
#pip install spacy   
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz
#pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.1.0/fr_core_news_sm-2.1.0.tar.gz

#conda install -c conda-forge spacy-model-fr_core_news_sm

#python -m spacy download en_core_web_sm
#python -m  spacy download fr_core_web_sm






    