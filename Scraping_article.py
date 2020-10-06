from selenium import webdriver
<<<<<<< HEAD
from selenium.webdriver.chrome.options import Options
#import time
#import urllib , bs4

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium") 

driver = webdriver.Chrome(chrome_options=chrome_options)

=======
#import time

driver = webdriver.Chrome()
 
>>>>>>> ae8892a... scraping
driver.get("https://www.forbes.com/business")           

cl_element=driver.find_elements_by_class_name('headlink')

cl_list = []

for c in cl_element:
    cl_list.append(c.get_attribute('href'))                                             
driver.close()
article={}
<<<<<<< HEAD
article2={}

list_paragraphs = []
news_contents = []
=======
>>>>>>> ae8892a... scraping

for c in cl_list:
    driver = webdriver.Chrome()
    driver.get(c)
    title_element=driver.find_element_by_xpath('//*[@id="article-stream-0"]/div[2]/div[2]/div[1]/div/h1')
    title=title_element.text
    for i in range(1,50):
        try:
            txt_element=driver.find_element_by_xpath('//*[@id="article-stream-0"]/div[2]/div[2]/div[3]/div[1]/p['+str(i)+']')
            txt=txt_element.text
<<<<<<< HEAD
            list_paragraphs.append(txt)
            final_article = " ".join(list_paragraphs)
            article[i,c,title]=[txt]       
        except:
            pass
    news_contents.append(final_article)
    list_paragraphs = []
    driver.close()
driver.quit()   

=======
            article[i,c,title]=[txt]
        except:
            pass
    driver.close()
driver.quit()   
    
>>>>>>> ae8892a... scraping
