##################################################################################
############# IMPORTATION ET TRAITEMENT DE LA BDD AVEC ARTICLES ##################
##################################################################################

# Les articles ont été scrappé en plusieurs fois et mis dans le fichier local le_parisien
import pandas as pd
import glob

df = pd.DataFrame()
for file_name in glob.glob('chemin/le_parisien/*.csv'):
    x = pd.read_csv(file_name)
    df = pd.concat([df,x],axis=0)
    
del x
del file_name

# Enlever si un même article a été scrappé plus d'une fois
df.drop_duplicates(keep=False,inplace=True) 
df.reset_index(drop=True,inplace=True)

# Enlever les articles dont le texte n'a pas pu être scrappé
dl=[]
for i in range(0,len(df)):
        if df['0'][i]=='[]':
            dl.append(i)
df.drop(index=dl,inplace=True)
del dl

# Création de nouvelles colonnes: la catégorie, le titre, le jour, le mois et l'année 
# de l'article
dft=df['1'].str.split("/", expand=True)
df['categorie']=dft[3]

dftt=df['1'].str.rsplit(pat="-",n=4,expand=True)
df['jour']=dftt[1]
df['mois']=dftt[2]
df['an']=dftt[3]

dfttt=dftt[0].str.rsplit(pat="/",n=1,expand=True)
df['titre']=dfttt[1].str.replace('-', ' ').str.title()

df=df.rename(columns={'0': 'texte','1':'lien'})

del dft 
del dftt
del dfttt
df.reset_index(drop=True,inplace=True)

# Création de la colonne ident qui sera utilisé plus tard pour identifier les entreprises 
# proche du Parisien
df['ident']='Non'


# Exporter la dataframe traitée dans un nouveau csv 
path=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien_tr.csv"
df.to_csv(path, index = False, header=True)


##################################################################################
##############  CREATION DE LA BDD D'ARTICLES POUR L'INTERFACE ###################
##################################################################################

#Les colonnes suivantes sont crées:
df=df.rename(columns={'texte': 'Texte','titre':'Titre'})
df['localisation']=''
df['personne']=''
df['entreprise']=''
df['Positive']=''
df['L\'entreprise']=''
df['PDG']=''
df['Detient_Media']=False
df['localisationPrecise']=''
  
df = df[['lien','Titre','localisation','Texte','personne','entreprise','Positive','L\'entreprise','PDG','Detient_Media','localisationPrecise']]

df.reset_index(inplace=True)
df.drop(['index'],axis=1,inplace=True)
 
#Appel de la fonction pour nettoyer nos articles
nettoyageArticle(df)

#Appel de la fonction qui nous permet d'ajouter les informations dans la dataframe 
ajout_TAG(df)

#Appel de la fonction pour ajouter un sentiment positif ou pas    
ajoutSentiment(df)

#Ajout de l'entreprise concernée par l'article
ajoutEntreprise(df)

#Ajout de la localisation de l'entreprise
ajoutLocalisation(df)

#Ajout du nom du PDG
recupererPDG(df)

#Ajout de la Collusion oui ou Non 
detientMedia(df)        


# Recupération de la base initiale sur les articles Le Parisien afin de réaliser un résumé
# pour chaque article suite à un oubli de notre part de garder le texteOriginal 
# dans la dataframe
df=pd.read_csv("C:/Users/idel/Desktop/M2/Python/le_parisien2_traitement.csv")

df_o = pd.read_csv("C:/Users/idel/Desktop/M2/Python/le_parisien2.csv")

df_o.drop_duplicates(keep=False,inplace=True) 
df_o.reset_index(drop=True,inplace=True)

df_o['0']=df_o['0'].astype(str)

from gensim.summarization import summarize
#Fonction permettant de réaliser des résumés en prenant seulement 20% du texte
def summarizePassage(text,summaryRatio=0.2):
     try:
       summary = summarize(text,split=False,ratio=summaryRatio)
     except:
       print("WARNING: Gensim unable to reduce: ", text)
       return [text]
     return summary
 
df["Resume"]=''    
for i in range(len(df)):
        df["Resume"][i]=summarizePassage(df_o['0'][i])
    
#Exportation:
df.to_csv('C:/Users/idel/Desktop/M2/Python/le_parisien2_traitement.csv',index = False, header=True)


