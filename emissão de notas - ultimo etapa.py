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


def emitirnota():
    sleep(2)
    driver.get('https://app.contaazul.com/#/vendas-e-orcamentos')

    sleep(2)
    #encontra o primeiro botão "emitir"
    botaoemitir = driver.find_element_by_xpath('(//a[contains(.,"Emitir")])[1]')
    botaoemitir.click()
    
    sleep(2)
    #retorna o nome do cliente
    nome = driver.find_element_by_xpath('//span[@ng-if="serviceInvoice.recipient.companyName"]')
    print(nome.text)
    
    #encontra o botão "Emitir Nota Fiscal"
    botaoemitirnotafiscal = driver.find_element_by_xpath('//a[contains(.,"Emitir Nota Fiscal")]')
    #print(type(botaoemitirnotafiscal))
    #print(botaoemitirnotafiscal.text)
    driver.execute_script("arguments[0].click();", botaoemitirnotafiscal)
    

#emitirnota()


# In[3]:


driver.get('https://app.contaazul.com/#/vendas-e-orcamentos')
sleep(2)
notasparaemitir = driver.find_elements_by_xpath('(//a[contains(.,"Emitir")])')
totaldenotas = int(len(notasparaemitir))
print(type(totaldenotas))
print(totaldenotas)

for i in range(0,totaldenotas):
    print('nota ' + str(i) + ' de ' + str(totaldenotas))
    emitirnota()
    
print('Finalizado!')

