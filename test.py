import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd


def main():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    driver = uc.Chrome(chrome_options=chrome_options)

    driver.get('https://fbref.com/en/comps/9/shooting/Premier-League-Stats')

    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')

    rows = soup.find("table", id='stats_shooting').find("tbody").find_all("tr")

    df_goals = pd.DataFrame(columns=['Nation', 'Goals'])
    nation = []
    goals = []

    for row in rows:
        cells = row.find_all("td")
        if cells:
            nation.append(cells[1].get_text())
            goals.append(cells[7].get_text())

    for i in range(len(goals)):
        df_goals.loc[i] = [nation[i], goals[i]]

    print(df_goals)
            

if __name__ == '__main__':
    main()

# Currenlty
# france 176
