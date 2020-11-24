import tkinter
import pandas as pd


df=pd.read_csv("C:/Users/idel/Desktop/M2/Python/le_parisien2_traitement.csv")
dc=pd.read_csv("C:/Users/idel/Desktop/M2/Python/le_Monde_traitement.csv")
dc_bis=pd.read_csv("C:/Users/idel/Desktop/M2/Python/Eco_lemonde_traitement.csv")


#InterFAce Graphique


#Article Le Parisien

listTitreParisien=df['Titre']
listArticleParisien=df['Texte']
dictionnaireParisien = dict()
 
for x in listTitreParisien:
     for y in listArticleParisien:
        dictionnaireParisien[x] = y



#Article Le Monde secteur entreprise
listTitre=dc['Titre']
listArticle=dc['TexteOriginal']
dictionnaire = dict()
 
for x in listTitre:
     for y in listArticle:
        dictionnaire[x] = y

#Article Le Monde Tous les secteurs

listTitreMondeBis=dc_bis['Titre']
listArticleMondeBis=dc_bis['TexteOriginal']
dictionnaireMondeBis = dict()
 
for x in listTitreMondeBis:
     for y in listArticleMondeBis:
        dictionnaireMondeBis[x] = y





fenetre=tkinter.Tk()   


#Importation des Images
parisien = tkinter.PhotoImage(file="C:\\Users\\idel\\Desktop\\M2\\Python\\Le_Parisien_logo.png")
leMonde = tkinter.PhotoImage(file="C:\\Users\\idel\\Desktop\\M2\\Python\\Logo-le-monde.png")


def ArticleLemonde():  
    
    top= tkinter.Toplevel(fenetre)
    top.geometry("1200x700") #Taille de la fenetre
    cadre1 = tkinter.Frame(top)      #Creation d'une fenêtre sur la gauche de l'ecran qui va permettre l'affichage des différentes licences au sein du domaine sélectionné
    cadre1.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)
    cadre2= tkinter.Frame(top)       #Creation d'une fenêtre sur la droite de l'ecran qui va permettre l'affichage des différentes universités proposant ses formations
    cadre2.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH,expand=True)
       
        
    entry = tkinter.Entry(top,width=120)
    result = entry.get()    #Result récupère le texte entré par l'utilisateur
    
    entry.pack(padx=1,pady=1)     #Affichage de la zone de recherche

    
    mylist = tkinter.Listbox(cadre1)      #Creation d'une listBox à gauche qui va contenir les formations
    mylist2 = tkinter.Text(cadre2)
    
    
    #Affichage de la clé du dictionnaire , qui correspond au nom des formations en lien avec le domaine choisi par l'utilisateur  
    for cle in dictionnaire.keys():
        mylist.insert(tkinter.END,cle)
    
    def articleAffichage():
        result = str(entry.get())
        
        
        #Partie analyse
        mask = (dc['Titre']==result)
        dc2=dc[mask]
        maliste=list()
        entreprise = ('\n\n' + 'Entreprise : ' + str(dc2.iloc[0,9]))
        pdg = ('PDG :' + str(dc2.iloc[0,10]))
        positive = ('Texte positive : ' + str(dc2.iloc[0,8]))
        localisation = ('Localisation Precise : ' + str(dc2.iloc[0,12]))
    
        maliste=[entreprise,'\n',pdg,'\n',positive,'\n',localisation]
        
        
        mylist2.insert(tkinter.END,dictionnaire[result])
        
        mylist2.insert(tkinter.END,maliste)    
        
    def efface():
        mylist2.delete(1.0,tkinter.END)
        entry.delete(0, tkinter.END)
           
    
    mylist.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)   #Affichage de la listbox
    mylist2.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH,expand=True)  #Affichage de la listbox
    
    tkinter.Label(cadre1,text="Entrer un article (Faire un Ctrl+c et Ctrl+v) : ").pack(padx=0,pady=0)
    tkinter.Button(top,text="Entrer ",command=articleAffichage).pack(padx=1,pady=0)
    tkinter.Button(top,text="Effacer ",command=efface).pack(padx=2,pady=0)

    
def ArticleLeParisien():  
    
    top= tkinter.Toplevel(fenetre)
    top.geometry("1200x700") #Taille de la fenetre
    cadre1 = tkinter.Frame(top)      #Creation d'une fenêtre sur la gauche de l'ecran qui va permettre l'affichage des différentes licences au sein du domaine sélectionné
    cadre1.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)
    cadre2= tkinter.Frame(top)       #Creation d'une fenêtre sur la droite de l'ecran qui va permettre l'affichage des différentes universités proposant ses formations
    cadre2.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH,expand=True)
       
        
    entry = tkinter.Entry(top,width=120)
    result = entry.get()    #Result récupère le texte entré par l'utilisateur
    
    entry.pack(padx=1,pady=1)     #Affichage de la zone de recherche

    
    mylist = tkinter.Listbox(cadre1)      #Creation d'une listBox à gauche qui va contenir les formations
    mylist2 = tkinter.Text(cadre2)
    
    
    #Affichage de la clé du dictionnaire , qui correspond au nom des formations en lien avec le domaine choisi par l'utilisateur  
    for cle in dictionnaireParisien.keys():
        mylist.insert(tkinter.END,cle)
    
    def articleAffichage():
        result = str(entry.get())
        
        #Partie analyse
        mask = (df['Titre']==result)
        df2=df[mask]
        maliste=list()
        entreprise = ('\n\n' + 'Entreprise : ' + str(df2.iloc[0,7]))
        pdg = ('PDG :' + str(df2.iloc[0,8]))
        positive = ('Texte positive : ' + str(df2.iloc[0,6]))
        localisation = ('Localisation Precise : ' + str(df2.iloc[0,10]))
    
        maliste=[entreprise,'\n',pdg,'\n',positive,'\n',localisation]    
        
        mylist2.insert(tkinter.END,dictionnaireParisien[result])
        
        mylist2.insert(tkinter.END,maliste)
        
    def efface():
        mylist2.delete(1.0,tkinter.END)
        entry.delete(0, tkinter.END)
           
    
    mylist.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)   #Affichage de la listbox
    mylist2.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH,expand=True)  #Affichage de la listbox
    
    tkinter.Label(cadre1,text="Entrer un article (Faire un Ctrl+c et Ctrl+v) : ").pack(padx=0,pady=0)
    tkinter.Button(top,text="Entrer ",command=articleAffichage).pack(padx=1,pady=0)
    tkinter.Button(top,text="Effacer ",command=efface).pack(padx=2,pady=0)    


def ArticleLemondeGeneral():
    top= tkinter.Toplevel(fenetre)
    top.geometry("1200x700") #Taille de la fenetre
    cadre1 = tkinter.Frame(top)      #Creation d'une fenêtre sur la gauche de l'ecran qui va permettre l'affichage des différentes licences au sein du domaine sélectionné
    cadre1.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)
    cadre2= tkinter.Frame(top)       #Creation d'une fenêtre sur la droite de l'ecran qui va permettre l'affichage des différentes universités proposant ses formations
    cadre2.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH,expand=True)
       
        
    entry = tkinter.Entry(top,width=120)
    result = entry.get()    #Result récupère le texte entré par l'utilisateur
    
    entry.pack(padx=1,pady=1)     #Affichage de la zone de recherche

    
    mylist = tkinter.Listbox(cadre1)      #Creation d'une listBox à gauche qui va contenir les formations
    mylist2 = tkinter.Text(cadre2)
    
    
    #Affichage de la clé du dictionnaire , qui correspond au nom des formations en lien avec le domaine choisi par l'utilisateur  
    for cle in dictionnaireMondeBis.keys():
        mylist.insert(tkinter.END,cle)
    
    def articleAffichage():
        result = str(entry.get())
        
        
        #Partie analyse
        mask = (dc_bis['Titre']==result)
        dc2=dc_bis[mask]
        maliste=list()
        entreprise = ('\n\n' + 'Entreprise : ' + str(dc2.iloc[0,9]))
        pdg = ('PDG :' + str(dc2.iloc[0,10]))
        positive = ('Texte positive : ' + str(dc2.iloc[0,8]))
        localisation = ('Localisation Precise : ' + str(dc2.iloc[0,12]))
    
        maliste=[entreprise,'\n',pdg,'\n',positive,'\n',localisation]
        
        
        mylist2.insert(tkinter.END,dictionnaireMondeBis[result])
        
        mylist2.insert(tkinter.END,maliste)    
        
    def efface():
        mylist2.delete(1.0,tkinter.END)
        entry.delete(0, tkinter.END)
           
    
    mylist.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)   #Affichage de la listbox
    mylist2.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH,expand=True)  #Affichage de la listbox
    
    tkinter.Label(cadre1,text="Entrer un article (Faire un Ctrl+c et Ctrl+v) : ").pack(padx=0,pady=0)
    tkinter.Button(top,text="Entrer ",command=articleAffichage).pack(padx=1,pady=0)
    tkinter.Button(top,text="Effacer ",command=efface).pack(padx=2,pady=0)
    

#Button Interface d'acceuil
tkinter.Button(fenetre,text="Article Le Monde Secteur Entreprise",font='Helvetica 13 bold',height = 4, width = 30,command=ArticleLemonde).pack(padx=1,pady=1)
tkinter.Button(fenetre,text="Article Le Parisien ",font='Helvetica 13 bold',height = 4, width = 30,command=ArticleLeParisien).pack(padx=1,pady=10)
tkinter.Button(fenetre,text="Article Le Monde (général) ",font='Helvetica 13 bold',height = 4, width = 30,command=ArticleLemondeGeneral).pack(padx=1,pady=10)



#Canvas permettant l'affichage de toutes les images
c = tkinter.Canvas(fenetre,width=200,height=200,bg ='white')

#Affichage de toutes les images sur l'ecran de démarrage de l'application
c.create_image(300, 100, image=parisien)
c.create_image(1200, 100, image=leMonde)
c.pack(side=tkinter.LEFT,expand=True,fill=tkinter.X)

#On relie les onglets à notre fenêtre principale
m = tkinter.Menu(fenetre)

#Creation des onglets
sm1 = tkinter.Menu(fenetre)
   
#Creation des onglets
m.add_cascade (label = "Quitter", menu = sm1)
   

#Lien entre les fenetres et les onglets
#Chaque sous menu present dans chaque onglets renvoi vers sa fenêtre respective comme défini préalablement

sm1.add_command(label="Quitter", command=fenetre.destroy)

   #Parametre de la fenetre
fenetre.geometry("1200x700") #Taille de la fenetre
fenetre.title("NLP M2-TIDE") #Titre de la fenetre
fenetre.config(menu = m) #Lancement avec tous les onglets config avant
fenetre.mainloop() #Lancement de la fenetre

