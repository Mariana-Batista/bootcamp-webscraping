import requests 

url = "http://lumtest.com/myip.json"
url2 = "http://www.globo.com"

response = requests.get(url2)

if response.status_code == 200:
    print(response.json())
    
else: 
    print("Erro")