import pandas as pd

df = pd.read_csv('data/births_deaths.csv')

new_df = df[['Location', 'Time', 'Sex', 'Age', 'IndicatorName', 'Value']]
new_df.columns = ['kraj', 'rok', 'płeć', 'wiek', 'Indykator', 'wartość']

new_df.to_csv('birth_death.csv', index=False)