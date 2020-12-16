# NLP
Présentation et Description du Projet

Problématique : À l'aide d’un langage de programmation, comment peut-on savoir si un article de presse est positif sur le sujet traité ? 

Présentation du projet :

L’objectif de ce projet est d’analyser de nombreux articles de presse français, et suite à un traitement de texte élaboré sur le logiciel Python-Spider, de pouvoir définir si ces articles sont positifs (ou négatifs) à propos du sujet décrit par les auteurs dans leurs différents articles.

En amont, nous avons sélectionné deux sites de presse française, « Le Monde » ainsi que « Le Parisien ». Pour le premier, ont été sélectionnées seulement quelques catégories spécifiques afin de bien répondre à notre problématique, la section réservée aux articles sur les entreprises, et celle réservée à l’économie française et internationale. 

Pour le site du Parisien, nous avons créé une grande base de données depuis les articles de janvier 2020 jusqu’à ceux d’aujourd’hui sur toutes les catégories possibles.
Ainsi la base de données du site “Le Parisien” pour le projet de traitement de texte est constituée de plus de 13000 articles avec toutes les catégories. On retrouvera pour chaque article scrappé le texte complet, son lien vers le site de presse, sa catégorie, sa date de parution sur le site et son titre. 

De manière plus précise, ce projet a pour but d’analyser le sentiment de l’article sélectionné, en essayant de savoir si son contenu est positif ou négatif sur le sujet décrit.
Par exemple, dans un premier temps, le projet devait se centrer exclusivement sur les articles en lien avec les entreprises ou qui gravitent autour des thèmes tel que l’économie française ou l’économie internationale. Le programme devait donc déterminer si un article quelconque, publié sur le site du Monde, était positif, c’est-à-dire qu’il présentait l’entreprise avec des adjectifs qualificatifs positifs … En conséquence, le programme retourne la valeur “True” si l’article analysé est positif pour l’entreprise, et par opposition, il retourne “False” si l’article est négatif pour l’entreprise. On peut ainsi conclure qu’un article de presse peut agir comme une mauvaise publicité pour certains groupes ou au contraire un vecteur positif qui permet de gagner en visibilité sur les réseaux et plateformes numériques. 

Pour aller plus loin dans le projet, nous avons aussi décidé d’extraire, si cela est possible, le PDG de l’entreprise décrite et sa localisation géographique. De plus, nous voulons aussi savoir si l’entreprise a un potentiel lien économique (ou financier) avec le journal, c'est-à-dire que l’entreprise à des parts de marché dans le journal. 
Dans le cas du journal “Le Parisien”, l’actionnaire majoritaire est Bernard Arnault, et son entreprise LVMH détient à 100% le groupe de presse “Le Parisien”. Pour “Le Monde” on dénombre trois actionnaires majoritaires, Xavier Niel le fondateur d'Iliad, maison mère de Free, Matthieu Pigasse et le tchèque Daniel Kretinsky.

Ci-dessous, les deux liens nous dressent la situation actuelle pour tous les organes de presse français afin de savoir quelles entreprises ou personnes sont actionnaires (majoritaires / minoritaires) dans un organe de presse. 

Lien de l’article : https://www.monde-diplomatique.fr/cartes/PPA
Lien du Git : https://github.com/mdiplo/Medias_francais

On a aussi rajouté dans nos dataframes finales la variable “résumé” qui permet d’afficher avec seulement 20% du texte traité les grandes lignes de l’article.

