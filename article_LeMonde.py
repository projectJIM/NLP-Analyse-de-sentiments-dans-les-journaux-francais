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
    
#df.to_csv("C:\\Users\\idel\\Desktop\\M2\\Python\\LeMonde.csv",index=False)


#Creation des 60 articles dans l'environnement globale
for i in range(len(pageArticleTot)):
    globals()["Article_%s"%i]= ''.join(pageArticleTot[i])    

df.head(5)


#NLP


#Intallation
#pip install --upgrade pip
#pip install spacy   
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz
#pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.1.0/fr_core_news_sm-2.1.0.tar.gz

#conda install -c conda-forge spacy-model-fr_core_news_sm

#python -m spacy download en_core_web_sm
#python -m  spacy download fr_core_web_sm


#import spacy



import fr_core_news_sm
import en_core_web_sm
import nltk


nlpEng = en_core_web_sm.load()
nlp = fr_core_news_sm.load()


#Nettoyage des articles de la dataframe en supprimant les mots stop

#nltk.download('stopwords')
from nltk.corpus import stopwords
MotArret = set(stopwords.words('french'))


tokenisation_Article=[]
def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]

for i in range(len(df)):
    article = "".join(df.iloc[i,3])
    tmp=return_token(article)
    tokenisation_Article.append(tmp)

tokenisation_Article[1]
    
#Suppression '\xa0'
erreur = '\xa0'

#suppression des erreur
for i in range(len(tokenisation_Article)):

    tokenisation_Article[i] = list(filter(lambda a: a != erreur, tokenisation_Article[i]))

#☺Verificaition
tokenisation_Article[1]


#suppression des mots stop
#for i in range(len(tokenisation_Article)):
#    for j in range(len(tokenisation_Article[i])):
#        tmp=[]
#        mot=tokenisation_Article[i][j]
#        if mot not in MotArret:
#            tmp="".join(tokenisation_Article[i][j])
#    
#        tokenisation_Article_propre.append(tmp)
     

#suppression des mots stop , on met nos données dans une liste article Propre
#utilisation d'une fonction     
tokenisation_Article_propre=[]        
for i in range(len(tokenisation_Article)):
    tmp=(list(filter(lambda x: x not in MotArret, tokenisation_Article[i])))
    tmp=" ".join(tmp)
    tokenisation_Article_propre.append("".join(tmp))
    
#verification
tokenisation_Article_propre[1]


df['localisation']=''
df['personne']=''
df['entreprise']=''

#Recuperer catégorie (Named entity recognition)
#Ajout des lables dans notre dataframe
#On recupere les Article Prore (corrigé des mots stop et erreur /xa0)
def return_NER():
    # Tokeniser la phrase
    
    for i in range(len(df)):
        sentence=tokenisation_Article_propre[i]
        doc = nlp(sentence)
        titre = nlp(df['Titre'][i])
        localisation =[] 
        personne=[]
        entreprise=[]
    # Retourner le texte et le label pour chaque entité
        for X in doc.ents:
            if (X.label_=='ORG' ):
                    entreprise.append(X.text)
            elif X.label_=='LOC':
                localisation.append(X.text)            
            elif X.label_=='PER':
                personne.append(X.text)
        #Recupere les entreprises present dans le titre 
        #(si cela n'a pas été le cas dans le texte)        
        
        for Y in titre.ents:
            if (Y.label_=='ORG'):
                entreprise.append(Y.text)
        
        df['localisation'][i]=localisation
        df['personne'][i]=personne
        df['entreprise'][i]=entreprise

        if(df['entreprise'][i]==[]):
            df['entreprise'][i]=['nan']

#Appel de la fonction qui nous permet d'ajouter les informations dans la dataframe 
return_NER()

#Sentiment (positive ou negative)
 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
 
model = SentimentIntensityAnalyzer()
 
def get_sentiment(text):
    scores=model.polarity_scores(text)
    return scores.get('compound')

df["positive"]=""
for i in range(len(df)):
    positive = get_sentiment(tokenisation_Article_propre[i])>0.05
    df["positive"][i]=positive


#Ajout de la colonne l'entreprise qui va nous permettre d'ajouter l'entreprise
#la plus cité, en concluant que c'est l'entreprise sur laquelle l'article est réalisé
    
df['L\'entreprise']=''

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist 
for i in range(len(df)):
    token = df['entreprise'][i]
    fdist = FreqDist(token) 
    mot = fdist.most_common(1)
    
    df['L\'entreprise'][i]=mot[0][0]




#Comptage des occurence de mots
#Mise en place d'un graphique sous forme de Bar Plot
#Application du comptage de mot sur le deuxieme articles

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

maliste = tokenisation_Article_propre[2]
maliste = maliste.split(".")


# create a count vectorizer object
count_vectorizer = CountVectorizer()
# fit the count vectorizer using the text data
count_vectorizer.fit(maliste)
# collect the vocabulary items used in the vectorizer
dictionary = count_vectorizer.vocabulary_.items()

# lists to store the vocab and counts
vocab = []
count = []
# iterate through each vocab and count append the value to designated lists
for key, value in dictionary:
    vocab.append(key)
    count.append(value)
# store the count in pandas dataframe with vocab as index
vocab_bef_stem = pd.Series(count, index=vocab)
# sort the dataframe
vocab_bef_stem = vocab_bef_stem.sort_values(ascending=False)  

top_vacab = vocab_bef_stem.head(30)
top_vacab.plot(kind = 'barh', figsize=(5,10))


#Frequence des mots

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist 
token = return_token(tokenisation_Article_propre[2])
fdist = FreqDist(token) 
fdist1 = fdist.most_common(30) 
fdist1

#Stemming (recuperation de la racine des mots)  ou lemmatisation
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("french")

def stemming(text):    
    '''a function which stems each word in the given text'''
    text = [stemmer.stem(word) for word in text.split()]
    return " ".join(text) 

stem = stemming(tokenisation_Article_propre[2])
token = return_token(stem)
fdist = FreqDist(token) 
fdist1 = fdist.most_common(30) 
fdist1

maliste = "".join(stem)
maliste = maliste.split(".")
# create a count vectorizer object
count_vectorizer = CountVectorizer()
# fit the count vectorizer using the text data
count_vectorizer.fit(maliste)
# collect the vocabulary items used in the vectorizer
dictionary = count_vectorizer.vocabulary_.items()

# lists to store the vocab and counts
vocab = []
count = []
# iterate through each vocab and count append the value to designated lists
for key, value in dictionary:
    vocab.append(key)
    count.append(value)
# store the count in pandas dataframe with vocab as index
vocab_bef_stem = pd.Series(count, index=vocab)
# sort the dataframe
vocab_bef_stem = vocab_bef_stem.sort_values(ascending=False)  

top_vacab = vocab_bef_stem.head(30)
top_vacab.plot(kind = 'barh', figsize=(5,10))











    