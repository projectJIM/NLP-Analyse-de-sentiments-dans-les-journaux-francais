# Analyse de sentiments dans les journaux français

## Présentation et Description du Projet NLP

![Le Parisien](https://github.com/projectJIM/NLP/blob/main/Interface/Le_Parisien/Le_Parisien_logo.png?raw=true) 

![Monde](https://github.com/projectJIM/NLP/blob/main/Interface/Le_Monde/Logo-le-monde.png?raw=true) 

Problématique de départ : À l'aide d’un langage de programmation, comment peut-on savoir si un article de presse est positif ou négatif sur le sujet traité ? 

# Présentation du projet :

L’objectif de ce projet est d’analyser de nombreux articles de presse français, et suite à un traitement de texte élaboré sur le logiciel Python-Spider, de pouvoir définir si ces articles sont positifs (ou négatifs) à propos du sujet décrit par les auteurs dans leurs différents articles.

En amont, nous avons sélectionné deux sites de presse française, « Le Monde » ainsi que « Le Parisien ». Pour le premier, ont été sélectionnées seulement quelques catégories spécifiques afin de bien répondre à notre problématique, la section réservée aux articles sur les entreprises, et celle réservée à l’économie française et internationale. 
(Voir **article_LeMonde.py**)

Pour le site du Parisien, nous avons créé une grande base de données depuis les articles de janvier 2020 jusqu’à ceux d’aujourd’hui sur toutes les catégories possibles.
Ainsi la base de données du site “Le Parisien” pour le projet de traitement de texte est constituée de plus de 13000 articles avec toutes les catégories. On retrouvera pour chaque article scrappé le texte complet, son lien vers le site de presse, sa catégorie, sa date de parution sur le site et son titre. (Voir **Scraping_le_parisien.py**) 

De manière plus précise, ce projet a pour but d’analyser le sentiment de l’article sélectionné, en essayant de savoir si son contenu est positif ou négatif sur le sujet décrit.
Par exemple, dans un premier temps, le projet devait se centrer exclusivement sur les articles en lien avec les entreprises ou qui gravitent autour des thèmes tel que l’économie française ou l’économie internationale. Le programme devait donc déterminer si un article quelconque, publié sur le site du Monde, était positif, c’est-à-dire qu’il représentait l’entreprise avec des adjectifs élogieux . En conséquence, le programme retourne la valeur “True” si l’article analysé est positif pour l’entreprise, et par opposition, il retourne “False” si l’article est négatif pour l’entreprise. On peut ainsi conclure qu’un article de presse peut agir comme une mauvaise publicité pour certains groupes ou au contraire un vecteur positif qui permet de gagner en visibilité sur les réseaux et plateformes numériques. 

Pour aller plus loin dans le projet, nous avons aussi décidé d’extraire, si cela est possible, le PDG de l’entreprise décrite et sa localisation géographique. De plus, nous voulons aussi savoir si l’entreprise a un potentiel lien économique (ou financier) avec le journal, c'est-à-dire que l’entreprise à des parts de marché dans le journal. 
Dans le cas du journal “Le Parisien”, l’actionnaire majoritaire est Bernard Arnault, et son entreprise LVMH détient à 100% le groupe de presse “Le Parisien”. Pour “Le Monde” on dénombre trois actionnaires majoritaires, Xavier Niel le fondateur d'Iliad, maison mère de Free, Matthieu Pigasse et le tchèque Daniel Kretinsky. (Voir **traitement_Parisien.py**) (Voir **traitement_article_Lemonde_Generale.py**)

Ci-dessous, le lien nous dresse la situation actuelle pour tous les organes de presse français afin de savoir quelles entreprises ou personnes sont actionnaires (majoritaires / minoritaires) dans un organe de presse. Nous ferons à la fin une analyse des articles du Parisien sur le groupe LVMH.

Lien de l’article : https://www.monde-diplomatique.fr/cartes/PPA

On a aussi rajouté dans nos dataframes finales la variable “résumé” qui permet d’afficher avec seulement 20% du texte traité les grandes lignes de l’article.

## Traitement de texte 

Nous avons utilisé le package NLTK pour faire plusieurs variantes de textes qui seront utilisé plus tard dans l'analyse: sans les mots vides, la ponctuation ou tout en cherchant la source du mot. 
De plus, dans cette partie nous avons identifier si un article contenait ou pas mention d'une entreprise proche du journal, dans ce cas Le Parisien, donc une entreprise faisant partie du groupe LVMH. Ceci a été fait à l'aide du package spaCy. (Voir **NLP_Parisien.py**)

Voici deux graphiques qui illustrent l'importance de cette étape. Le premier représente la fréquence d'apparition de mots dans un article du Parisien non traité, et le deuxième montre la fréquence dans le cas ou les mots vides ont été enlevé.  
\mettre image avec le decompte du mots des differents types de textes

La différence est significative. Dans le premier cas, les mots qui auront un poids plus important dans de nombreuses analyses (par exemple dans l'estimateur Bayesien - voir la partie suivante) sont des mots relativement insignifiant. Dans le deuxième cas, ces mots vides sont mis à l'écart et la thématique de l'article peut être déduit en regardant uniquement ce graphique de fréquence. Or, les stopwords (mots vides) ont une signification, voir par exemple le test fait à la fin de la partie suivante.

## L'estimateur de Bayes 

Le Naive Bayes Estimator, ou estimateur naïf de Bayes, permet une classification binaire des articles. Si on considère deux classes 0 et 1, il est basé sur le calcul de la probabilité d’appartenir à la classe 1 (article positif) ou 0 (article négatif). 
Dans notre cas, le décompte des mots permet de calculer cette probabilité. Chaque mot représente une variable explicative qui est soit présente, soit absente de l’article et sur lequel on a une opinion préalable positive ou négative. 

Comment cette opinion préalable au test est-elle construite? Supposons que pour une base de données d'entraînement, les classes sont indiquées. Nous allons chercher alors combien de fois un mot (ponctuation incluse) apparaît dans les articles positifs et combien de fois il apparait aussi dans les articles négatifs. Ainsi, nous pouvons calculer la probabilité qu’un nouvel article soit positif ou négatif en fonction des mots apparaissant dans cet article, et en fonction de leur fréquence d'apparition dans les articles pré-classifiés de notre base d'entraînement. 

Notre échantillon d'entrainement est constitué de 158 articles, à qui ont a attribué un label positif/négatif. Mais en fait, nous avont quatre échantillons d'entrainements possibles, qui représente les mêmes articles mais peuvent nous conduire à des résultats différents. (Voir **Naive_Bayes_Parisien.py**)
Nous allons donc tester quatre variations d’inputs possibles de cet estimateur et comparer leurs performances:
 - les articles non-modifiés ;
 - les articles où la ponctuation a été enlevé;
 - les articles dont les “stopwords”, ou mots vides, sans importances pour le sentiment, ont été enlevés (ainsi que la ponctuation) ;
 - les articles où uniquement la source du mot a été préservée.
 Après avoir dédié 85% à notre partie train et les 15 % restant au test et répété 100 fois leur répartition aléatoire, nous avons une moyenne des résultats suivants:
 
 Type de texte|Précision             |Ecart-type 
--------------|----------            |---
Texte normal| 0.7333            | 0.0052
Texte sans ponctuation| 0.7287  | 0.0065
Texte sans mots vides| 0.7229   | 0.0079
Texte avec source du mot| 0.7241| 0.0068

On observe que la précision du classifieur est très proche en fonction de la méthode choisie. Mais ces résultats nous montre une tendance: plus le traitement du texte est lourd, donc plus on change le texte (par exemple en enlevant la ponctuation et les mots vides - type 3) plus notre classifieur sera instable. Or, notre échantillon n'est pas grand, donc l'instabilité peut provenir de ce fait aussi. Finalement, le texte brut a eu la meilleure performance d'après ces paramètres. Voyons un deuxième indicateur informateur de nos résultats, la matrice de confusion:

Texte Normal  |Positif | Négatif            
--------------|----------|-------            
Positif|   <7>    |      3
Négatif|   4   | <10>

Texte sans ponctuation  |Positif | Négatif            
--------------|----------|-------            
Positif|   <10>    |      3
Negatif|   4    | <7>

Texte sans mots vides  |Positif | Négatif            
--------------|----------|-------            
Positif|   <9>    |      4
Négatif|   5    | <6>

Texte avec source du mot  |Positif | Négatif            
--------------|----------|-------            
Positif|   <10>    |      1
Négatif|   6    | <7>

(en ligne = label de référence; en colonne = label test)

Ceci n'est qu'un exemple, et la matrice de confusion change en reprenant les calcus. Parmi les 24 articles dans notre base test, on observe que dans chaque instance, il y a en général plus de faux négatifs que de faux positifs. L'estimateur peut donc avoir tendance de mettre un label positif plus facilement qu'il ne le devrait avoir. Or, il faut savoir que notre base train-test contenait initialement plus d'articles négatif, ce qui est certainement un facteur qui a eu une influence sur ces résultats. 

Le package nltk.NaiveBayesClassifier nous a permis de faire ces calculs. Les mots inconnus par la base d'entraînement et apparaissant dans les nouveaux articles (test) sont ignorés dans les calculs de probabilité. Ceci montre l’importance de fournir un grand nombre d'articles d'entraînement, pour couvrir un vocabulaire important, mais aussi pour éviter un biais. Le biais peut intervenir par exemple, avec trop peu d’articles, sur les expressions de type “pas trop mal” qui sont dans un article positif, mais qui pourrait finir par associer le mot “mal” à un article positif.

Nous avons réaliser un test simple de notre classifieur qui exclut les mots vides, en reprenant trois expressions commune qui peuvent apparaitre dans un texte et nous avons eu les résultats suivants: (le code se trouve dans la partie "Avis de la phrase ou du mot" de **Naive_Bayes_Parisien.py**)

Expression  |Avis           
--------------|----------            
"Bien"|   Positif (proba de 51.5 vs 0.485)   
"Mal" |   Négatif   (proba de 0.499 vs 0.501)
"Pas si bien que ça" |   Positif (0.588 vs 0.411)

Sachant que nous avons utilisé le classifieur sans mots vides, le résultat n'est pas satisfaisant. "Mal" a apparament apparu que dans un peu plus d'article négatif que positif,
et la troisième expression, négative, est accéptée comme positive de 8%.
Donc on observe que c'est une des limites de cette méthode, les expressions ironiques ou autres, plus subtiles, ne peuvent pas être comprises par cet algorithme simple.

L’avantage principal de cet algorithme est sa simplicité et sa facile interprétation: un article est positif s'il contient plus de mots d’articles entraînés positifs que négatifs.
 
 ## Application et limites 
 
 Finalement, nous allons appliquer notre classifieur aux articles des entreprise liées au groupe LVMH, pour en déduire si elles reçoivent un traitement privilégier du journal Parisien. Malheureusement, il n'y a que 12 articles dans notre base de données qui remplissent ce critère, donc toute conclusion sur le traitement privilégier sera limité sur ces articles. (Voir fin de **Naive_Bayes_Parisien.py**)
 
 Selon notre classifieur, des 12 articles sur les entreprises du groupe LVMH, 9 sont positifs et que 3 sont négatifs. Après avoir observé les 12 articles, selon nous, la classification est sans faille: tout les articles ont été bien labelisé. 
 Or, un article négatif et un article positif ne sont que des reportages de "Radio Classique" du groupe LVMH, donc pas directement lié à l'image du groupe, mais tout autant bien classé. 2 articles en effet raportent des faits négatifs sur le groupe, touchant à des cas de poursuite judiciaire sans fin contre des dirigeants. Finalement, tout les autres articles sont positifs, de manière assez prononcé, en parlant surtout d'action bénéfique du groupe sur la société.
 
Dans cette exemple précis, notre classificateur a montré sa force en classifiant parfaitement les articles. Mais pour faires des analyses sérieuses sur des sujets sensibles tel que la question de la propagande médiatique, il faudra avoir une base beaucoup plus grande.

 
 #### Brèche
 
 Le scraping des articles à l’aide de beautifulsoup nous a permis de récupérer l’ensemble des articles et a révélé une faille dans le système des articles réservés aux abonnés. En effet, tous les sites de presse française ont une section réservée pour leurs abonnés et notre programme permet de contourner ce système en lisant le contenu de l'article directement sur le logiciel de programmation ou dans les cases du fichier Excel de notre base de données préparée.
