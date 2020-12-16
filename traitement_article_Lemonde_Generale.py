
import pandas as pd

dt=pd.read_csv("C:/Users/idel/Desktop/M2/Python/Eco_lemonde.csv")
dt.drop('Unnamed: 0.1.1', inplace=True, axis=1)


dt['localisation']=''
dt['personne']=''
dt['entreprise']=''
dt['Positive']=''
dt['L\'entreprise']=''
dt['PDG']=''
dt['Detient_Media']=False
dt['localisationPrecise']=''


#Appel de la fonction pour nettoyer nos articles
nettoyageArticle(dt)

for i in range(len(dt)):
         dt['Texte'][i]=dt['Texte'][i].replace('\xa0','')
         dt['TexteOriginal'][i]=dt['TexteOriginal'][i].replace('\xa0','')

#Appel de la fonction qui nous permet d'ajouter les informations dans la dataframe 
ajout_TAG(dt)
#Appel de la fonction pour ajouter un sentiment positif ou pas    
ajoutSentiment(dt)
#Ajout de l'entreprise concernée par l'article



for i in range(len(dt)):
            dt['localisation'][i]=dt['localisation'][i].replace('[','')
            dt['localisation'][i]=dt['localisation'][i].replace(']','')
            dt['personne'][i]=dt['personne'][i].replace('[','')
            dt['personne'][i]=dt['personne'][i].replace(']','')
            dt['entreprise'][i]=dt['entreprise'][i].replace('[','')
            dt['entreprise'][i]=dt['entreprise'][i].replace(']','')

ajoutEntreprise(dt)

ajoutLocalisation(dt)

#Ajout du nom du PDG
recupererPDG(dt)
#Ajout de la Collusion oui ou Non 
detientMedia(dt) 



dt.to_csv('C:/Users/idel/Desktop/M2/Python/Eco_lemonde_traitement.csv',index = False, header=True)


