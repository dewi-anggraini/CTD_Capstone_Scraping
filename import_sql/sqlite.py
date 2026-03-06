# 2. Database Import Program
import sqlite3
import pandas as pd
import os
 
# Connect to SQLite database (creates file if not exists) 
conn = sqlite3.connect("my_database.db") 
cursor = conn.cursor()

# List of CSV files 
csv_files = ["Standings.csv", "BattingLeaders.csv", "PitchingLeaders.csv"] 

# Loop through each file and import 
for csv_file in csv_files: 
    try: 
       # Use filename (without extension) as table name 
       table_name = os.path.splitext(os.path.basename(csv_file))[0]

       # Conversion
       if table_name == "Standings":
           df = pd.read_csv(csv_file, header=None) 
           df.columns = ["Year", "Team", "Wins", "Losses", "Pct", "GB"]
           # Convert year to integer 
           df["Year"] = df["Year"].astype(int) 
           # Wins/Losses to integers 
           df["Wins"] = pd.to_numeric(df["Wins"], errors="coerce").astype("Int64") 
           df["Losses"] = pd.to_numeric(df["Losses"], errors="coerce").astype("Int64") 
           # Winning percentage to float 
           df["Pct"] = pd.to_numeric(df["Pct"], errors="coerce") 

       elif table_name in ["BattingLeaders", "PitchingLeaders"]: 
            df = pd.read_csv(csv_file, header=0) 
            df = df.rename(columns={
                "#": "Value",
                "Name(s)": "Name",
                "Team(s)": "Team",
                "Top 25": "Rank"
                }) 
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64") 
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        
       # Import into SQLite (replace if table exists) 
       df.to_sql(table_name, conn, if_exists="replace", index=False) 

       print(f"Imported {csv_file} into {table_name} successfully.")

    except Exception as e: 
        print(f"Error importing {csv_file}: {e}") 

print("\nChecking database contents...") 
# List all tables 
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") 
tables = cursor.fetchall() 
print("Tables in database:", tables) 

# Show first 5 rows from each table 
for (table_name,) in tables: 
    print(f"\nPreview of {table_name}:") 
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;") 
    rows = cursor.fetchall() 
    for row in rows: 
        print(row)

# Example: teams with more than 30 wins 
cursor.execute("SELECT Year, Team, Wins FROM Standings WHERE Wins > 30;") 
print(cursor.fetchall()) 
# Example: batting leaders with Value > 25 
cursor.execute('SELECT Year, Statistic, Name, Team, Value FROM BattingLeaders WHERE Value > 25;') 
print(cursor.fetchall())
       
# Close connection 
conn.close()