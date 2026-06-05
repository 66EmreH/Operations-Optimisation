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
    df1 = runway_3.sort_values(by='arrival_time')
    runway_4 = df[df['arrival_runway'] == 4]
    df2 = runway_4.sort_values(by='arrival_time')
    swapped = 0
    for i in range(len(df1) - 1):
        i = i+1
        if df1.iloc[i]['arrival_time'] < df1.iloc[i-1]['arrival_time'] + 2:
            df1.iloc[i]['arrival_runway'] = 4
            swapped = swapped + 1
    print(f"Number of conflicts detected on runway {df1.iloc[i]['arrival_runway']}: {swapped}")
    for i in range(len(df2) - 1):
        i = i+1
        if df2.iloc[i]['arrival_time'] < df2.iloc[i-1]['arrival_time'] + 2:
            df2.iloc[i]['arrival_runway'] = 3
            swapped = swapped + 1
    print(f"Number of conflicts detected on runway {df2.iloc[i]['arrival_runway']}: {swapped}")
    dfnew = pd.concat([df1, df2]).sort_values(by='arrival_time')

    return swapped, dfnew
going = True
timer = 20
previous_swapped = 1e6
while going:

    swapped, df = check_arrival_conflicts(df)
    if previous_swapped <= swapped:
        timer -= 1
    previous_swapped = swapped
    final_df = df.sort_values(by='arrival_time')

    if timer == 0:
        print("No more improvements detected. Final schedule:")
        print(final_df)
        break

    if swapped == 0:
        print("No more conflicts detected. Final schedule:")
        print(final_df)
        break
