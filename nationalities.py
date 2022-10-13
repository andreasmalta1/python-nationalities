import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random

# figure(figsize=(8, 6), dpi=80)


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


def nations_played(url):
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
    
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.bar(df_players["Nation"], df_players["# Players"], color=random_colour())
    for index, value in enumerate(df_times['# Players']):
        plt.text(index - 0.1, value + 1, value)
    ax0.set_title('Number of players from each nation (Top 10)')
    ax0.set_xlabel('Nations')
    ax0.set_ylabel('# of Players')

    ax1 = fig.add_subplot(gs[1, 0])
    ax1.bar(df_times["Nation"], df_times["Min"], color=random_colour())
    for index, value in enumerate(df_times['Min']):
        plt.text(index - 0.1, value + 1, value)
    ax1.set_title('Number of minutes played by nation (Top 10)')
    ax1.set_xlabel('Nations')
    ax1.set_ylabel('Minutes')

    fig.savefig('full_figure.png')
    plt.show()
    



# get goals data():
def nations_goals():
    goals_csv = 'epl_goals.csv'
    df = pd.read_csv(goals_csv, usecols = [2, 8])
    df = df.rename(columns={'Nation': 'Nation', 'Gls▼': 'Goals'})
    df.drop(df[df['Goals'] <= 0].index, inplace = True)
    df = df.astype({'Goals':'int'})

    df_sum = df.groupby('Nation')['Goals'].sum().reset_index()
    df_sum = df_sum.sort_values(by=['Goals'])
    df_sum = df_sum.tail(10)

    plt.bar(df_sum["Nation"], df_sum["Goals"])
    for index, value in enumerate(df_sum['Goals']):
        plt.text(index - 0.1, value + 1, value)
    plt_titles("Number of goals scored from each nation (Top 10)", "Nations", "# of Players")
    


# Nationailties represented in PL by mins
# Nationailties represented in PL by # players
# Order of nationalities by goals scored in PL

# Nationailties represented in UCL by mins
# Nationailties represented in UCL by # players
# Order of nationalities by goals scored in PL

def main():
    pl_url = 'https://fbref.com/en/comps/9/nations/Premier-League-Nationalities'
    nations_played(pl_url)
    cl_url = 'https://fbref.com/en/comps/8/nations/Champions-League-Nationalities'
    # nations_played(cl_url)


main()