import pandas as pd
import numpy as np
import boto3
import io

s3_client = boto3.client('s3')

bucket_name = 'football-prediction-test'
file_paths = ['E0-2324.csv', 'E0-2223.csv', 'E1-2223.csv']

dfs = []
for file_path in file_paths:
    response = s3_client.get_object(Bucket=bucket_name, Key=file_path)
    df = pd.read_csv(io.BytesIO(response['Body'].read()))
    dfs.append(df)

df_season_1 = dfs[0]
df_season_2 = dfs[1]
df_season_2_second = dfs[2]


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

output_bucket_name = 'football-prediction-test'
output_file_path = 'E0-2324-ProcessesData.csv'

df_both_seasons_essentials.to_csv(output_file_path, index=False)
with open(output_file_path, 'rb') as file:
    s3_client.upload_fileobj(file, output_bucket_name, output_file_path)