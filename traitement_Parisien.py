

##################################################################################
#########  1. Importing the corpora with news articles ###########################
##################################################################################

import pandas as pd

import glob

df = pd.DataFrame()
for file_name in glob.glob('C:/Users/idel/Desktop/M2/Python/le_parisien2.csv'):
    x = pd.read_csv(file_name)
    df = pd.concat([df,x],axis=0)
    
del x
del file_name

# dropping duplicate values 
df.drop_duplicates(keep=False,inplace=True) 
df.reset_index(drop=True,inplace=True)

dl=[]
for i in range(0,len(df)):
        if df['0'][i]=='[]':
            dl.append(i)
df.drop(index=dl,inplace=True)
del dl

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

df['ident']='Non'


path=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien_tr.csv"

df.to_csv(path, index = False, header=True)

######################Imad #############

#Article Le Parisien:

import glob

df = pd.DataFrame()
for file_name in glob.glob('C:/Users/idel/Desktop/M2/Python/le_parisien2.csv'):
    x = pd.read_csv(file_name)
    df = pd.concat([df,x],axis=0)
    
del x
del file_name

# dropping duplicate values 
df.drop_duplicates(keep=False,inplace=True) 
df.reset_index(drop=True,inplace=True)

dl=[]
for i in range(0,len(df)):
        if df['0'][i]=='[]':
            dl.append(i)
df.drop(index=dl,inplace=True)
del dl

dft=df['1'].str.split("/", expand=True)
df['categorie']=dft[3]

dftt=df['1'].str.rsplit(pat="-",n=4,expand=True)
df['jour']=dftt[1]
df['mois']=dftt[2]
df['an']=dftt[3]


dfttt=dftt[0].str.rsplit(pat="/",n=1,expand=True)
df['titre']=dfttt[1].str.replace('-', ' ').str.title()

del dfttt
del dftt
del dft
    


df=df.rename(columns={'0': 'Texte','1':'lien','titre':'Titre'})
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
#Appel de la fonction pour ajouter un sentiment positive ou pas    
ajoutSentiment(df)
#Ajout de l'entreprise concerné par l'article


ajoutEntreprise(df)

ajoutLocalisation(df)

#Ajout du nom du PDG
recupererPDG(df)
#Ajout de la Collusion oui ou Non 
detientMedia(df)        


df.to_csv('C:/Users/idel/Desktop/M2/Python/le_parisien2_traitement.csv',index = False, header=True)


