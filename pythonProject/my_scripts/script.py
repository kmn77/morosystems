from morosystems.pythonProject.src.confest import *


def test_1_google_to_morosystem(browser):
    print("0.1 - Otevření browseru a URL google.com")

    try:
        open_google_page(browser=browser, url="https://www.google.com/")

        cookie_accept(browser=browser)

        search_bar_find(browser=browser)

        search_bar_fill_input(browser=browser, find_text="MoroSystems")

        search_bar_accept_find(browser=browser)

        search_results(browser=browser)

        # GET morosystems.cz
        browser.get("https://www.morosystems.cz/")

        nav_kariera(browser)

    except:
        print("Něcose nepovedlo?")

    finally:
        tear_down(browser=browser)
