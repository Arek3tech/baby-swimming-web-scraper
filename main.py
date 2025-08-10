from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def scrapuj_copart_selenium(url):
    # Opcje uruchomienia przeglądarki w tle (headless)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    # Inicjalizacja sterownika Chrome (upewnij się, że masz chromedriver)
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"Ładuje stronę: {url}")
        driver.get(url)

        # Poczekaj kilka sekund na załadowanie treści dynamicznej przez JavaScript
        time.sleep(5)

        # Pobierz źródło strony po załadowaniu JS
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Znajdź wszystkie elementy aukcji - divy z klasą 'search-results-row'
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
    # Przykładowy URL wyszukiwania aut na Copart
    url = 'https://www.copart.com/lotSearchResults/?free=true&query=car'
    scrapuj_copart_selenium(url)
