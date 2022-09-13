import pandas as pd
import matplotlib.pyplot as plt
import random
import requests
from bs4 import BeautifulSoup, Comment

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


def show_plots():
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    """plt.show(block=False)
    plt.pause(2)
    plt.close()"""
    plt.show()


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

    clr = []

    for team in col:
        if team in primary_colour:
            clr.append(primary_colour[team])
        else:
            print(team)
    return clr


def secondary_team_colours(col):
    secondary_colour = {
        "Arsenal": "#9C824A",
        "Aston Villa": "#670e36",
        "Brentford": "#140E0C",
        "Brighton": "#FFCD00",
        "Burnley": "#99D6EA",
        "Chelsea": "#6A7AB5",
        "Crystal Palace": "#C4122E",
        "Everton": "#FFFFFF",
        "Leeds United": "#1D428A",
        "Leicester City": "#FDBE11",
        "Liverpool": "#00B2A9",
        "Manchester City": "#1C2C5B",
        "Manchester Utd": "#FBE122",
        "Newcastle Utd": "#41B6E6",
        "Norwich City": "#00A650",
        "Southampton": "#FFC20E",
        "Tottenham": "#FFFFFF",
        "Watford": "#ED2127",
        "West Ham": "#1BB1E7",
        "Wolves": "#231F20",
    }
    clr = []

    for team in col:
        if team in secondary_colour:
            clr.append(secondary_colour[team])
        else:
            print(team)
    return clr


def random_colour():
    clr = []
    for rnd in range(0, 20):
        r = random.random()
        b = random.random()
        g = random.random()
        each_clr = (r, b, g)
        clr.append(each_clr)
    return clr


def plt_titles(plot_title, x_label, y_label):
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    show_plots()


def sort_data_frame(df, col, indent, title, x, y, pct):
    df = df.sort_values(by=[col])
    plt.barh(df["Squad"], df[col], color=team_colours(df["Squad"]))
    if not pct:
        for index, value in enumerate(df[col]):
            plt.text(value + indent, index, str(value))
    else:
        for index, value in enumerate(df[col]):
            plt.text(value + indent, index, str(value) + "%")

    plt_titles(title, x, y)


def sort_data_frame_players(df, col, indent, title, x, y, pct):
    df[col] = df[col].astype(float)
    int_check = True
    for index, row in df.iterrows():
        if not row[col].is_integer():
            int_check = False
            break

    if int_check is True:
        df[col] = df[col].astype(int)

    df = df.sort_values(by=[col])
    plt.barh(df["Player"], df[col], color=team_colours(df["Squad"]))
    if not pct:
        for index, value in enumerate(df[col]):
            plt.text(value + indent, index, str(value))
    else:
        for index, value in enumerate(df[col]):
            plt.text(value + indent, index, str(value) + "%")

    plt_titles(title, x, y)


def sort_data_frame_zeroes(df, col, indent, title, x, y, pct):
    df = df.sort_values(by=[col])
    plt.barh(df["Squad"], df[col], color=team_colours(df["Squad"]))
    if not pct:
        for index, value in enumerate(df[col]):
            if value != 0:
                plt.text(value + indent, index, str(value))
    else:
        for index, value in enumerate(df[col]):
            if value != 0:
                plt.text(value + indent, index, str(value) + "%")

    plt_titles(title, x, y)
    
    
def sort_data_frame_zeroes_players(df, col, indent, title, x, y, pct):
    df[col] = df[col].astype(float)
    int_check = True
    for index, row in df.iterrows():
        if not row[col].is_integer():
            int_check = False
            break

    if int_check is True:
        df[col] = df[col].astype(int)

    df = df.sort_values(by=[col])
    plt.barh(df["Player"], df[col], color=team_colours(df["Squad"]))
    if not pct:
        for index, value in enumerate(df[col]):
            if value != 0:
                plt.text(value + indent, index, str(value))
    else:
        for index, value in enumerate(df[col]):
            if value != 0:
                plt.text(value + indent, index, str(value) + "%")

    plt_titles(title, x, y)


def sort_data_frame_negatives(df, col, indent_positive, indent_negative, title, x, y, pct):
    df = df.sort_values(by=[col])
    plt.barh(df["Squad"], df[col], color=team_colours(df["Squad"]))
    if not pct:
        for index, value in enumerate(df[col]):
            if value > 0:
                plt.text(value + indent_positive, index, str(value))
            if value < 0:
                plt.text(value - indent_negative, index, str(value))
    else:
        for index, value in enumerate(df[col]):
            if value > 0:
                plt.text(value + indent_positive, index, str(value) + "%")
            if value < 0:
                plt.text(value - indent_negative, index, str(value) + "%")

    plt_titles(title, x, y)


def sort_data_frame_negatives_players(df, col, indent_positive, indent_negative, title, x, y, pct):
    df[col] = df[col].astype(float)
    int_check = True
    for index, row in df.iterrows():
        if not row[col].is_integer():
            int_check = False
            break

    if int_check is True:
        df[col] = df[col].astype(int)

    df = df.sort_values(by=[col])
    plt.barh(df["Player"], df[col], color=team_colours(df["Squad"]))
    if not pct:
        for index, value in enumerate(df[col]):
            if value > 0:
                plt.text(value + indent_positive, index, str(value))
            if value < 0:
                plt.text(value - indent_negative, index, str(value))
    else:
        for index, value in enumerate(df[col]):
            if value > 0:
                plt.text(value + indent_positive, index, str(value) + "%")
            if value < 0:
                plt.text(value - indent_negative, index, str(value) + "%")

    plt_titles(title, x, y)


def nations():
    url = "https://fbref.com/en/comps/9/nations/Premier-League-Nationalities"
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
    df_players = df_players.tail(5)

    df_times = df
    df_times = df_times.dropna()
    df_times = df_times.sort_values(by=["Min"])
    df_times = df_times.tail(5)

    plt.bar(df_players["Nation"], df_players["# Players"])
    plt_titles("Number of players from each nation (Top 5)", "Nations", "# of Players")

    plt.bar(df_times["Nation"], df_times["Min"])
    plt_titles("Number of minutes played by nation (Top 5)", "Nations", "Minutes")


def general_team():
    url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    html = pd.read_html(url, header=1)
    df = html[0]

    sort_data_frame(df, "# Pl", 0.4, "Number of players used", "# Players", "Teams", False)

    poss_a = []
    col_for = "Poss"
    col_against = "Possession Against"
    df = df.sort_values(by=[col_for])
    for index, row in df.iterrows():
        poss_a.append(round(100 - row[col_for], 1))
    df[col_against] = poss_a
    df[col_against] = df[col_against].astype(float)
    df[col_for] = df[col_for].astype(float)

    labels = df["Squad"]
    poss_against = (df[col_against]) * -1
    poss_for = df[col_for]

    fig, ax = plt.subplots()

    ax.barh(labels, poss_against, label="Possession Against", color=secondary_team_colours(df["Squad"]))
    ax.barh(labels, poss_for, label="Possession For", color=team_colours(df["Squad"]))

    ax.set_ylabel("Teams")
    ax.set_title("Possession Against vs Possession For")

    for index, value in enumerate(df[col_for]):
        plt.text(value / 2, index - 0.1, str(value))
    for index, value in enumerate(df[col_against]):
        plt.text((value * -0.5), index - 0.1, str(value))

    show_plots()

    sort_data_frame_zeroes(df, "Gls", 0.4, "Goals Scored", "# Assists", "Teams", False)
    sort_data_frame_zeroes(df, "Ast", 0.4, "Assists Provided", "# Assists", "Teams", False)

    assist_per_goal = []
    for index, row in df.iterrows():
        assist_per_goal.append(round((row["Ast"] / row["Gls"]) * 100))
    df["Ast/Gls"] = assist_per_goal
    sort_data_frame(df, "Ast/Gls", 0.4, "% Assists provided per goals", "% Assists/Goals", "Teams", True)

    sort_data_frame(df, "G-PK", 0.4, "Non-Penalty Goals Scored", "# Goals", "Teams", False)
    sort_data_frame_zeroes(df, "PKatt", 0.05, "Penalties Awarded", "# Penalties", "Teams", False)
    sort_data_frame_zeroes(df, "PK", 0.05, "Penalties Scored", "# Goals", "Teams", False)

    pens_scored_ratio = []
    for index, row in df.iterrows():
        if row["PKatt"] != 0:
            if row["PK"] > 0:
                pens_scored_ratio.append(round((row["PK"] / row["PKatt"]) * 100))
            else:
                pens_scored_ratio.append(row["PKatt"] / 1000)
        else:
            pens_scored_ratio.append(0)
    col = "Pen Rt"
    df[col] = pens_scored_ratio
    df = df.sort_values(by=[col])
    plt.barh(df["Squad"], df[col], color=team_colours(df["Squad"]))
    col_index = df.columns.get_loc("PKatt")
    for index, value in enumerate(df[col]):
        if 0 < value < 1:
            plt.text(0.25, index, "Missed " + str(df.iat[index, col_index]) + " pen(s)")
        else:
            if value > 0:
                plt.text(value + 0.4, index, str(value) + "%")

    plt_titles("% of Pens scored", "% Pen", "Teams")

    goal_pen_ratio = []
    for index, row in df.iterrows():
        goal_pen_ratio.append(round((row["G-PK"] / row["Gls"]) * 100))
    df["GPKratio"] = goal_pen_ratio
    sort_data_frame(df, "GPKratio", 0.4, "% of goals from non-penalties", "% Goals", "Teams", True)

    sort_data_frame_zeroes(df, "CrdY", 0.4, "Number of Yellow Cards", "# Yellow Cards", "Teams", False)
    sort_data_frame_zeroes(df, "CrdR", 0.005, "Number of Red Cards", "# Red Cards", "Teams", False)
    sort_data_frame(df, "xG", 0.4, "Expected Goals", "xG", "Teams", False)

    over_under = []
    for index, row in df.iterrows():
        over_under.append(round((row["Gls"] - row["xG"]), 2))
    df["OP"] = over_under
    sort_data_frame_negatives(df, "OP", 0.2, 0.4, "Over-Performance", "# Goals", "Teams", False)


def keeping_teams():
    url = "https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats"
    html = pd.read_html(url, header=1)
    df = html[0]

    sort_data_frame_zeroes(df, "GA", 0.4, "Goals conceded", "# Goals", "Teams", False)
    sort_data_frame_zeroes(df, "PKA", 0.1, "Penalty goals conceded", "# Goals", "Teams", False)
    sort_data_frame_zeroes(df, "FK", 0.02, "Free kick goals conceded", "# Goals", "Teams", False)
    sort_data_frame_zeroes(df, "CK", 0.1, "Corner kick goals conceded", "# Goals", "Teams", False)
    sort_data_frame_zeroes(df, "OG", 0.02, "Own goals conceded", "# Goals", "Teams", False)
    sort_data_frame(df, "PSxG", 0.02, "Expected goals from shots", "xG", "Teams", False)
    sort_data_frame(df, "PSxG/SoT", 0.005, "Expected goals from Shot on Target", "Goals/Shot", "Teams", False)
    sort_data_frame_negatives(df, "PSxG+/-", 0.1, 0.3, "xG Difference", "# Expected Goals Difference", "Teams", False)
    sort_data_frame(df, "Att.1", 2, "Attempted GK passes", "Passes", "Teams", False)
    sort_data_frame(df, "Thr", 1, "Number of GK throws", "Throws", "Teams", False)
    sort_data_frame(df, "AvgLen", 0.7, "Average GK Pass Length", "Length in yards", "Teams", False)
    sort_data_frame(df, "Att", 1, "Attempted Long GK passes", "Long Passes", "Teams", False)
    sort_data_frame(df, "Cmp%", 1, "% Completed GK Long Passes", "% Long Passes", "Teams", True)
    sort_data_frame(df, "Launch%", 1, "% of GK Long Passes", "% Long Passes", "Teams", True)
    sort_data_frame(df, "Att.2", 0.7, "Number of goal kicks", "# Goal kicks", "Teams", False)
    sort_data_frame(df, "Launch%.1", 1, "% of Goal Kicks Launched", " Launched Goal Kicks", "Teams", True)
    sort_data_frame(df, "AvgLen.1", 0.7, "Average Goal Kick Length", "Length in yards", "Teams", False)
    sort_data_frame(df, "Opp", 0.7, "Crosses against into the box", "# Crosses", "Teams", False)
    sort_data_frame(df, "Stp", 0.1, "Crosses stopped by GK in box", "# Crosses", "Teams", False)
    sort_data_frame(df, "Stp%", 0.1, "% of crosses stopped by GK", "# Crosses", "Teams", True)
    sort_data_frame(df, "#OPA", 0.1, "# of Defensive Actions outside penalty area", "# Actions", "Teams", False)
    sort_data_frame(df, "AvgDist", 0.1, "Avg. Dist/ from goal of defensive actions", "Distance (Yards)", "Teams", False)


def keeping_players():
    url = "https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))#
    df = None
    for each in comments:
        if "table" in str(each):
            try:
                df = pd.read_html(str(each), header=1)[0]
                df = df[df['Rk'].ne('Rk')].reset_index(drop=True)
            except ValueError:
                continue

    sort_data_frame_players(df, "GA", 0.4, "Goals conceded", "# Goals", "GK", False)
    sort_data_frame_zeroes_players(df, "PKA", 0.1, "Penalty goals conceded", "# Goals", "GK", False)
    sort_data_frame_zeroes_players(df, "FK", 0.02, "Free kick goals conceded", "# Goals", "GK", False)
    sort_data_frame_zeroes_players(df, "CK", 0.1, "Corner kick goals conceded", "# Goals", "GK", False)
    sort_data_frame_zeroes_players(df, "OG", 0.02, "Own goals conceded", "# Goals", "GK", False)
    sort_data_frame_players(df, "PSxG", 0.02, "Expected goals from shots", "xG", "GK", False)
    sort_data_frame_players(df, "PSxG/SoT", 0.005, "Expected goals from Shot on Target", "Goals/Shot", "GK", False)
    sort_data_frame_negatives_players(df, "PSxG+/-", 0.1, 0.3, "xG Difference", "# xG Difference", "GK", False)
    sort_data_frame_players(df, "Att.1", 2, "Attempted GK passes", "Passes", "GK", False)
    sort_data_frame_players(df, "Thr", 1, "Number of GK throws", "Throws", "GK", False)
    sort_data_frame_players(df, "AvgLen", 0.7, "Average GK Pass Length", "Length in yards", "GK", False)
    sort_data_frame_players(df, "Att", 1, "Attempted Long GK passes", "Long Passes", "GK", False)
    sort_data_frame_players(df, "Cmp%", 1, "% Completed GK Long Passes", "% Long Passes", "GK", True)
    sort_data_frame_players(df, "Launch%", 1, "% of GK Long Passes", "% Long Passes", "GK", True)
    sort_data_frame_players(df, "Att.2", 0.7, "Number of goal kicks", "# Goal kicks", "GK", False)
    sort_data_frame_players(df, "Launch%.1", 1, "% of Goal Kicks Launched", " Launched Goal Kicks", "GK", True)
    sort_data_frame_players(df, "AvgLen.1", 0.7, "Average Goal Kick Length", "Length in yards", "GK", False)
    sort_data_frame_players(df, "Opp", 0.7, "Crosses against into the box", "# Crosses", "GK", False)
    sort_data_frame_players(df, "Stp", 0.1, "Crosses stopped by GK in box", "# Crosses", "GK", False)
    sort_data_frame_players(df, "Stp%", 0.1, "% of crosses stopped by GK", "# Crosses", "GK", True)
    sort_data_frame_players(df, "#OPA", 0.1, "# of Defensive Actions outside penalty area", "# Actions", "GK", False)
    sort_data_frame_players(df, "AvgDist", 0.1, "Avg. Dist from goal of defensive actions", "Yards", "GK", False)


def shooting_teams():
    url = "https://fbref.com/en/comps/9/shooting/Premier-League-Stats"
    html = pd.read_html(url, header=1)
    df = html[0]

    sort_data_frame(df, "Sh", 2, "Number of shots", "# Shots", "Teams", False)
    sort_data_frame(df, "Sh/90", 0.1, "Number of shots/90", "# Shots / 90", "Teams", False)
    sort_data_frame(df, "SoT", 0.6, "Number of shots on Target", "# Shots", "Teams", False)
    sort_data_frame(df, "SoT/90", 0.05, "Number of shots on Target/90", "# Shots / 90", "Teams", False)
    sort_data_frame(df, "SoT%", 0.2, "Shots on Target %", "% SoT", "Teams", True)
    sort_data_frame(df, "G/Sh", 0.0007, "Goals / Shot", "# Goals", "Teams", False)
    sort_data_frame(df, "G/SoT", 0.007, "Goals / SoT", "# Goals", "Teams", False)
    sort_data_frame(df, "Dist", 0.1, "Avg. Dist. of shots taken", "Distance in yards", "Teams", False)
    sort_data_frame_zeroes(df, "FK", 0.1, "Shots from Free Kicks", "# Free Kicks", "Teams", False)
    sort_data_frame(df, "xG", 0.1, "xG", "# Goals", "Teams", False)
    sort_data_frame(df, "npxG", 0.1, "Non Penalty xG", "npxG", "Teams", False)
    sort_data_frame(df, "npxG/Sh", 0.0007, "Non Penalty xG per Shot", "npxG/Shot", "Teams", False)
    sort_data_frame_negatives(df, "np:G-xG", 0.1, 0.4, "Goals minus xG from non-pens", "Goals", "Teams", False)


def shooting_players():
    url = "https://fbref.com/en/comps/9/shooting/Premier-League-Stats"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))  #
    df = None
    for each in comments:
        if "table" in str(each):
            try:
                df = pd.read_html(str(each), header=1)[0]
                df = df[df['Rk'].ne('Rk')].reset_index(drop=True)
            except ValueError:
                continue

    """df["90s"] = df["90s"].astype(float)
    df["Sh"] = df["Sh"].astype(float)
    for index, row in df.iterrows():
        if row["90s"] < 4:
            df = df.drop(index)
        elif row["Sh"] < 25:
            df = df.drop(index)"""

    sort_data_frame_players(df, "Sh", 2, "Number of shots", "# Shots", "Teams", False)
    sort_data_frame_players(df, "Sh/90", 0.1, "Number of shots/90", "# Shots / 90", "Teams", False)
    sort_data_frame_players(df, "SoT", 0.6, "Number of shots on Target", "# Shots", "Teams", False)
    sort_data_frame_players(df, "SoT/90", 0.05, "Number of shots on Target/90", "# Shots / 90", "Teams", False)
    sort_data_frame_players(df, "SoT%", 0.2, "Shots on Target %", "% SoT", "Teams", True)
    sort_data_frame_players(df, "G/Sh", 0.0007, "Goals / Shot", "# Goals", "Teams", False)
    sort_data_frame_players(df, "G/SoT", 0.007, "Goals / SoT", "# Goals", "Teams", False)
    sort_data_frame_players(df, "Dist", 0.1, "Avg. Dist. of shots taken", "Distance in yards", "Teams", False)
    sort_data_frame_zeroes_players(df, "FK", 0.1, "Shots from Free Kicks", "# Free Kicks", "Teams", False)
    sort_data_frame_players(df, "xG", 0.1, "xG", "# Goals", "Teams", False)
    sort_data_frame_players(df, "npxG", 0.1, "Non Penalty xG", "npxG", "Teams", False)
    sort_data_frame_players(df, "npxG/Sh", 0.0007, "Non Penalty xG per Shot", "npxG/Shot", "Teams", False)
    sort_data_frame_negatives_players(df, "np:G-xG", 0.1, 0.4, "Goals minus xG from non-pens", "Goals", "Teams", False)


def passing_teams():
    url = "https://fbref.com/en/comps/9/passing/Premier-League-Stats"
    html = pd.read_html(url, header=1)
    df = html[0]

    sort_data_frame(df, "Att", 50, "Attempted Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp", 15, "Completed Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp%", 1, "% Completed Passes", "% Passes", "Teams", True)
    sort_data_frame(df, "TotDist", 1000, "Total Pass Distance", "Distance in yards", "Teams", False)
    sort_data_frame(df, "PrgDist", 500, "Progressive Pass Distance", "Distance in yards", "Teams", False)
    sort_data_frame(df, "Att.1", 50, "Attempted Short Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp.1", 15, "Completed Short Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp%.1", 1, "% Completed Short Passes", "% Passes", "Teams", True)
    sort_data_frame(df, "Att.2", 50, "Attempted Medium Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp.2", 15, "Completed Medium Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp%.2", 1, "% Completed Medium Passes", "% Passes", "Teams", True)
    sort_data_frame(df, "Att.3", 20, "Attempted Long Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp.3", 5, "Completed Long Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Cmp%.3", 1, "% Completed Long Passes", "% Passes", "Teams", True)

    fig, ax = plt.subplots()
    a = df["Cmp"]
    b = df["Cmp.2"]
    c = df["Cmp.3"]

    ax.barh(df["Squad"], a, label="Short Passes")
    ax.barh(df["Squad"], b, left=a, label="Medium Passes")
    ax.barh(df["Squad"], c, left=a + b, label="Long Passes")
    plt.gca().invert_yaxis()
    ax.set_ylabel("Teams")
    ax.set_title("Pass Composition")
    plt.legend()
    show_plots()

    sort_data_frame(df, "KP", 1, "Passes leading to a shot", "# Passes", "Teams", False)
    sort_data_frame(df, "1/3", 5, "Passes into the final third", "# Passes", "Teams", False)
    sort_data_frame(df, "PPA", 1, "Passes into the box", "# Passes", "Teams", False)
    sort_data_frame(df, "CrsPA", 0.5, "Crosses into the box into the box", "# Crosses", "Teams", False)
    sort_data_frame(df, "Prog", 5, "Progressive Passes", "# Passes", "Teams", False)


def passing_types_teams():
    url = "https://fbref.com/en/comps/9/passing_types/Premier-League-Stats"
    html = pd.read_html(url, header=1)
    df = html[0]

    sort_data_frame(df, "Live", 50, "Live Ball Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Dead", 5, "Dead Ball Passes", "# Passes", "Teams", False)
    sort_data_frame(df, "Press", 1, "Passes Under Pressure", "# Passes", "Teams", False)
    sort_data_frame(df, "CK", 1, "Corner Kicks", "# CK", "Teams", False)
    sort_data_frame_zeroes(df, "In", 1, "In-swinging Corner Kicks", "# Ck", "Teams", False)
    sort_data_frame_zeroes(df, "Out", 1, "Out-swinging Corner Kicks", "# Ck", "Teams", False)
    sort_data_frame_zeroes(df, "Str", 0.1, "Straight Corner Kicks", "# Ck", "Teams", False)
    sort_data_frame_zeroes(df, "Ground", 20, "Ground Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Low", 10, "Low Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "High", 5, "High Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Left", 10, "Left Foot Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Right", 20, "Right Foot Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Head", 2, "Headed Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "TI", 1, "Throw Ins", "# Throw Ins", "Teams", False)
    sort_data_frame_zeroes(df, "Cmp", 20, "Completed Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Off", 0.2, "Offsides", "# Offsides", "Teams", False)
    sort_data_frame_zeroes(df, "Out.1", 1, "Out of Bounds passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Int", 1, "Intercepted Passes", "# Passes", "Teams", False)
    sort_data_frame_zeroes(df, "Blocks", 1, "Blocked Passes", "# Passes", "Teams", False)


general_team()
nations()
keeping_teams()
keeping_players()
shooting_teams()
shooting_players()
passing_teams()
passing_types_teams()
