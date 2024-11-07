from selenium import webdriver
import pytest
import time
from selenium.webdriver.common.by import By

# @pytest.fixture(params=["chrome", "firefox", "edge"])

@pytest.fixture(params=["chrome", "firefox", "edge"])
def browser(request):
    browser_name = request.param
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()

    driver.maximize_window()
    driver.implicitly_wait(3)

    print("0.1 - Otevření browseru")

    # Quit
    yield driver
    driver.quit()

def open_google_page(browser, url):

    browser.get(url)
    # Kontrola že se stránka načetla podle URL/Tittle
    if "Google" not in browser.title and browser.current_url != "https://www.google.com":
        raise Exception("Stránka google.com se nenačetla! Spadlo na URL:", browser.current_url, "title je:",
                        browser.title)
    else:
        print("0.2 - Stránka se načetla v pořádku")

def cookie_accept(browser):
    # Odkliknutí cookies
    print("1. Odkliknutí cookies")

    # Najdi všechny <div> prvky s role="none" - jen řes text to nefunguje protože tam obsahují smluvní podmínky hledaný text
    elements = browser.find_elements(By.CSS_SELECTOR, 'div[role="none"]')

    cookies_accept_all_button = next((el for el in elements if "Přijmout vše" in el.text), None)

    if cookies_accept_all_button:
        highlight(cookies_accept_all_button, 3, "red", 5)
        cookies_accept_all_button.click()
    else:
        raise Exception("Nepodařilo se najít button 'Přijmout vše'")

    print("1. Odkliknutí cookies OK")

def search_bar_find(browser):
    # Najití search baru na google.com
    print("2. Najití search baru a click")
    time.sleep(1)

    google_search_bar_input_field = browser.find_element(By.XPATH, f"//*[@title='Hledat']")
    highlight(google_search_bar_input_field, 1, "red", 5)
    # Click na pole pro focus
    google_search_bar_input_field.click()

    print("2. Najití a kliknutí na search bar OK")

def search_bar_accept_find(browser):
    # Potvrzení vyhledávání
    print("4. Potvrzení vyhledávání")
    google_search_bar_input_approve = browser.find_element(By.XPATH,
                                                           "//input[@value='Hledat Googlem' and @aria-label='Hledat Googlem' and @name='btnK']")
    google_search_bar_input_approve.click()
    print("4. Potvrzení vyhledávání OK")

def search_bar_fill_input(browser, find_text):
    # Vložení textu od hledání
    print("3. Vyhledávání morosystems")
    google_search_bar_input_field = browser.find_element(By.XPATH, f"//*[@title='Hledat']")
    google_search_bar_input_field.send_keys(find_text)
    highlight(google_search_bar_input_field, 1, "red", 5)
    print("3. Vyhledávání", find_text, "OK")

def search_results(browser):
    # Ukázání výsledku
    print("5. Zobrazení výsledku")
    results = browser.find_elements(By.XPATH, f"//*[contains(text(), 'MoroSystems')]")

    for element in results:
        browser.execute_script("arguments[0].scrollIntoView();", element)
        highlight(element, 0.3, "red", 10)

    print("5. Zobrazení výsledku OK")


def nav_kariera(browser):
    # Proklik na "Kariéra"
    print("6. Proklik na 'Kariéra'")
    kariera = browser.find_element(By.CSS_SELECTOR, "#menu-hlavni-menu > li:nth-child(6) > a")
    highlight(kariera, 1, "red", 5)
    kariera.click()
    time.sleep(3)  # showcase
    print("6. Proklik na 'Kariéra' OK")


# Červený obrys elementu a blikající písmo
def highlight(element, effect_time, color, border):
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)

    original_style = element.get_attribute('style')

    # Přidání blikajícího efektu na písmo s rychlostí 10x za sekundu
    blink_style = (
        "border: {0}px solid {1}; "
        "color: red; "
        "animation: blink 0.1s steps(1, end) infinite; "  # Blikání 10x za sekundu
        "@keyframes blink {{"
        "0% {{ color: red; }} "
        "50% {{ color: transparent; }} "
        "100% {{ color: red; }} "
        "}}"
    ).format(border, color)

    apply_style(blink_style)
    time.sleep(effect_time)
    apply_style(original_style)

def tear_down(browser):
    print("Tear down in 1s (browser.quit)")
    time.sleep(1)
    browser.quit()
    print("Tear down DONE")