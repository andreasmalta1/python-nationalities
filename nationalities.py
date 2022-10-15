import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random
import warnings

warnings.filterwarnings("ignore")


def show_plots():
    plt.savefig('my_plot.png')
    plt.show()


def plt_titles(plot_title, x_label, y_label):
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    show_plots()


def random_colour():
    clr = []
    for rnd in range(0, 10):
        r = random.random()
        b = random.random()
        g = random.random()
        each_clr = (r, b, g)
        clr.append(each_clr)
    return clr


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
        "Cameroon": "#479A50"}

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
                'xk KVX': 'Kosovo'}
    return countries.get(country)


def nations_played(urls):
    df_total_times = pd.DataFrame(columns=['Nation','Min'])
    df_total_players = pd.DataFrame(columns=['Nation','# Players'])
    df_total_goals = pd.DataFrame(columns=['Nation','Goals'])
    print(df_total_players)
    df = pd.DataFrame()
    
    for url in urls:
        competition = urls[url]

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
        if competition != 'ucl':
            df_total_players = pd.concat([df_total_players, df_players], ignore_index=True)
        
        df_players = df_players.tail(10)

        df_times = df
        df_times = df_times.dropna()
        df_times = df_times.sort_values(by=["Min"])
        df_times = df_times.drop(['# Players'], axis=1)
        if competition != 'ucl':
            df_total_times = pd.concat([df_total_times, df_times], ignore_index=True)

        df_times = df_times.tail(10)
        

        if competition == 'epl':
            comp_title = 'Premier League'
        if competition == 'laliga':
            comp_title = 'La Liga'
        if competition == 'bundesliga':
            comp_title = 'Bundesliga'
        if competition == 'seriea':
            comp_title = 'Serie A'
        if competition == 'ligue1':
            comp_title = 'Ligue 1'
        if competition == 'ucl':
            comp_title = 'Uefa Champions League'
        
        fig = plt.figure(figsize=(20, 10))
        fig.subplots_adjust(hspace=0.5)
        gs = GridSpec(nrows=3, ncols=1)
        fig.suptitle(f'{comp_title} Nationalities', fontsize=16)
        
        ax0 = fig.add_subplot(gs[0, 0])
        bars = ax0.bar(df_players["Nation"], df_players["# Players"], color=team_colours(df_players["Nation"]))
        ax0.bar_label(bars)
        ax0.set_title('Number of players from each nation (Top 10)')
        ax0.set_xlabel('Nations')
        ax0.set_ylabel('# of Players')

        ax1 = fig.add_subplot(gs[1, 0])
        bars = ax1.bar(df_times["Nation"], df_times["Min"], color=team_colours(df_times["Nation"]))
        ax1.bar_label(bars)
        ax1.set_title('Number of minutes played by nation (Top 10)')
        ax1.set_xlabel('Nations')
        ax1.set_ylabel('Minutes')

        goals_csv = f'goals_csvs/{competition}_goals.csv'
        df = pd.read_csv(goals_csv, usecols = [2, 8])
        df = df.rename(columns={'Nation': 'Nation', 'Gls': 'Goals'})
        df.drop(df[df['Goals'] <= 0].index, inplace = True)
        df = df.astype({'Goals':'int'})

        df_sum = df.groupby('Nation')['Goals'].sum().reset_index()
        df_sum = df_sum.sort_values(by=['Goals'])
        df_sum = df_sum.tail(10)

        for i, row in df_sum.iterrows():
            country = dict_conversion(df_sum.at[i,'Nation'])
            if country:
                df_sum.at[i,'Nation'] = country

        ax2 = fig.add_subplot(gs[2, 0])
        bars = ax2.bar(df_sum["Nation"], df_sum["Goals"], color=team_colours(df_sum["Nation"]))
        ax2.bar_label(bars)
        ax2.set_title('Number of goals scored from each nation (Top 10)')
        ax2.set_xlabel('Nations')
        ax2.set_ylabel('Goals')

        fig.savefig(f'images/{competition}-nations.png')
        # plt.show()
    
    df_total_players = df_total_players.groupby('Nation').sum()
    df_total_players = df_total_players.sort_values(by=["# Players"])
    # print(df_total_players)
    df_total_players = df_total_players.tail(10)
    # Iterate on rows

    fig = plt.figure(figsize=(20, 10))
    fig.subplots_adjust(hspace=0.5)
    gs = GridSpec(nrows=3, ncols=1)
    fig.suptitle(f'Top 5 Nationalities', fontsize=16)
    
    ax0 = fig.add_subplot(gs[0, 0])
    bars = ax0.bar(df_total_players["Nation"], df_total_players["# Players"], color=team_colours(df_total_players["Nation"]))
    ax0.bar_label(bars)
    ax0.set_title('Number of players from each nation (Top 10)')
    ax0.set_xlabel('Nations')
    ax0.set_ylabel('# of Players')
    plt.show()

# Combined top 5 leagues

def main():
    pl_url = 'https://fbref.com/en/comps/9/nations/Premier-League-Nationalities'
    liga_url = 'https://fbref.com/en/comps/12/nations/La-Liga-Nationalities'
    bundesliga_url = 'https://fbref.com/en/comps/20/nations/Bundesliga-Nationalities'
    italy_url = 'https://fbref.com/en/comps/11/nations/Serie-A-Nationalities'
    french_url = 'https://fbref.com/en/comps/13/nations/Ligue-1-Nationalities'
    cl_url = 'https://fbref.com/en/comps/8/nations/Champions-League-Nationalities'

    league_urls = {pl_url: 'epl',
                    liga_url: 'laliga',
                    bundesliga_url: 'bundesliga',
                    italy_url: 'seriea',
                    french_url: 'ligue1',
                    cl_url: 'ucl'}
    
    nations_played(league_urls)
    
    # nations_played(pl_url, 'epl')
    # nations_played(liga_url, 'laliga')
    # nations_played(bundesliga_url, 'bundesliga')
    # nations_played(italy_url, 'seriea')
    # nations_played(french_url, 'ligue1')
    # nations_played(cl_url, 'ucl')


main()