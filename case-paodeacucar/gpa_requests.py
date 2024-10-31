import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import pandas as pd

class PaoAcucarScraper:
    
    def __init__(self):
        self.origin = 'https://www.paodeacucar.com'
        self.products = []
        self.api_key = 'paodeacucar'
        self.page = 1
        self.results_per_page = 12
        self.keyword = ''
        self.http = self._configure_session()
        
    def start(self, keyword):
        self.keyword = keyword
        content = self.search_product()
        product_data = self.get_product_data(content)
        if product_data:
            self.save_to_csv(product_data, f"{self.keyword}_products.csv")
        return product_data
        
    def _configure_session(self):
        retry_strategy = Retry(
            total=3,
            status_forcelist=[403, 429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def search_product(self):
        url = f'https://api.linximpulse.com/engage/search/v3/search?apikey={self.api_key}&origin={self.origin}&page={self.page}&resultsPerPage={self.results_per_page}&terms={self.keyword}&allowRedirect=true&salesChannel=461&salesChannel=catalogmkp&sortBy=relevance'

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        
        try: 
            content = self.http.get(url, headers=headers)
            if content.status_code == 200:
                return content.json()
            else:
                raise Exception(f"Request failed with status code: {content.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_product_data(self, content):
        if content:
            products = content.get("products", [])
            return products
        else:
            return []

    def save_to_csv(self, data, filename):
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Dados salvos em {filename}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")

keyword = 'sabonete'
scraper = PaoAcucarScraper()
data = scraper.start(keyword)
print(data)


