import urllib3
import requests
from requests_kerberos import HTTPKerberosAuth
from bs4 import BeautifulSoup

class HsdesApiHandler:

    def __init__(self, pem_path):
        self.pem_path = pem_path
        self.headers = {
            'Content-type': 'application/json',
        }
        self.base_url = 'https://hsdes-api.intel.com/rest/'

    @staticmethod
    def remove_html_tags(description):
        soup = BeautifulSoup(description, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()
        return ' '.join(soup.stripped_strings)

    def get_data(self, url_suffix):
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url = self.base_url + url_suffix 
            print("URL: ",url)
           # https://hsdes-api.intel.com/rest/query/16019102685?include_text_fields=Y&start_at=1&max_results=400
            response =requests.get(url,verify=self.pem_path,auth=HTTPKerberosAuth(), headers=self.headers)       
                
            return response.json()
    
    def run_query_by_id(self, query_id):
        return self.get_data(f'query/{query_id}?include_text_fields=Y&start_at=1&max_results=400')
    
    def get_article_data(self,url):
         urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
         response =requests.get(url,verify=self.pem_path,auth=HTTPKerberosAuth(), headers=self.headers)
         return response.json()
