from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Lista krajów
countries = [
    "India", "China", "us", "Indonesia", "Pakistan", "Nigeria",
    "Brazil", "Bangladesh", "Russia", "Mexico", "Ethiopia", "Japan",
    "Philippines", "Egypt", "democratic-republic-of-the-congo", "Vietnam", "Iran", "Turkey",
    "Germany", "Thailand"
]

# Ustawienia opcji Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")

# Inicjalizacja przeglądarki
driver = webdriver.Chrome(options=chrome_options)

def get_population(country):
    url = f'https://www.worldometers.info/world-population/{country.lower()}-population/'
    driver.get(url)
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    try:
        # Czekaj na załadowanie elementu z populacją
        population_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#maincounter-wrap > div > span')
        ))
        population = population_element.text
    except Exception as e:
        print(f"Could not get population data for {country}: {e}")
        population = None
    return population

try:
    while True:
        for country in countries:
            population = get_population(country)
            if population:
                print(f"{country}: {population}")
        print('Sleeping for 5 minutes...')
        time.sleep(10)  # Czekaj 5 minut przed kolejną iteracją
except KeyboardInterrupt:
    pass
finally:
    driver.quit()