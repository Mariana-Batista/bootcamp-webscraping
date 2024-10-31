import requests
import pandas as pd
from bs4 import BeautifulSoup

keyword = 'sabonete'

# Corrigindo a URL com interpolação de string
url = f"https://lista.mercadolivre.com.br/{keyword}"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    search_result = soup.find_all("div", class_="ui-search-result__content-wrapper")
      
    data = []
    
    for result in search_result:
        link = result.find("a", class_="ui-search-link")
        title = result.find("h2", class_="ui-search-item__title").text.strip()
        price = result.find("span", class_="andes-money-amount__fraction").text.strip()
        
        # Tentando extrair a marca de forma mais robusta
        brand_tag = result.find("span", class_="ui-search-item__group__element ui-search-item__brand")
        brand = brand_tag.text.strip() if brand_tag else "Marca não especificada"
        
        if link:
            link = link.get("href")
        
        data.append({"Title": title, "Price": price, "Brand": brand, "Link": link})
    
    # Criando um DataFrame com os dados coletados
    df = pd.DataFrame(data)
    print(df)
    
    df.to_csv("produtos.csv", index=False, encoding="utf-8")
    
else: 
    print('Erro ao acessar a página')
