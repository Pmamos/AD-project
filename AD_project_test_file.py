from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Uruchom Chrome w trybie headless

driver = webdriver.Chrome(options=chrome_options)  # Użyj ścieżki do sterownika, jeśli nie jest on zainstalowany w PATH
driver.get('https://www.worldometers.info/world-population/')
time.sleep(2)  # Czekaj na załadowanie strony
def get_population():
    population = driver.find_element(By.CSS_SELECTOR,'#maincounter-wrap > div > span').text
    return population

while True:
    print(get_population())
    time.sleep(2)

