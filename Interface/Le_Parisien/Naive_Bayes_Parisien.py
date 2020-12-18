import pandas as pd
import nltk
#nltk.download()

#####################################################################################
######################### IMPORTATION DE DONNEES  ###################################
#####################################################################################
df=pd.read_csv('C:/Users/jovan/OneDrive/Radna površina/Paris 1/NLP_2/data/le_parisien/le_parisien_final.csv')

# Correction manuelle d'un article non-liée à LVMH
df['ident'][1112]='Non'
#df['ident'].value_counts()
#12 articles sur le groupe LVMH

df_avis=pd.read_csv('C:/Users/jovan/OneDrive/Radna površina/Paris 1/NLP_2/data/le_parisien/le_parisien_avis.csv')

#df_avis['Label_texte'][2][:110]

##################################################################################
#########################   NAIVE BAYES ESTIMATOR  ###############################
##################################################################################

################## CREATION LISTE POUR CHAQUE TYPE DE TEXTE ######################

#tx=['Label_texte','Label_no_sw','Label_same_roots','Label_no_puk']
def train(txt):
    t=[]  
    t1=df_avis[txt].tolist()
    t2=df_avis['Avis'].tolist()     
    import ast
    for i in range(len(t1)):
        t.append((ast.literal_eval(t1[i]),t2[i]))
    return t

input_texte=train('Label_texte')
input_no_sw=train('Label_no_sw')
input_same_roots=train('Label_same_roots')
input_no_puk=train('Label_no_puk')


############################# FONCTION CREATRICE DU BAYESIEN #########################

# Source d'inspiration: https://www.datatechnotes.com/2019/05/sentiment-classification-with-nltk.html

import random
#from sklearn.model_selection import KFold
#0.9*len(input_no_puk)
def bayes(input_tx,n=100,p=0.8):
    """ Il faut introduire dans la fonction le type de texte input_tx et le nombre de 
        repetitions n. p sera le pourcentage des données dédiés au train.  """
    all_acc=[]
    proba=[]
    for i in range(n):
        random.shuffle(input_tx) # va changer l'ordre dans train ce qui va permettre d'avoir un 
        # nouveau train et test ci-dessous.
        pourc=round(p*len(df_avis))
        train_x=input_tx[0:pourc]
        test_x=input_tx[pourc:len(input_tx)]
        
        model = nltk.NaiveBayesClassifier.train(train_x)
        acc=nltk.classify.accuracy(model, test_x)
#        print("Accuracy:", acc)
        all_acc.append(acc)

        # Pour avoir la probabilité associé aux choix du bayesien pour chaque article:
    for j in range(0,len(test_x)):
        prob_dist = model.prob_classify(test_x[j][0])
        proba.append([prob_dist.prob("positive"),prob_dist.prob("negative")])
        print("positive " + str(prob_dist.prob("positive")))
        print("negative " + str(prob_dist.prob("negative")))
    model.show_most_informative_features(n=20)
    return all_acc #,proba

###################### ENTRAINEMENT SUR DIFFERENTS TYPES DE TEXTES #######################

#Pour chaque type de texte, serait calculé dans l'odrde suivant: 
# - la précision sur 100 itérations
# - la probabilité associé aux décisions pour le dernière itération
# - la moyenne et l'ecart type de toutes les itérations

############## Avec le texte brut ###################

acc_texte,proba_texte=bayes(input_texte,100,p=0.85)  

moy_txt=sum(acc_texte)/len(acc_texte)
std_txt=sum((i - moy_txt) ** 2 for i in acc_texte) / len(acc_texte) 
print('La moyenne est:',moy_txt,"et l'ecart-type est:",std_txt)

############ Avec la ponctuation éliminés ##########################

acc_no_sw,proba_sw=bayes(input_no_sw,100,p=0.85)

moy_no_sw=sum(acc_no_sw)/len(acc_no_sw)
std_no_sw=sum((i - moy_no_sw) ** 2 for i in acc_no_sw) / len(acc_no_sw) 
print('La moyenne est:',moy_no_sw,"et l'ecart-type est:",std_no_sw)

############ Avec la source du mot ###################

acc_same_roots=bayes(input_same_roots,100,p=0.85)

moy_same_roots=sum(acc_same_roots)/len(acc_same_roots)
std_same_roots=sum((i - moy_same_roots) ** 2 for i in acc_same_roots) / len(acc_same_roots) 
print('La moyenne est:',moy_same_roots,"et l'ecart-type est:",std_same_roots)

############ Avec les stopwords et la ponctuation éliminés ############

acc_no_puk,proba_no_puk=bayes(input_no_puk,100,p=0.85)

moy_no_puk=sum(acc_no_puk)/len(acc_no_puk)
std_no_puk=sum((i - moy_no_puk) ** 2 for i in acc_no_puk) / len(acc_no_puk) 
print('La moyenne est:',moy_no_puk,"et l'ecart-type est:",std_no_puk)

########################### Matrice de confusion #######################################

from collections import defaultdict
def Matrice_confusion(input_tx,p=0.8):
    refsets = defaultdict(set)
    testsets = defaultdict(set)
    labels = []
    tests = []
    pourc=round(p*len(input_tx))
    model = nltk.NaiveBayesClassifier.train(input_tx[0:pourc])
    for i, (feats, label) in enumerate(input_tx[pourc:len(input_tx)]):
        refsets[label].add(i)
        observed = model.classify(feats)
        testsets[observed].add(i)
        labels.append(label)
        tests.append(observed)
    print(nltk.ConfusionMatrix(labels, tests))

random.shuffle(input_texte)
random.shuffle(input_no_sw)
random.shuffle(input_same_roots)
random.shuffle(input_no_puk)

Matrice_confusion(input_texte,p=0.85)
Matrice_confusion(input_no_sw,p=0.85)
Matrice_confusion(input_same_roots,p=0.85)
Matrice_confusion(input_no_puk,p=0.85)

############################################################################################
############################### DESCRIPTIF STAT ############################################
###########################################################################################

####################### Fréquence d'un mot dans un article ##############################

from nltk.probability import FreqDist
import matplotlib.pyplot as plt

def Freq_article(i,article):
    """ Compte la frequence d'apparition d'un mot dans un article """
    mots=list(df[article])
    l=mots[i].strip('][').split(', ')    
    fdist = FreqDist(l)
#    print(fdist)
    fdist.most_common(5)    
    fdist.plot(20,cumulative=False)
    plt.show()


# Les graphiques publiés sur le git
Freq_article(12892,'tokens')
Freq_article(12892,'tokens_no_sw')


######################### AVIS DE LA PHRASE OU DU MOT ###################################

# Une manière intéressante de tester le fonctionnement de notre bayesien est de lui faire 
# rentrer une phrase, un mot ou une expression et voir le sentiment qu'il attribue.
# Par exemple, "Bien" a un avis positif et "Mal" a un avis négatif.

def bayes_avis(input_tx,string):
    """ Pour une phrase quelconque retourne l'avis selon l'estimateur. """
    model = nltk.NaiveBayesClassifier.train(input_tx)
#    model.show_most_informative_features(15)
    exemple = string 
    t_features = {c:True for c in exemple.lower().split()}
    print(exemple," : ", model.classify(t_features)) 
    print("Probabilité sentiment positif: " + str(model.prob_classify(t_features).prob("positive")))
    print("Probabilité sentiment négatif: " + str(model.prob_classify(t_features).prob("negative")))

bayes_avis(input_no_sw,"Bien")
#Avis positif

bayes_avis(input_no_sw,"Mal")
#Avis négatif

bayes_avis(input_no_sw,"Pas si bien que ça")
# Ce genre d'expression montre la limite de notre classificateur. Il est plus dur d'associer
# des groupes de mots de signification parfois contre-intuitive lorsqu'on regarde les mots
# individuellement. C'est le cas d'expression ironique, d'oxymore... 
# Cet exemple montre aussi la limite de retirer de notre analyse les stopwords. Ils peuvent
# jouer un role important dans la détérmination du sens d'une phrase.


#########################################################################################
############################ Application de notre algorithme ############################
##########################################################################################
def bayes_appli(input_tx,tests):
    """ La fonction va classifier un article en positif ou negatif. Il faut choisir le
        type de texte traité. """
    all_ft=[]
    model = nltk.NaiveBayesClassifier.train(input_tx)
    res=[]
    for test in tests:
     t_features = {c:True for c in test.lower().split()}
     print(test," : ", model.classify(t_features)) 
     all_ft.append(model.classify(t_features))
     res.append([tests,model.classify(t_features)])
    return all_ft,res

# Nous allons appliquer notre fonction aux entreprise liées au groupe LVMH, pour en déduire
# si il reçoivent un traitement privilégier du journal Parisien:

tests_lvmh=df['texte'][df['ident']=='Oui'].tolist()

avis,res=bayes_appli(input_no_sw,tests_lvmh)

import pandas as pd 
pd.Series(avis).value_counts()

# Selon notre classificateur, des 12 articles sur les entreprises du groupe LVMH, 9 sont
# positifs et que 3 sont négatifs.
# Selon nous, après avoir observé les 12 articles, l'algorithme a fait une classification
#sans faille des articles.
# 1 article négatif et 1 article positif ne sont que des reportages de Radio Classique du 
#groupe LVMH, donc pas directement lié à l'image du groupe, mais bien classé. 2 articles 
#raportent des faits négatifs sur le groupe, touchant à des cas de poursuite judiciaire 
#sans fin. Finalement, tout les autres articles sont positifs, de manière assez prononcé, 
# et parlant d'action bénéfique du groupe sur la société.
 
# Dans cette exemple précis, notre classificateur a montré sa force en classifiant 
# parfaitement les articles.
