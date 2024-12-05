import asyncio

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

class Function:
    @staticmethod
    def check_domain(domain):

        p = sync_playwright().start()  
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            if not domain.startswith(('http://', 'https://')):
                domain = 'http://' + domain

            response = page.goto(domain, wait_until='domcontentloaded')
            status_code = response.status
            has_content = bool(page.content())
            has_content = 1 if has_content else 0
            country = response.headers.get('geo-country', 'Unknown')

        except Exception as e:
            print(f"erro {e}")
            status_code = None
            has_content = 0
            country = 'Unknown'

        finally:
            browser.close()
            p.stop()  

        return status_code, has_content, country

    @staticmethod
    async def check_domain_async(domain):
        async with async_playwright() as p:  
            browser = await p.chromium.launch()
            page = await browser.new_page()

            try:
                if not domain.startswith(('http://', 'https://')):
                    domain = 'http://' + domain

                response = await page.goto(domain, wait_until='domcontentloaded')
                status_code = response.status
                has_content = bool(await page.content())
                has_content = 1 if has_content else 0
                country = response.headers.get('geo-country', 'Unknown')

            except Exception as e:
                print(f"Erro: {e}")
                status_code = None
                has_content = 0
                country = 'Unknown'

            finally:
                await browser.close()

        return status_code, has_content, country
    

domain = 'marvelrivals.com'

async def test_function(domain):

    assincrona = await Function.check_domain_async(domain)

    print (f"Função assincrona: {assincrona}")

    return assincrona

