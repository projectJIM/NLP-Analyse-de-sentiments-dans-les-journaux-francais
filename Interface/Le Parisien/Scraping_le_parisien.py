##############################################################################################
############################### SCRAPING LE PARISIEN #########################################
##############################################################################################

################### Importation de package nécessaires: ##################################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#import time

#Nous utilisons les options de chrome pour ne pas avoir le problème de devoir accepter
# à chaque page les cookies du site.
#chrome_options = Options()
#chrome_options.add_argument("user-data-dir=selenium") 
#Les options sont sauvegardés. Il suffit de cliquer la première fois pour accepter les cookies.

##################################### Scraping ##############################################
cl_list = []

#Le scraping est réalisé en changeant de lien à chaque fois (pour chaque jour).
jour=["%.2d" % i for i in range(1,32)]
mois=["%.2d" % i for i in range(1,12)]
for m in mois:
    for j in jour: 
        try:
            chrome_options = Options()
            chrome_options.add_argument("user-data-dir=selenium") 
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get('https://www.leparisien.fr/archives/2020/'+j+'-'+m+'-2020/')
        except:
            pass
        for i in range(3,50):
                try:
                    c=driver.find_element_by_xpath('//*[@id="top"]/div['+str(i)+']/div/a')
                    cl_list.append(c.get_attribute('href')) 
                except:
                    pass
        driver.close()
driver.quit()

cl_list = list(dict.fromkeys(cl_list))
# cl_list contiendra les liens de tous les articles que nous allons scrapper.

#Ici seront scrappé les articles:
art_2021=[]
for lr in range(0,len(cl_list)-1):
    article=[]
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium") 
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(cl_list[lr])
    try:
        for sec in range(1,30):
            art=driver.find_elements_by_xpath('//*[@id="left"]/div[1]/div[2]/div[2]/section['+str(sec)+']/p')
            for el in art:
                ele=el.text
                article.append(ele)
        art_2021.append([article,cl_list[lr]])
    except:
        pass
    driver.close()

######################## Exportation des articles: ##################################

import pandas as pd    
le_parisien_2535=pd.DataFrame(art_2021)    

path=r"C:\Users\jovan\OneDrive\Radna površina\Paris 1\NLP_2\data\le_parisien2_2.csv"

le_parisien_2535.to_csv(path, index = False, header=True)
