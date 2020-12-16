# NLP

## Présentation et Description du Projet

Problématique : À l'aide d’un langage de programmation, comment peut-on savoir si un article de presse est positif sur le sujet traité ? 

# Présentation du projet :

L’objectif de ce projet est d’analyser de nombreux articles de presse français, et suite à un traitement de texte élaboré sur le logiciel Python-Spider, de pouvoir définir si ces articles sont positifs (ou négatifs) à propos du sujet décrit par les auteurs dans leurs différents articles.

En amont, nous avons sélectionné deux sites de presse française, « Le Monde » ainsi que « Le Parisien ». Pour le premier, ont été sélectionnées seulement quelques catégories spécifiques afin de bien répondre à notre problématique, la section réservée aux articles sur les entreprises, et celle réservée à l’économie française et internationale. 

Pour le site du Parisien, nous avons créé une grande base de données depuis les articles de janvier 2020 jusqu’à ceux d’aujourd’hui sur toutes les catégories possibles.
Ainsi la base de données du site “Le Parisien” pour le projet de traitement de texte est constituée de plus de 13000 articles avec toutes les catégories. On retrouvera pour chaque article scrappé le texte complet, son lien vers le site de presse, sa catégorie, sa date de parution sur le site et son titre. 

De manière plus précise, ce projet a pour but d’analyser le sentiment de l’article sélectionné, en essayant de savoir si son contenu est positif ou négatif sur le sujet décrit.
Par exemple, dans un premier temps, le projet devait se centrer exclusivement sur les articles en lien avec les entreprises ou qui gravitent autour des thèmes tel que l’économie française ou l’économie internationale. Le programme devait donc déterminer si un article quelconque, publié sur le site du Monde, était positif, c’est-à-dire qu’il représentait l’entreprise avec des adjectifs élogieux … En conséquence, le programme retourne la valeur “True” si l’article analysé est positif pour l’entreprise, et par opposition, il retourne “False” si l’article est négatif pour l’entreprise. On peut ainsi conclure qu’un article de presse peut agir comme une mauvaise publicité pour certains groupes ou au contraire un vecteur positif qui permet de gagner en visibilité sur les réseaux et plateformes numériques. 

Pour aller plus loin dans le projet, nous avons aussi décidé d’extraire, si cela est possible, le PDG de l’entreprise décrite et sa localisation géographique. De plus, nous voulons aussi savoir si l’entreprise a un potentiel lien économique (ou financier) avec le journal, c'est-à-dire que l’entreprise à des parts de marché dans le journal. 
Dans le cas du journal “Le Parisien”, l’actionnaire majoritaire est Bernard Arnault, et son entreprise LVMH détient à 100% le groupe de presse “Le Parisien”. Pour “Le Monde” on dénombre trois actionnaires majoritaires, Xavier Niel le fondateur d'Iliad, maison mère de Free, Matthieu Pigasse et le tchèque Daniel Kretinsky.

Ci-dessous, les deux liens nous dressent la situation actuelle pour tous les organes de presse français afin de savoir quelles entreprises ou personnes sont actionnaires (majoritaires / minoritaires) dans un organe de presse. 

Lien de l’article : https://www.monde-diplomatique.fr/cartes/PPA

On a aussi rajouté dans nos dataframes finales la variable “résumé” qui permet d’afficher avec seulement 20% du texte traité les grandes lignes de l’article.

## L'estimateur de Bayes 

Le Naive Bayes Estimator, ou estimateur naïf de Bayes, permet une classification binaire des articles. Si on considère deux classes 0 et 1, il est basé sur le calcul de la probabilité d’appartenir à la classe 1 (article positif) ou 0 (article négatif). 
Dans notre cas, le décompte des mots permet de calculer cette probabilité. Chaque mot représente une variable explicative qui est soit présente, soit absente de l’article. 

Supposons que pour une base de données d'entraînement, les classes sont indiquées. Nous allons chercher alors à combien de fois un mot (ponctuation incluse) apparaît dans les articles positifs et combien de fois il apparait aussi dans les articles négatifs. Ainsi, nous pouvons calculer la probabilité qu’un nouvel article soit positif ou négatif en fonction des mots apparaissant dans cet article, et en fonction de la fréquence d'apparition de ces mots dans les articles de notre base d'entraînement. 

Le package nltk.NaiveBayesClassifier permet de faire exactement ce calcul. Les mots inconnus par la base d'entraînement apparaissant dans les nouveaux articles sont ignorés dans nos calculs. Ceci montre l’importance de fournir un grand nombre d'articles d'entraînement, pour couvrir un vocabulaire important, mais aussi pour éviter un biais. Le biais peut intervenir par exemple, avec trop peu d’articles, sur les expressions de type “pas trop mal” qui sont dans un article positif, mais qui pourrait finir par associer le mot “mal” à un article positif.
C’est aussi une des limites de cette méthode, les expressions ironiques ou autres plus subtiles ne peuvent pas être comprises par cet algorithme simple.
L’avantage principal de cet algorithme est sa simplicité et sa facile interprétation: un article est positif s' il contient plus de mots d’articles entraînés positifs que négatifs.

Nous allons tester quatre variations d’inputs possibles de cet algorithme et comparer leurs performances:
 - les articles non-modifiés ;
 - les articles dont les “stopwords”, ou mots vides, sans importances pour le sentiment, ont été enlevés ;
 - les articles où la ponctuation a été enlevé;
 - les articles où uniquement la source du mot a été préservée.

