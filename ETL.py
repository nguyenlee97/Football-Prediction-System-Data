
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import sys

df_season_1=pd.read_csv('E0-2324.csv')
df_season_2 = pd.read_csv('E0-2223.csv')
df_season_2_second =pd.read_csv('E1-2223.csv')


df_burnley_home= df_season_2_second[df_season_2_second['HomeTeam']=='Burnley']
df_shefutd_home= df_season_2_second[df_season_2_second['HomeTeam']=='Sheffield United']
df_luton_home = df_season_2_second[df_season_2_second['HomeTeam']=='Luton']
df_burnley_away= df_season_2_second[df_season_2_second['AwayTeam']=='Burnley']
df_shefutd_away = df_season_2_second[df_season_2_second['AwayTeam']=='Sheffield United']
df_luton_away = df_season_2_second[df_season_2_second['AwayTeam']=='Luton']
df_season_2_second = pd.concat([df_burnley_home, df_burnley_away, df_shefutd_home, df_shefutd_away, df_luton_home, df_luton_away], axis=0)

df_season_2= pd.concat([df_season_2,df_season_2_second], axis=0)

teams_s1 = df_season_1.columns.unique()

teams_s2 = df_season_2.columns.unique()

same_columns = np.intersect1d(teams_s1, teams_s2)

df_season_1 = df_season_1[same_columns]
df_season_2 = df_season_2[same_columns]

df_both_seasons = pd.concat([df_season_1, df_season_2], axis=0)

df_both_seasons['Date'] = pd.to_datetime(df_both_seasons['Date'], dayfirst=True, errors='coerce')

df_both_seasons['Day'] = df_both_seasons['Date'].dt.day
df_both_seasons['Month'] = df_both_seasons['Date'].dt.month
df_both_seasons['Year'] = df_both_seasons['Date'].dt.year

df_both_seasons_essentials = df_both_seasons[['Day','Month','Year','HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HST', 'AST']]

df_both_seasons_essentials['HTGDIFF'] = df_both_seasons_essentials['FTHG'] - df_both_seasons_essentials['FTAG']
df_both_seasons_essentials['ATGDIFF'] = df_both_seasons_essentials['FTAG'] - df_both_seasons_essentials['FTHG']

df_both_seasons_essentials= df_both_seasons_essentials.sort_values(['Year', 'Month','Day'], ascending=False)

df_both_seasons_essentials.to_csv('df_both_seasons_essentials', index=False)