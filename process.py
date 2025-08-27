# %%
import pandas
df = pandas.read_csv("Atlantic crossings.csv")

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

# %% Pivot the data to have the directions as columns and the dates as rows
df_pivot = df.pivot(index=['Start date','Ship'], columns='Direction', values='Knots')

# %% Save the processed data to a new csv file
df_pivot.to_csv("Atlantic crossings_processed.csv")

# %% Pivot the data to have the directions as columns and the dates as rows
df_pivot2 = df.pivot(index=['Start date','Ship'], columns='Direction', values='Days')
df_pivot2.to_csv("Atlantic crossings_processed_days.csv")

# %%
