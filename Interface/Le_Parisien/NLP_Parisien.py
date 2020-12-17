import pandas as pd
import nltk
#nltk.download()


##################################################################################
###3####  LE PARISIEN: ENTREPRISES LIEES ET ENTREPRISES CONCURRENTES  #############
##################################################################################

org_lvmh=['LVMH', 'Louis Vuitton','Ao Yun','Ardbeg','Belvedere','Bodega Numanthia',
'Cape Mentelle','Chandon','Château Cheval Blanc',"Château d'Yquem","Cloudy Bay","Dom Pérignon",
"Glenmorangie","Hennessy","Krug","Mercier","Moët & Chandon","Newton Vineyard",
"Ruinart","Terrazas de los Andes","Veuve Clicquot","Volcan de mi tierra",
"Woodinville","Wenjun","Berluti","Céline","Charles & Keith","Christian Dior",
"Deus Ex Machina","Emilio Pucci","Fendi","Fenty","Givenchy","Kenzo","Loewe",
"Loro Piana","Marc Jacobs","Moynat","Nicholas Kirkwood","Patou","Rimowa",
"R. M. Williams","Thomas Pink","Acqua di Parma","Benefit Cosmetics","Fresh",
"Givenchy Parfums","Guerlain","Kendo Brands","Bite Beauty",
"Fenty Beauty by Rihanna", "Marc Jacobs Beauty","KVD Vegan Beauty",
"Kat Von D Beauty","OleHenriksen","Ole Henriksen","Kenzo Parfums","Maison Francis Kurkdjian",
"Make Up For Ever","Christian Dior","Loewe","Bulgari","Chaumet","FRED",
"Hublot","TAG Heuer","Zenith","DFS","La Grande Epicerie","Le Bon Marché","Sephora",
"Starboard Cruise Services","Belmond", "Caffè-Pasticceria Cova","Cheval Blanc",
"Royal Van Lent Shipyard","Princess Yachts","Les Echos","Pinarello",'Bernard Arnault',
'Radio Classique','Investir - Le Journal des Finances','la Samaritaine','Bvlgari','Celine']


org_concurrentes=['Chanel','Hermes','Gucci','Burberry','Cartier','Prada','Rémy Martin',
                  'Pernod Ricard','Martell','Chivas Regal','Absolut Vodka','Ballantines',
                  'Courvoisier']


##################################################################################
########################  IMPORTATION DES ARTICLES ###############################
##################################################################################

df=pd.read_csv('C:/Users/jovan/OneDrive/Radna površina/Paris 1/NLP_2/data/le_parisien/le_parisien_final.csv')

# 13 194 articles du Parisien

##################################################################################
########################  TRAITEMENT DE TEXTE  ###################################
##################################################################################

# Source d'inspiration: https://machinelearningmastery.com/clean-text-machine-learning-python/

################ Enlever la ponctuation #######################
def remove_punctuation(text):
    """Fonction qui prend en input le texte et enlève la ponctuation"""
    import string
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

df['texte_nopuk'] = df['texte'].apply(remove_punctuation)


#################### Tokenization et enlever la ponctuation: ##################
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

df['tokens']=df['titre']
for i in range(0,len(df)):
    df['tokens'][i] = tokenizer.tokenize(df['texte'][i])

#print(df['tokens'][0])

###################### Enlever les mots vides (au, ce, de...) #####################
from nltk.corpus import stopwords
sw = stopwords.words('french')

# On rajoute a qui, surprise, n'y était pas.
sw.append('a')
       
def stopwords(text):
    text = [word for word in text if word.lower() not in sw]
    return " ".join(text)

df['no_sw'] = df['tokens'].apply(stopwords)    

#df['no_sw'][0]

df['tokens_no_sw']= df['no_sw']

# Tokenization:
for i in range(0,len(df)):
    df['tokens_no_sw'][i] = [t for t in df['no_sw'][i].split()]

#df['tokens_no_sw'][0]

########################## RACINE DU MOT ###################################
# On utilise le SnowballStemmer français de NLTK
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("french")

def stemming(text):    
    """ Le stemming est la 'coupure' de la partie insignifiante du mot """
    text = [stemmer.stem(word) for word in text.split()]
    return " ".join(text) 

df['same_roots'] = df['no_sw'].apply(stemming)

#df['same_roots'][0]

# Tokenization:
df['same_roots_tk']=df['same_roots']
for i in range(0,len(df)):
    df['same_roots_tk'][i] = [t for t in df['same_roots'][i].split()]

#df['same_roots_tk'][0]

##################################################################################
########################## ANALYSE DES TEXTES  ###################################
##################################################################################

########################## COUNT WORDS ########################################

def count_words(i,text):
    " Compte l'occurence d'un mot dans l'article i "
    freq = nltk.FreqDist(df[text][i])
    for key,val in freq.items():
        print(str(key) + ':' + str(val))
    freq.plot(20, cumulative=False)

count_words(0,text='tokens_no_sw')
count_words(0,text='same_roots_tk')


########################## IDENTIFICATION #####################################

# Nous allons chercher à identifier les entreprises proches du Parisien
# ATTENTION: Savoir que cette partie peut mettre beaucoup de temps à s'exécuter

def return_POS(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner les étiquettes de chaque token
    return [(X, X.pos_) for X in doc]

def ident_wordtype(text):
    noun = pd.DataFrame(nltk.pos_tag(df[text][0]))
    cl_np=[]
    for i in range(0,len(noun)):
        if noun[1][i]=='NNP':
               cl_np.append(noun[0][i]) 
    return noun

token_type=ident_wordtype('tokens')
ident_wordtype('no_puk_sw_tk')

# Cette partie au-dessus n'a finalement pas été utile car on a trouvé le package fr_core_news_sm

import fr_core_news_sm
#from pprint import pprint
nlp = fr_core_news_sm.load()

# De la documentation de spaCy:
# Possible types identifiés:
#PERSON	People, including fictional.
#NORP	Nationalities or religious or political groups.
#FAC	Buildings, airports, highways, bridges, etc.
#ORG	Companies, agencies, institutions, etc.
#GPE	Countries, cities, states.
#LOC	Non-GPE locations, mountain ranges, bodies of water.
#PRODUCT	Objects, vehicles, foods, etc. (Not services.)
#EVENT	Named hurricanes, battles, wars, sports events, etc.
#WORK_OF_ART	Titles of books, songs, etc.
#LAW	Named documents made into laws.
#LANGUAGE	Any named language.
#DATE	Absolute or relative dates or periods.
#TIME	Times smaller than a day.
#PERCENT	Percentage, including ”%“.
#MONEY	Monetary values, including unit.
#QUANTITY	Measurements, as of weight or distance.
#ORDINAL	“first”, “second”, etc.
#CARDINAL	Numerals that do not fall under another type.

df['org']=df['titre']

def ident_nom_propre(i,text):
    """Identifie les chiffres,dates et noms propres. Les organisations seront associés à l'article"""
    doc = nlp(df[text][i])
    #pprint([(X.text, X.label_) for X in doc.ents])
    ident=[(X.text, X.label_) for X in doc.ents]
#    id2=pd.DataFrame(ident, columns=['mots','type'])    
    org=[]
    for j in range(0,len(ident)):
        if ident[j][1]=='ORG':
              org.append(ident[j][0])
    df['org'][i]=org
#    return id2

#On va lancer la fonction pour tout article:
for art in range(0,len(df)):
    ident_nom_propre(art,'no_sw')
    

df['ident']='Non'
       
def ident_org(i):
    """ Identifie si une entreprise du groupe LVMH est dans l'article """
    for i in range(len(df)):
        check =  any(item in df['org'][i] for item in org_lvmh)
        if check is True:
            df['ident'][i]='Oui'
            
import time
start = time.time()                  
for i in range(len(df)):                             
    ident_org(i)
end = time.time()
print(round(end - start),'secondes')

########################################################################################
########################## EXPORTATION DES DF TRAITES #################################
########################################################################################

########################### TOUS LES ARTICLES TRAITES #############################
path=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien\le_parisien_final.csv"
df.to_csv(path, index = False, header=True)

#Creer une df avec uniquement les articles d'economies
#df_eco=df[df['categorie']=='economie']

#Creer une dataframe avec uniquement les articles en lien avec LVMH
#df_lvmh=df[df['ident']=='Oui']    

########################## ARTICLES POSITIFS ET NEGATIFS IDENTIFIES ####################

#Manuellement:   
pos=[1,2,4,7,9,10,12,16,23,24,25,26,27,28,29,32,34,35,36,37,38,41,43,45,48,51,54,55,57,
41,63,64,65,66,67,68,74,76,78,80,84,85,91,96,97,104,112,113,117,119,120,123,134,136,139,146,
153,165,168,169,170,222,243,480,544,554,640,649,651,1749,
2217,2465,4420,4429,4440,4493,4633,4767,4980,4983,5107,6733,6797,6806,6945,6949]

neg=[0,3,5,6,8,11,13,14,15,17,18,19,20,21,22,30,31,33,39,40,42,44,46,47,49,50,52,53,56,58,59,
     60,61,62,69,70,71,72,73,75,77,79,81,82,83,86,87,88,89,90,92,93,94,95,98,99,
     100,101,102,103,105,107,108,109,115,116,121,125,126,127,128,135,137,138,139,140,141,148,
     156,158,164,169,
     784,761,
     1065,1270,1632,1994,
     2014,2055,2210,2359,2636,3650,3660,4210,4216,4485,4549,4660
     ,6006,6665,6671,6721,6792,6888,6898,9840]

#df['categorie'].unique()

df_pos=df.loc[pos]
df_neg=df.loc[neg]

path2=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien\le_parisien_pos.csv"
path3=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien\le_parisien_neg.csv"

df_pos.to_csv(path2, index = False, header=True)
df_neg.to_csv(path3, index = False, header=True)

all_av=pos+neg
df_avis=df.loc[all_av]
df_avis.reset_index(drop=True,inplace=True)

######################################################################################
########################## TRAITEMENT BAYES NLTK ####################################
######################################################################################

# Source d'inspiration: https://www.datatechnotes.com/2019/05/sentiment-classification-with-nltk.html

# Dans cette partie nous avons traité nos articles pour les formatter de manière convenable
# au Naive Bayes du NLTK

#ATTENTION: Dure longtemps et à lancer une seule fois

from nltk.tokenize import word_tokenize

def bayes_prep(text):
    data=([(posi[text], 'positive') for index, posi in df_pos.iterrows()]+
           [(nega[text], 'negative') for index, nega in df_neg.iterrows()])
    tokens=list(word.lower() for words in data for word in word_tokenize(words[0]))
    tokens2 = [item.replace("'","") for item in tokens]
    tokens3 = [x for x in tokens2 if x]  
    tokenss = []
    [tokenss.append(x) for x in tokens3 if x not in tokenss]
    tokens_set=set(tokenss)
    #    print(tokens_set)
    #Donc on va creer un ensemble de mots apparaissant sur l'ensemble des articles
    
    # Pour chaque article de data, on va prendre son label positive/negatif x[1]. 
    # On va aussi tokenizer les mots de x[0] et mettre un label true/false si le mot est dans
    # l'article ou pas.
    train=[({word:(word in word_tokenize(x[0])) for word in tokens_set}, x[1]) for x in data]
    return train

txt=['texte', 'no_sw', 'same_roots', 'texte_nopuk']

train_texte=bayes_prep('texte')
train_no_sw=bayes_prep('no_sw')
train_same_roots=bayes_prep('same_roots')
train_texte_nopuk=bayes_prep('texte_nopuk')

#df_avis=pd.read_csv('C:/Users/jovan/OneDrive/Radna površina/Paris 1/NLP_2/data/le_parisien/le_parisien_avis.csv')

df_texte = pd.DataFrame(train_texte, columns =['Label_texte', 'Avis'])
df_no_sw = pd.DataFrame(train_no_sw, columns =['Label_no_sw', 'Avis'])
df_same_roots = pd.DataFrame(train_no_sw, columns =['Label_same_roots', 'Avis'])
df_texte_nopuk = pd.DataFrame(train_no_sw, columns =['Label_no_puk', 'Avis'])

df_avis['Label_texte'] = df_texte['Label_texte']
df_avis['Avis'] = df_texte['Avis']
df_avis['Label_no_sw'] = df_no_sw['Label_no_sw']
df_avis['Label_same_roots'] = df_same_roots['Label_same_roots']
df_avis['Label_no_puk'] = df_texte_nopuk['Label_no_puk']

path1=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien\le_parisien_avis.csv"
df_avis.to_csv(path1, index=False, header=True)