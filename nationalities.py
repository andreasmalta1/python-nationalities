import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random


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
        "Arsenal": "#EF0107",
        "Aston Villa": "#95BFE5",
        "Brentford": "#E30613",
        "Brighton": "#0057B8",
        "Burnley": "#6C1D45",
        "Chelsea": "#034694",
        "Crystal Palace": "#1B458F",
        "Everton": "#003399",
        "Leeds United": "#FFCD00",
        "Leicester City": "#003090",
        "Liverpool": "#C8102E",
        "Manchester City": "#6CABDD",
        "Manchester Utd": "#DA291C",
        "Newcastle Utd": "#241F20",
        "Norwich City": "#FFF200",
        "Southampton": "#D71920",
        "Tottenham": "#132257",
        "Watford": "#FBEE23",
        "West Ham": "#7A263A",
        "Wolves": "#FDB913",
    }


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
                'ng NGA': 'Nigeria',
                'sr SUR': 'Suriname ',
                'jp JPN': 'Japan',
                'at AUT': 'Austria',
                'nl NED': 'Netherlands',
                'il ISR': 'Israel',
                'rs SRB': 'Serbia',
                'hr CRO': 'Croatia',
                'uy URU': 'Uruguay',
                'xk KVX': 'Kosovo'}
    return countries.get(country)


def nations_played(url, competition):
    html = pd.read_html(url, header=0)
    df = html[0]
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
    df_players = df_players.tail(10)

    df_times = df
    df_times = df_times.dropna()
    df_times = df_times.sort_values(by=["Min"])
    df_times = df_times.tail(10)

    fig = plt.figure(figsize=(20, 10))
    fig.subplots_adjust(hspace=0.5)
    gs = GridSpec(nrows=3, ncols=1)
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
    fig.suptitle(f'{comp_title} Nationalities', fontsize=16)
    
    ax0 = fig.add_subplot(gs[0, 0])
    bars = ax0.bar(df_players["Nation"], df_players["# Players"], color=random_colour())
    ax0.bar_label(bars)
    ax0.set_title('Number of players from each nation (Top 10)')
    ax0.set_xlabel('Nations')
    ax0.set_ylabel('# of Players')

    ax1 = fig.add_subplot(gs[1, 0])
    bars = ax1.bar(df_times["Nation"], df_times["Min"], color=random_colour())
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
    bars = ax2.bar(df_sum["Nation"], df_sum["Goals"], color=random_colour())
    ax2.bar_label(bars)
    ax2.set_title('Number of goals scored from each nation (Top 10)')
    ax2.set_xlabel('Nations')
    ax2.set_ylabel('Goals')

    fig.savefig(f'{competition}-nations.png')
    plt.show()  

# Combined top 5 leagues
# Add nation colours

def main():
    pl_url = 'https://fbref.com/en/comps/9/nations/Premier-League-Nationalities'
    liga_url = 'https://fbref.com/en/comps/12/nations/La-Liga-Nationalities'
    bundesliga_url = 'https://fbref.com/en/comps/20/nations/Bundesliga-Nationalities'
    italy_url = 'https://fbref.com/en/comps/11/nations/Serie-A-Nationalities'
    french_url = 'https://fbref.com/en/comps/13/nations/Ligue-1-Nationalities'
    cl_url = 'https://fbref.com/en/comps/8/nations/Champions-League-Nationalities'
    
    nations_played(pl_url, 'epl')
    nations_played(liga_url, 'laliga')
    nations_played(french_url, 'ligue1')
    nations_played(bundesliga_url, 'bundesliga')
    nations_played(italy_url, 'seriea')
    nations_played(cl_url, 'ucl')


main()