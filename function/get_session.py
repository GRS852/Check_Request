import aiohttp
import requests
import asyncio

from bs4 import BeautifulSoup


class FunctionGet:

    @staticmethod
    async def check_domain_async(domain):

        async with aiohttp.ClientSession() as session:

            keywords = ["this domain is for sale", 
                        "this domain has recently been registered with namecheap",
                        "registre seu domínio hoje mesmo"]
            try:

                if not domain.startswith(('http://', 'https://')):
                    domain = 'http://' + domain

 
                async with session.get(domain) as response:

                    status = response.status
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    page_text = soup.get_text().lower()
                    has_content = bool(content)
                    has_content = 1 if has_content else 0
                    country = response.headers.get('geo-country', 'Unknown')

                    if any (keyword in page_text for keyword in keywords):
                        return 999, 0, 'Unknown'
                    
            except Exception as e:
                print(f"Erro: {e}")
                status = 999
                has_content = 0
                country = 'Unknown'


        return status, has_content, country
    
    def check_domain(domain):

        keywords = ["this domain is for sale", 
                    "this domain has recently been registered with namecheap",
                    "registre seu domínio hoje mesmo"]
    
        try:
            if not domain.startswith(('http://', 'https://')):
                domain = 'http://' + domain

            response = requests.get(domain)

            status = response.status_code
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            page_text = soup.get_text().lower()
            has_content = 1 if content else 0
            country = response.headers.get('geo-country', 'Unknown')

            if any(keyword in page_text for keyword in keywords):
                return 999, 0, 'Unknown'

        except Exception as e:
            print(f"Erro: {e}")
            status = 999
            has_content = 0
            country = 'Unknown'

        return status, has_content, country
        
