import pandas as pd
def birth():
    df = pd.read_csv('data/births_deaths.csv')

    new_df = df[['Location', 'Time', 'Sex', 'Age', 'IndicatorName', 'Value']]
    new_df.columns = ['kraj', 'rok', 'płeć', 'wiek', 'Indykator', 'wartość']

    new_df.to_csv('birth_death.csv', index=False)
    new_df.to_excel('birth_death.xlsx', index=False)

def married():
    df = pd.read_csv('data/married.csv')
    new_rows = []

    for index, row in df.iterrows():
        age_start = row['AgeStart']
        age_end = row['AgeEnd']
        value = row['Value']

        age_range = age_end - age_start + 1
        value_per_age = value / age_range

        for age in range(age_start, age_end + 1):
            new_row = row.copy()
            new_row['Age'] = age
            new_row['Value'] = value_per_age
            new_row['AgeStart'] = age
            new_row['AgeEnd'] = age
            new_rows.append(new_row)
    new_df = pd.DataFrame(new_rows)

    final_df = new_df[['Location', 'Time', 'Sex', 'Age', 'IndicatorName', 'Value']]
    final_df.columns = ['kraj', 'rok', 'płeć', 'wiek', 'IndicatorName', 'wartość']

    final_df.to_csv('married.csv', index=False)
    final_df.to_excel('married.xlsx', index=False)

birth()
