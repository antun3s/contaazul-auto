#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

# Baixe o Chromedriver em: https://chromedriver.chromium.org/downloads
chromedriver = '/home/antunes/scripts/scripts-pessoais/contaazul-python/contaazul-selenium/chromedriver'
driver = webdriver.Chrome(chromedriver)

def contaazullogin():
    driver.get ('https://app.contaazul.com/auth/')
    driver.find_element_by_id('username_login').send_keys('login@suaempresa.com')
    driver.find_element_by_id ('password_login').send_keys('SuaSenha')
    driver.find_element_by_id('loginSubmit').click()
    
contaazullogin()
driver.get('https://app.contaazul.com/#/vendas-e-orcamentos')


# In[2]:


# Checa se existe notafiscal gerada
def checa_notafiscal():
    try:
        driver.find_element_by_xpath("//h5[@class='ng-binding'][contains(.,'Nota Fiscal emitida!')]")
        return(True)
    except NoSuchElementException:
        return(False)

checa_notafiscal()


# ### função enviar_email() desativada

# In[6]:

def enviar_email():
#    try:
#        driver.find_element_by_xpath("//a[contains(@data-text,'Enviar boleto por e-mail')]").click)()
#    except:
#        return(False)
#        
    sleep(1)
    driver.find_element_by_xpath("//a[contains(@data-text,'Enviar boleto por e-mail')]").click()
    sleep(1)
    driver.find_element_by_xpath("//button[contains(.,'Apenas enviar boleto')]").click()
    sleep(1)                     
# xPath "botão enviar email"  //a[contains(@data-text,'Enviar boleto por e-mail')]
# xPath "apenas enviar email" //button[contains(.,'Apenas enviar boleto')]


# Captura as URLs de todas as vendas e acessa cada uma delas
elementos = driver.find_elements_by_xpath("(//a[@class='ng-binding ng-scope'])")

url = []

for i in range(len(elementos)):
    # Armazena todas as URLs de vendas em na lista url
    url.append(elementos[i].get_attribute('href'))

for i in range(len(url)):
    driver.get(url[i])
    sleep(0.2)
    vendaid=driver.find_element_by_xpath('//span[contains(@class,"ng-binding ng-scope")]').text
    if vendaid != 'Gafra Supermercados Eireli':
        if not checa_notafiscal():
            print( vendaid,' - sem NFe emitida')
            enviar_email()
        else:
            print( vendaid,' - NFe emitida')
    


# In[4]:
