import io
import requests
import pandas as pd


file_url = 'https://www.football-data.co.uk/mmz4281/9394/I1.csv'
urlData = requests.get(file_url).content
rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))

# cleanData has only important columns and no NULL values in any column or row
cleanData = rawData[["Div", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].dropna()

# filter only data for Juventus (playing either away or home)
juventusData = cleanData[(cleanData["HomeTeam"] == 'Juventus') | (cleanData["AwayTeam"] == 'Juventus')]

juventusHomeWinningData = juventusData[(juventusData["HomeTeam"] == 'Juventus') & (juventusData["FTR"] == 'H')]

juventusAwayWinningData = juventusData[(juventusData["AwayTeam"] == 'Juventus') & (juventusData["FTR"] == 'A')]

juventusWinningData = juventusData[((juventusData["HomeTeam"] == 'Juventus') & (juventusData["FTR"] == 'H')) | ((juventusData["AwayTeam"] == 'Juventus') & (juventusData["FTR"] == 'A'))]