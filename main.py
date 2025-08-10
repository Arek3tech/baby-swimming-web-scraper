# main.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrapuj_copart_selenium(url):
    # Opcje uruchomienia Chrome w trybie headless (bez GUI)
    options = Options()
    options.add_argument('--headless')      # tryb bez interfejsu
    options.add_argument('--disable-gpu')   # wyłącz GPU
    options.add_argument('--no-sandbox')    # sandbox wyłączony, potrzebne dla GitHub Actions i niektórych środowisk

    # Inicjalizacja sterownika Chrome z automatycznym pobieraniem chromedriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    try:
        print(f"Ładowanie strony: {url}")
        driver.get(url)

        # Poczekaj na załadowanie treści dynamicznej (JavaScript)
        time.sleep(5)

        # Pobierz kompletny HTML po załadowaniu treści
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Znajdź div'y z aukcjami o klasie 'search-results-row'
        auta = soup.find_all('div', class_='search-results-row')

        wyniki = []
        for auto in auta:
            # Tytuł aukcji: zwykle marka + model
            tytul_elem = auto.find('span', class_='lot-desc')
            tytul = tytul_elem.text.strip() if tytul_elem else 'Brak tytułu'

            # Cena wywoławcza (lub aktualna oferta)
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
    # Przykładowy URL wyników aukcji na Copart
    url = 'https://www.copart.com/lotSearchResults/?free=true&query=car'
    scrapuj_copart_selenium(url)
