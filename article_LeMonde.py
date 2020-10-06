import requests
import bs4
#Import BeautifulSoup 
from bs4 import BeautifulSoup

#def recup(domaine):
    
requete = requests.get("https://www.lemonde.fr/economie-francaise/") 
            
page = requete.content
soup = bs4.BeautifulSoup(page, 'lxml')

print(soup.prettify())
              
  
url = soup.find_all("a",attrs={"class":'teaser__link'})

titre = soup.find_all("h3",attrs={"class":'teaser__title'})


listeUrl = []
listTitre = []

for a in url :
    listeUrl.append(a.get('href'))
    
    if len(listeUrl) ==5 :
        break
    
for a in range(len(titre)) :
    listTitre.append(titre[a].text)
        
    if len(listTitre) ==5 :
        break


pageArticle =[]

for i in range(len(listeUrl)):
    paragrapheTot=[]
    titreTot=[]
    requeteUrl = requests.get(listeUrl[i])
    pageUrl = requeteUrl.content
    soupUrl = bs4.BeautifulSoup(pageUrl, 'lxml')
    paragraphe = soupUrl.find_all("p",attrs={"class":'article__paragraph'})
    
    titre = soupUrl.find_all("h3",attrs={"class":'article__title'})
    for i in paragraphe:
        paragrapheTot.append(i.text)
        titreTot.append(titre)
        
    pageArticle.append(paragrapheTot)



pageArticle


for i in range(len(pageArticle)):
    globals()["Article_%s"%i]= ''.join(pageArticle[i])    





#NLP

pip install spacy

python3 -m spacy download fr_core_web_sm

import spacy
import fr_core_web_sm

nlp = spacy.load("fr_core_news_sm")


def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]



#return url
            
#recup("economie-francaise")