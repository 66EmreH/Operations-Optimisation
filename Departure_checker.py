import pandas as pd

# Read the Excel file
df = pd.read_excel('paper_case_manuel_instance_fixed.xlsx')

# Display the first few rows
print(df.head())

print(df.iloc[0, 5])

def loop_check(df):
    changed = 0
    for i in range(100):
        count = 0
        times = [15*i,15*i+1,15*i+2,15*i+3,15*i+4,15*i+5,15*i+6,15*i+7,15*i+8,15*i+9,15*i+10,15*i+11,15*i+12,15*i+13,15*i+14]
        for j in range(len(df)):
            if df.iloc[j, 5] in times:
                count += 1
                final_j = j
        if count > 14:
            print(f"Time window {15*i} to {15*i+14} has {count} flights.")
            df.iloc[final_j, 5] = 15*i+15
            changed = 1

    return changed, df

changed = 1
loop_count = 0
while changed == 1:
    loop_count += 1
    changed, df = loop_check(df)
    print(f'Loop {loop_count} completed, checking again.')


df.to_excel('paper_case_manuel_instance_updated.xlsx', index=False)