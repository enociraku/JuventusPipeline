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

# Football season is expressed as a combination of 2 years, for example: season 91-92. In the website the hyphen 
# is missing so it is: 9192. This is how we are goning to loop over the files to extract all seasons.

# First year in the football season
year1 = 0
# Second year in the football season
year2 = 1
# Initialize empty dataframe
df = pd.DataFrame(columns = ["Div", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])


for index in range(1, 101):
    
    # Convert the years from integer to character (so that you can add the 0s later):
    year1_str = str(year1)
    year2_str = str(year2)
    
    if year1 < 10:
        year1_str = "0" + year1_str # Add extra 0 in front of the year number
    if year2 < 10:
        year2_str = "0" + year2_str # Add extra 0 in front of the year number
        
    file_url = 'https://www.football-data.co.uk/mmz4281/{}/I1.csv'.format(year1_str + year2_str)
    print(year1_str, year2_str)
    print(file_url)
    if requests.get(file_url).status_code == 200:
        urlData = requests.get(file_url).content
        rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')), usecols = list(range(10))) # read only first 10 columns
        cleanData = rawData[["Div", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].dropna()
        df = pd.concat([df, cleanData] ,ignore_index=True)
        print(cleanData)
        
    
    year1 = (year1 + 1) % 100
    year2 = (year2 + 1) % 100
