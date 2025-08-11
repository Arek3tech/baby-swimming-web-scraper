from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrapuj_copart_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    try:
        print(f"Ładowanie strony: {url}")
        driver.get(url)

        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        auta = soup.find_all('div', class_='search-results-row')

        wyniki = []
        for auto in auta:
            tytul_elem = auto.find('span', class_='lot-desc')
            tytul = tytul_elem.text.strip() if tytul_elem else 'Brak tytułu'

            cena_elem = auto.find('span', class_='currentBid') or auto.find('span', class_='auctionPrice')
            cena = cena_elem.text.strip() if cena_elem else 'Brak ceny'

            wyniki.append({'tytul': tytul, 'cena': cena})

        print("Znalezione aukcje:")
        for samochod in wyniki:
            print(f"Aukcja: {samochod['tytul']}, Cena: {samochod['cena']}")
        
        return wyniki

    finally:
        driver.quit()


if __name__ == "__main__":
    url = 'https://www.copart.com/lotSearchResults/?free=true&query=car'
    scrapuj_copart_selenium(url)
