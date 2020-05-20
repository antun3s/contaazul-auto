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


# Checa se já existe boleto gerado para a venda
def checa_boleto():
    try:
        driver.find_element_by_xpath('//*[@id="statementHasAttachment_0"]')
        return(True)
    except NoSuchElementException:
        return(False)
# checa_boleto()


# In[3]:


# Checa se o valor pago é igual ao valor da venda
def checa_pago():
    try:
        valor = driver.find_element_by_id('negotiationTotalValueLabel')
        recebido = driver.find_element_by_id('statementsSummaryPaid')
        if valor.text == recebido.text:
            return(True)
        else:
            return(False)
    except NoSuchElementException:
        return(False)
# checa_pago()


# In[4]:


# Checa se existe notafiscal gerada
def checa_notafiscal():
    try:
        driver.find_element_by_xpath("//h5[@class='ng-binding'][contains(.,'Nota Fiscal emitida!')]")
        return(True)
    except NoSuchElementException:
        return(False)

# checa_notafiscal()


# In[10]:


def gera_remessa():
    driver.implicitly_wait(1) # seconds
    
    # boleto
    driver.find_element_by_xpath('//*[@id="btnStatementGenerateBankslip_0"]').click()
    print('Clique no boleto')
    sleep(2)
    #driver.find_element_by_xpath('//button[contains(@data-text,"Imprimir boleto")']).click()

    # sicoob
    sleep(0.9)
    driver.find_element_by_xpath("//ng-transclude[contains(.,'Sicoob')]").click()
    print('Clique no Sicoob')
    
    # seguinte
    sleep(0.9)
    driver.find_element_by_xpath("//button[contains(.,'Seguinte')]").click()
    print('Clique no Seguinte')
    
    # apenas download
    sleep(1.5)
    driver.find_element_by_xpath("//button[contains(.,'Apenas download do boleto')]").click()
    print('Clique no Apenas download do boleto')
    
    # cancelar
    sleep(1)
    driver.find_element_by_xpath("//button[contains(.,'Cancelar')]").click()
    print('Clique no Cancelar')
    
    # voltar
    sleep(1)
    driver.find_element_by_xpath("//ul[@id='breadcrumb']/li[2]/a").click()


# ## Captura as URLs de todas as vendas e acessa cada uma delas
# ### função gerar_remessa() desativada

# In[11]:


# Captura as URLs de todas as vendas e acessa cada uma delas
elementos = driver.find_elements_by_xpath("(//a[@class='ng-binding ng-scope'])")

url = []

for i in range(len(elementos)):
    # Armazena todas as URLs de vendas em na lista url
    url.append(elementos[i].get_attribute('href'))

#print(url)

for i in range(len(url)):
    driver.get(url[i])
    sleep(0.5)
    vendaid=driver.find_element_by_xpath('//span[contains(@class,"ng-binding ng-scope")]').text
    print(vendaid)
    if vendaid != 'Gafra Supermercados Eireli':
        if not checa_notafiscal():
            print( vendaid,' - sem NFe emitida')
            if not checa_boleto():
                print(vendaid, '- sem boleto')
                gera_remessa()
                print(vendaid, '- boleto gerado')
            else:
                print(vendaid, '- com boleto')
        else:
            print( vendaid,' - NFe emitida')