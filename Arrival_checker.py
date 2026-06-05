import pandas as pd

# Read the Excel file
df = pd.read_excel('paper_case_manuel_instance.xlsx')

# Display the first few rows
print(df.head())


runway_4 = df[df['arrival_runway'] == 4]
runway_4_sorted = runway_4.sort_values(by='arrival_time')
runway_3 = df[df['arrival_runway'] == 3]
runway_3_sorted = runway_3.sort_values(by='arrival_time')

print("Flights on Runway 4 (sorted by arrival time):")
print(runway_4_sorted)
print("Flights on Runway 3 (sorted by arrival time):")
print(runway_3_sorted)

def check_arrival_conflicts(df):
    runway_3 = df[df['arrival_runway'] == 3]
    df1 = runway_3.sort_values(by='arrival_time').copy()
    runway_4 = df[df['arrival_runway'] == 4]
    df2 = runway_4.sort_values(by='arrival_time').copy()
    changed = 0
    for i in range(len(df1) - 1):
        i = i+1
        if df1.iloc[i]['arrival_time'] < df1.iloc[i-1]['arrival_time'] + 1:
            df1.loc[df1.index[i], 'arrival_time'] = df1.iloc[i]['arrival_time'] + 1
        elif df1.iloc[i]['arrival_time'] < df1.iloc[i-1]['arrival_time'] + 2 and df1.iloc[i]['aircraft_size'] in ['B', 'C'] and df1.iloc[i-1]['aircraft_size'] in ['D', 'E', 'F']:
            df1.loc[df1.index[i], 'arrival_time'] = df1.iloc[i]['arrival_time'] + 1
            changed = 1
    for i in range(len(df2) - 1):
        i = i+1
        if df2.iloc[i]['arrival_time'] < df2.iloc[i-1]['arrival_time'] + 1:
            df2.loc[df2.index[i], 'arrival_time'] = df2.iloc[i]['arrival_time'] + 1
        elif df2.iloc[i]['arrival_time'] < df2.iloc[i-1]['arrival_time'] + 2 and df2.iloc[i]['aircraft_size'] in ['B', 'C'] and df2.iloc[i-1]['aircraft_size'] in ['D', 'E', 'F']:
            df2.loc[df2.index[i], 'arrival_time'] = df2.iloc[i]['arrival_time'] + 1
            changed = 1    
    return df1, df2, changed

while True:
    runway_3_sorted, runway_4_sorted, changed = check_arrival_conflicts(df)
    df = pd.concat([runway_3_sorted, runway_4_sorted], ignore_index=True)
    if changed == 0:
        break


df.to_excel('paper_case_manuel_instance_updated.xlsx', index=False)