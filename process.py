# %%
import pandas

def table_to_df(table):
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip header row
        row = []
        for td in tr.find_all(['td', 'th']):
            row.append(td.text.strip())
        if row:  # Only append non-empty rows
            rows.append(row)

    return pandas.DataFrame(rows, columns=headers)
# %%
import requests
from bs4 import BeautifulSoup
session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})
resp = session.get('https://en.wikipedia.org/wiki/Blue_Riband')
resp.raise_for_status()
bs4 = BeautifulSoup(resp.text, 'html.parser')

# %%
tabs = bs4.find_all('table', class_='wikitable')

# Convert the first table to a pandas dataframe
westbound = table_to_df(tabs[0])
westbound['Direction'] = 'Westbound'
eastbound = table_to_df(tabs[1])
eastbound['Direction'] = 'Eastbound'

df = pandas.concat([westbound, eastbound])

df.drop(columns=['Flag'], inplace=True)

# %%
df.head()

# %% Extract the knots from the speed column
df['Knots'] = df['Speed'].str.extract(r'(\d+\.?\d*)').astype(float)

# %% Extract the start date from the Dates and Year column
df['Start day'] = df['Dates'].str.extract(r'(\d+)').astype(int)
df['Start month'] = df['Dates'].str.extract(r'\s+([A-Za-z]+)')
df['Start year'] = df['Year']
df['Start date'] = df['Start year'].astype(str) + '-' + df['Start month'] + '-' + df['Start day'].astype(str)
df['Start date'] = pandas.to_datetime(df['Start date'], format='%Y-%B-%d')

# %% Remove references from the ship column
df['Ship'] = df['Ship'].str.extract(r'([A-Za-z\s]+)')

# %% Calculate the minutes taken for each crossing
df['Minutes'] = (df['Days, hours, minutes'].str.extract(r'(\d+) d').fillna(0).astype(int) * 24 * 60) + (df['Days, hours, minutes'].str.extract(r'(\d+) h').fillna(0).astype(int) * 60) + (df['Days, hours, minutes'].str.extract(r'(\d+) m').fillna(0).astype(int))
df['Days'] = df['Minutes'] / (24 * 60)

# %% Save the processed data to a new csv file
df.to_csv("Atlantic-crossings_processed.csv", index=False)

# %% Pivot the data to have the directions as columns and the dates as rows
df_pivot = df.pivot(index=['Start date','Ship'], columns='Direction', values='Knots')
df_pivot.to_csv("Atlantic-crossings_processed_knots.csv")

# %% Pivot the data to have the directions as columns and the dates as rows
df_pivot2 = df.pivot(index=['Start date','Ship'], columns='Direction', values='Days')
df_pivot2.to_csv("Atlantic-crossings_processed_days.csv")

# %%
