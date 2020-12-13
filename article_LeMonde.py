

import requests
import bs4
# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import pandas as pd

import fr_core_news_sm
import nltk

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist 
from gensim.summarization import summarize
     


nlp = fr_core_news_sm.load()


def recupererArticle(domaine):
        
    requete = requests.get("https://www.lemonde.fr/"+domaine+"/") 
                
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
        
    
    #Suppression '\xa0'
    erreur = '\xa0'
    
    for i in range(len(pageArticleTot)):
    
        pageArticleTot[i] = list(filter(lambda a: a != erreur, pageArticleTot[i]))
    
    df = pd.DataFrame({'Auteur':auteurTot,'Url':listeUrl ,'Titre':listTitre,'TexteOriginal':pageArticleTot,
                       'Texte':pageArticleTot,
                       'localisation':'','personne':'','entreprise':'','Positive':'','L\'entreprise':'','PDG':'',
                       'Detient_Media':False,"localisationPrecise":''})

    
    

    df['TexteOriginal'] = df['TexteOriginal'].astype(str)
        
    
    globals()['dc']=df
    
#Scrapping et déplacement du scraping dans une dataframe d'un domaine présent dans journal Lemonde
recupererArticle("entreprises")    
 

#Nettoyage des articles de la dataframe en supprimant les mots stop

def nettoyageArticle(df):
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
    
        
    #Suppression '\xa0'
    erreur = '\xa0'
    
    #suppression des erreur
    for i in range(len(tokenisation_Article)):
    
        tokenisation_Article[i] = list(filter(lambda a: a != erreur, tokenisation_Article[i]))
    
    #suppression des mots stop , on met nos données dans une liste article Propre
    #utilisation d'une fonction     
    tokenisation_Article_propre=[]        
    for i in range(len(tokenisation_Article)):
        tmp=(list(filter(lambda x: x not in MotArret, tokenisation_Article[i])))
        tmp=" ".join(tmp)
        tokenisation_Article_propre.append("".join(tmp))
        
    
    for i in range(len(df)):
        df['Texte'][i]=tokenisation_Article_propre[i]

    
    df['Texte']=df['Texte'].astype(str)
    df['TexteOriginal']=df['TexteOriginal'].astype(str)

    

#Recuperer catégorie (Named entity recognition)
#Ajout des lables dans notre dataframe
#On recupere les Article Prore (corrigé des mots stop et erreur /xa0)
def ajout_TAG(df):
    # Tokeniser la phrase
    
    for i in range(len(df)):
        sentence=df['Texte'][i]
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
        
        df['localisation']=df['localisation'].astype(str)
        df['personne']=df['personne'].astype(str)
        df['entreprise']=df['entreprise'].astype(str)
        
        
        
                
        
#Sentiment (positive ou negative)
def ajoutSentiment(df):
    
     
    model = SentimentIntensityAnalyzer()
     
    def get_sentiment(text):
        scores=model.polarity_scores(text)
        return scores.get('compound')
    
    
    for i in range(len(df)):
        positive = get_sentiment(df['Texte'][i])>0.05
        df["Positive"][i]=positive
    
    df['Positive']=df['Positive'].astype(str)

#Ajout de la colonne l'entreprise qui va nous permettre d'ajouter l'entreprise
#la plus cité, en concluant que c'est l'entreprise sur laquelle l'article est réalisé
    

#Fonction donnant l'entreprise concerné par l'article

def ajoutEntreprise(df):
    for i in range(len(df)):
        token = df['entreprise'][i]
        token=token.split(",")
        fdist = FreqDist(token) 
        mot = fdist.most_common(1)
        df['L\'entreprise'][i]=mot[0][0]

    
    df['L\'entreprise']=df['L\'entreprise'].astype(str)


def ajoutLocalisation(df):
    for i in range(len(df)):
        token = df['localisation'][i]
        token=token.split(",")
        fdist = FreqDist(token) 
        mot = fdist.most_common(1)
        df['localisationPrecise'][i]=mot[0][0]

    
    df['localisationPrecise']=df['localisationPrecise'].astype(str)

#Creation de la dataframe des media_francais et leurs influences

media_francais=pd.read_excel('C:/Users/idel/Desktop/M2/Python/medias_francais.xlsx')
media_francais['nom']=media_francais['nom'].astype(str)

#recuperation du PDG de chaque entreprise liée à chaque article


def recupererPDG(df):
    
    for i in range(len(df)):
        try:
            requete = requests.get("https://www.google.com/search?q=pdg+"+df['L\'entreprise'][i]+"&")
            page = requete.content
            soup = bs4.BeautifulSoup(page, 'lxml')  
            secteur = soup.find("div",attrs={"class":'BNeawe deIvCb AP7Wnd'})
            df['PDG'][i]=secteur.text
        except:
            continue
        
    #Suppression des erreurs
    df['PDG'] = df['PDG'].str.replace('Autres questions posées','')
    df['PDG'] = df['PDG'].str.replace('Images','')
    df['PDG'] = df['PDG'].str.replace('Recherches associées','')
    df['PDG'] = df['PDG'].str.replace('Afficher les résultats pour','')
    
    for i in range(len(df)):
        if(df['PDG'][i]==df['L\'entreprise'][i]):
            df['PDG'][i]= ''
        
    #Webscrapping de nouveau avec une nouvelle balise pour récupérer les pdg manquants
    for i in range(len(df)):
        if(df['PDG'][i]==''):
            try:
                requete = requests.get("https://www.google.com/search?q=pdg+de+"+df['L\'entreprise'][i]+"&")
                page = requete.content
                soup = bs4.BeautifulSoup(page, 'lxml')  
                secteur = soup.find("div",attrs={"class":'BNeawe s3v9rd AP7Wnd'})
                df['PDG'][i]=secteur.text
            except:
                continue
    
    import re
    def existeDigit(inputString):
        return bool(re.search(r'\d', inputString))
    
    #Suppression des PDG associé à NAN
    for i in range(len(df)):
        if(df['L\'entreprise'][i]=='nan'):
            df['PDG'][i]=''
    
    #Recupere toute les phrase afin de les remplacer par le personnage cité dans la phrase
    for i in range(len(df)):
        if(len(df['PDG'][i])>30):
            doc = nlp(df['PDG'][i])
            for X in doc.ents:
                if (X.label_=='PER' ):
                    df['PDG'][i]=X.text
    
    #Suppression des textes tronquer présentant des chiffres 
    for i in range(len(df)):
        if(existeDigit(df['PDG'][i])==True):
            df['PDG'][i]=''

    
    df['PDG']=df['PDG'].astype(str)
    


#ajout de la présence du PDG comme détenteur d'un media

def detientMedia(df):
    for i in range(len(media_francais)):
        for j in range(len(df)):
            if(media_francais['nom'][i]==df['PDG'][j]):
                df['Detient_Media'][j]=True


  
    df['Detient_Media']=df['Detient_Media'].astype(str)




#Traitement Article Le Monde
    
#Appel de la fonction pour nettoyer nos articles
nettoyageArticle(dc)

for i in range(len(dc)):
         dc['Texte'][i]=dc['Texte'][i].replace('\xa0','')
         dc['TexteOriginal'][i]=dc['TexteOriginal'][i].replace('\xa0','')
         
         

#Appel de la fonction qui nous permet d'ajouter les informations dans la dataframe 
ajout_TAG(dc)
#Appel de la fonction pour ajouter un sentiment positive ou pas    
ajoutSentiment(dc)
#Ajout de l'entreprise concerné par l'article



for i in range(len(dc)):
            dc['localisation'][i]=dc['localisation'][i].replace('[','')
            dc['localisation'][i]=dc['localisation'][i].replace(']','')
            dc['personne'][i]=dc['personne'][i].replace('[','')
            dc['personne'][i]=dc['personne'][i].replace(']','')
            dc['entreprise'][i]=dc['entreprise'][i].replace('[','')
            dc['entreprise'][i]=dc['entreprise'][i].replace(']','')

ajoutEntreprise(dc)

ajoutLocalisation(dc)

#Ajout du nom du PDG
recupererPDG(dc)
#Ajout de la Collusion oui ou Non 
detientMedia(dc)        


#Fonction permettant de réaliser des résumé en prenant seulement 20% du texte
def summarizePassage(text,summaryRatio=0.2):
     try:
       summary = summarize(text,split=False,ratio=summaryRatio)
     except:
       print("WARNING: Gensim unable to reduce: ", text)
       return [text]
     return summary
 
dc['Resume']=''    
for i in range(len(dc)):    
    dc['Resume'][i]=summarizePassage(dc["TexteOriginal"][i])

dc["Resume"]=dc["Resume"].astype(str)

#Suppression espace insécable

for i in range(len(dc)):
         dc['Texte'][i]=dc['Texte'][i].replace('\\xa0','')
         dc['Resume'][i]=dc['Resume'][i].replace('\\xa0','')

dc_bis['Resume']=''    
for i in range(len(dc_bis)):    
    dc_bis['Resume'][i]=summarizePassage(dc_bis["TexteOriginal"][i])


#Suppression espace insécable

dc_bis["Resume"]=dc_bis["Resume"].astype(str)
for i in range(len(dc_bis)):
         dc_bis['Texte'][i]=dc_bis['Texte'][i].replace('\\','')
         dc_bis['Resume'][i]=dc_bis['Resume'][i].replace('\\','')


dc.to_csv('C:/Users/idel/Desktop/M2/Python/le_Monde_traitement.csv',index = False, header=True)

dc_bis.to_csv("C:/Users/idel/Desktop/M2/Python/Eco_lemonde_traitement.csv",index = False, header=True)
