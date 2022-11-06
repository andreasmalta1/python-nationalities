import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import warnings
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance

warnings.filterwarnings("ignore")


def get_goals(url):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    driver = uc.Chrome(chrome_options=chrome_options)

    driver.get(url)

    source = driver.page_source
    driver.quit()
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
        df_goals.loc[i] = [nation[i], int(goals[i])]

    return df_goals


def team_colours(col):
    primary_colour = {
        "Argentina": "#43A1D5",
        "Nigeria": "#008751",
        "Denmark": "#C60C30",
        "Germany": "#000000",
        "Belgium": "#E30613",
        "France": "#21304D",
        "Portugal": "#E42518",
        "Norway": "#C8102E",
        "Brazil": "#FFDC02",
        "England": "#000040",
        "Spain": "#8B0D11",
        "Poland": "#DC143C",
        "Italy": "#0064AA",
        "Chile": "#0039A6",
        "Senegal": "#11A335",
        "Morocco": "#17A376",
        "Algeria": "#007229",
        "Canada": "#C5281C",
        "Suriname": "#377E3F",
        "Japan": "#000555",
        "Austria": "#ED2939",
        "Netherlands": "#F36C21",
        "Israel": "#0038B8",
        "Serbia": "#B72E3E",
        "Croatia": "#ED1C24",
        "Uruguay": "#55B5E5",
        "Republic of Ireland": "#169B62",
        "Wales": "#AE2630",
        "Scotland": "#004B84",
        "Colombia": "#FCD116",
        "Kosovo": "#244AA5",
        "Czech Republic": "#ED1B2C",
        "Switzerland": "#D52B1E",
        "Albania": "#E41E20",
        "Côte d'Ivoire": "#FF8200",
        "Mali": "#FCD116",
        "Cameroon": "#479A50",
        "Ghana": "#D40023",
        "Bosnia": "#002F6C",
        "Ukraine": "#FFD700",
        "Cameroon": "#479A50",
        "Turkey": "#E30A17",
        "Switzerland": "#FF0000",
        "Egypt": "#C8102E"}

    clr = []
    for team in col:
        if team in primary_colour:
            clr.append(primary_colour[team])
        else:
            print(team)
    return clr


def dict_conversion(country):
    countries = {'ar ARG': 'Argentina',
                'ng NGA': 'Nigeria',
                'dk DEN': 'Denmark',
                'de GER': 'Germany',
                'be BEL': 'Belgium',
                'fr FRA': 'France',
                'pt POR': 'Portugal',
                'no NOR': 'Norway',
                'br BRA': 'Brazil',
                'eng ENG': 'England',
                'es ESP': 'Spain',
                'pl POL': 'Poland',
                'it ITA': 'Italy',
                'cl CHI': 'Chile',
                'sn SEN': 'Senegal',
                'ma MAR': 'Morocco',
                'dz ALG': 'Algeria',
                'ca CAN': 'Canada' ,
                'sr SUR': 'Suriname',
                'jp JPN': 'Japan',
                'at AUT': 'Austria',
                'nl NED': 'Netherlands',
                'il ISR': 'Israel',
                'rs SRB': 'Serbia',
                'hr CRO': 'Croatia',
                'uy URU': 'Uruguay',
                'xk KVX': 'Kosovo',
                'ua UKR': 'Ukraine',
                'gh GHA': 'Ghana',
                'ba BIH': 'Bosnia',
                'cm CMR': 'Cameroon',
                'ch SUI': 'Switzerland',
                'eg EGY': 'Egypt'}
    return countries.get(country)


def nations_played(urls):
    df_total_times = pd.DataFrame(columns=['Nation','Min'])
    df_total_players = pd.DataFrame(columns=['Nation','# Players'])
    df_total_goals = pd.DataFrame(columns=['Nation','Goals'])
    df = pd.DataFrame()
    
    for url in urls:
        competition = urls[url]
        
        if competition == 'epl':
            comp_title = 'Premier League'
            goals_url = 'https://fbref.com/en/comps/9/shooting/Premier-League-Stats'
        if competition == 'laliga':
            comp_title = 'La Liga'
            goals_url = 'https://fbref.com/en/comps/12/shooting/La-Liga-Stats'
        if competition == 'bundesliga':
            comp_title = 'Bundesliga'
            goals_url = 'https://fbref.com/en/comps/20/shooting/Bundesliga-Stats'
        if competition == 'seriea':
            comp_title = 'Serie A'
            goals_url = 'https://fbref.com/en/comps/11/shooting/Serie-A-Stats'
        if competition == 'ligue1':
            comp_title = 'Ligue 1'
            goals_url = 'https://fbref.com/en/comps/13/shooting/Ligue-1-Stats'
        if competition == 'ucl':
            comp_title = 'Uefa Champions League'
            goals_url = 'https://fbref.com/en/comps/8/shooting/Champions-League-Stats'
        if competition == 'uel':
            comp_title = 'Uefa Europa League'
            goals_url = 'https://fbref.com/en/comps/19/2022/shooting/2022-Stats'


        html = pd.read_html(url, header=0)
        df = html[0]
        df = df.drop(['Rk', 'List'], axis=1)
        df["Nation"] = df["Nation"].str.split(" ", 1)

        drop_rows = []

        for index, row in df.iterrows():
            row["Nation"] = row["Nation"].pop()
            if row["# Players"] == "# Players":
                drop_rows.append(index)

        df = df.drop(labels=drop_rows)

        df["# Players"] = df["# Players"].astype(float)
        df["Min"] = df["Min"].astype(float)

        df_players = df.sort_values(by=["# Players"])
        df_players = df_players.drop(['Min'], axis=1)
        if competition != 'ucl' and competition != 'uel':
            df_total_players = pd.concat([df_total_players, df_players], ignore_index=True)
        
        df_players = df_players.tail(10)

        df_times = df
        df_times = df_times.dropna()
        df_times = df_times.sort_values(by=["Min"])
        df_times = df_times.drop(['# Players'], axis=1)
        if competition != 'ucl' and competition != 'uel':
            df_total_times = pd.concat([df_total_times, df_times], ignore_index=True)

        df_times = df_times.tail(10)
        
        fig = plt.figure(figsize=(20, 10))
        fig.subplots_adjust(hspace=0.5)
        gs = GridSpec(nrows=3, ncols=1)
        fig.suptitle(f'{comp_title} Nationalities', fontsize=22)
        fig.patch.set_facecolor('mediumpurple')
        
        ax0 = fig.add_subplot(gs[0, 0])
        bars = ax0.bar(df_players["Nation"], df_players["# Players"], color=team_colours(df_players["Nation"]), linewidth=10)
        ax0.bar_label(bars, size=16)
        ax0.set_title('Number of players from each nation (Top 10)', size=20)
        ax0.set_xlabel('Nations', size=16)
        ax0.set_ylabel('# of Players', size=16)
        ax0.set_facecolor('mediumpurple')
        for label in (ax0.get_xticklabels() + ax0.get_yticklabels()):
            label.set_fontsize(14)

        ax1 = fig.add_subplot(gs[1, 0])
        bars = ax1.bar(df_times["Nation"], df_times["Min"], color=team_colours(df_times["Nation"]), linewidth=10)
        ax1.bar_label(bars, size=16)
        ax1.set_title('Number of minutes played by nation (Top 10)', size=20)
        ax1.set_xlabel('Nations', size=16)
        ax1.set_ylabel('Minutes', size=16)
        ax1.set_facecolor('mediumpurple')
        for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
            label.set_fontsize(14)

        df = get_goals(goals_url)

        if competition != 'ucl' and competition != 'uel':
            df_total_goals = pd.concat([df_total_goals, df], ignore_index=True)

        df_sum = df.groupby('Nation')['Goals'].sum().reset_index()
        df_sum = df_sum.sort_values(by=['Goals'])
        df_sum = df_sum.tail(10)

        for i, row in df_sum.iterrows():
            country = dict_conversion(df_sum.at[i,'Nation'])
            if country:
                df_sum.at[i,'Nation'] = country

        ax2 = fig.add_subplot(gs[2, 0])
        bars = ax2.bar(df_sum["Nation"], df_sum["Goals"], color=team_colours(df_sum["Nation"]), linewidth=10)
        ax2.bar_label(bars, size=16)
        ax2.set_title('Number of goals scored from each nation (Top 10)', size=20)
        ax2.set_xlabel('Nations', size=16)
        ax2.set_ylabel('Goals', size=16)
        ax2.set_facecolor('mediumpurple')
        for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
            label.set_fontsize(14)

        # fig.savefig(f'images/{competition}-nations.png', transparent=True)
        fig.savefig(f'images/{competition}-nations.png')
        # if f'logo/{competition}.png' or f'logo/{competition}.jpg':
        #     img1 = Image.open('logos/epl (2).jpg')
        #     img2 = Image.open('images/epl-nations.png')
        #     img1.resize((2000, 1000))
        #     img1.paste(img2, (0,0), mask = img2)
        #     img1.save('hello2.png')
        
        # img1 = Image.open('images/epl-nations.png')
        # img2 = Image.open('logos/pl.png')
        # img1.paste(img2, (0,0), mask = img1)
        # img1.save('hello2.png')

        break

        # plt.show()

    fig = plt.figure(figsize=(20, 10))
    fig.subplots_adjust(hspace=0.5)
    gs = GridSpec(nrows=3, ncols=1)
    fig.suptitle(f'Top 5 Leagues Nationalities', fontsize=16)

    df_total_players = df_total_players.groupby('Nation', as_index=False).sum()
    df_total_players = df_total_players.sort_values(by=["# Players"])
    df_total_players = df_total_players.tail(10)
    
    ax0 = fig.add_subplot(gs[0, 0])
    bars = ax0.bar(df_total_players["Nation"], df_total_players["# Players"], color=team_colours(df_total_players["Nation"]))
    ax0.bar_label(bars)
    ax0.set_title('Number of players from each nation (Top 10)')
    ax0.set_xlabel('Nations')
    ax0.set_ylabel('# of Players')

    df_total_times = df_total_times.groupby('Nation', as_index=False).sum()
    df_total_times = df_total_times.sort_values(by=["Min"])
    df_total_times = df_total_times.tail(10)

    ax1 = fig.add_subplot(gs[1, 0])
    bars = ax1.bar(df_total_times["Nation"], df_total_times["Min"], color=team_colours(df_total_times["Nation"]))
    ax1.bar_label(bars)
    ax1.set_title('Minutes played from each nation (Top 10)')
    ax1.set_xlabel('Nations')
    ax1.set_ylabel('Minutes')

    df_total_goals = df_total_goals.groupby('Nation', as_index=False).sum()
    df_total_goals = df_total_goals.sort_values(by=["Goals"])
    df_total_goals = df_total_goals.tail(10)

    for i, row in df_total_goals.iterrows():
            country = dict_conversion(df_total_goals.at[i,'Nation'])
            if country:
                df_total_goals.at[i,'Nation'] = country

    ax2 = fig.add_subplot(gs[2, 0])
    bars = ax2.bar(df_total_goals["Nation"], df_total_goals["Goals"], color=team_colours(df_total_goals["Nation"]))
    ax2.bar_label(bars)
    ax2.set_title('Goals scored from each nation (Top 10)')
    ax2.set_xlabel('Nations')
    ax2.set_ylabel('Goals')
    
    fig.savefig(f'images/top-5-leagues-combined.png', transparent=True)
    # plt.show()


def main():
    pl_url = 'https://fbref.com/en/comps/9/nations/Premier-League-Nationalities'
    liga_url = 'https://fbref.com/en/comps/12/nations/La-Liga-Nationalities'
    bundesliga_url = 'https://fbref.com/en/comps/20/nations/Bundesliga-Nationalities'
    italy_url = 'https://fbref.com/en/comps/11/nations/Serie-A-Nationalities'
    french_url = 'https://fbref.com/en/comps/13/nations/Ligue-1-Nationalities'
    cl_url = 'https://fbref.com/en/comps/8/nations/Champions-League-Nationalities'
    uel_url = 'https://fbref.com/en/comps/19/2022/nations/2022-Nationalities'

    league_urls = {pl_url: 'epl',
                    liga_url: 'laliga',
                    bundesliga_url: 'bundesliga',
                    italy_url: 'seriea',
                    french_url: 'ligue1',
                    cl_url: 'ucl',
                    uel_url: 'uel'}
    
    nations_played(league_urls)


if __name__ == '__main__':
    main()

# Make text bold and slighlty bold
# Make only image in centre