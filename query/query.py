# 3. Database Query Program
import sqlite3

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Mapping long names in standings to short names in leaders tables 
team_map = { 
    "Boston Americans": ("Boston Americans", "Boston"), 
    "Philadelphia Athletics": ("Philadelphia Athletics", "Philadelphia"), 
    "Baltimore Orioles": ("Baltimore Orioles", "Baltimore"), 
    "Cleveland Blues": ("Cleveland Blues", "Cleveland"), 
    "Washington Senators": ("Washington Senators", "Washington"), 
    "St. Louis Browns": ("St. Louis Browns", "St. Louis"), 
    "Detroit Tigers": ("Detroit Tigers", "Detroit"), 
    "Chicago White Sox": ("Chicago White Sox", "Chicago"), 
    "Milwaukee Brewers": ("Milwaukee Brewers", "Milwaukee"), 
    "New York Highlanders": ("New York Highlanders", "New York") 
    }
# Checking the database schema
#cursor.execute("PRAGMA table_info(BattingLeaders);") 
#print(cursor.fetchall())
#cursor.execute("SELECT DISTINCT Team FROM PitchingLeaders")
#print(cursor.fetchall())
#ursor.execute("SELECT DISTINCT Team FROM BattingLeaders")
#print(cursor.fetchall())
#cursor.execute("SELECT DISTINCT Statistic FROM BattingLeaders")
#print(cursor.fetchall())
#cursor.execute("SELECT DISTINCT Statistic FROM PitchingLeaders")
#print(cursor.fetchall())

# Create a function to normalize the team's name (different names in different files)
# this will return name based on mapping
def normalize_team(team):
    return team_map.get(team, (team, team))

while True:
    print("\nMajor League Baseball Database Menu")
    print("1. Show Team Standings")
    print("2. Show Batting Leaders")
    print("3. Show Pitching Leaders")
    print("4. Join Pitching Leaders With Team Standings")
    print("5. Filter Standings by Year")
    print("6. Filter Batting Leaders by Player")
    print("7. Filter Pitching Leaders by Player")
    print("8. Filter by Team")
    print("9. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        cursor.execute("SELECT * FROM Standings")
        for row in cursor.fetchall():
            print(row)

    elif choice == "2":
        cursor.execute("SELECT * FROM BattingLeaders")
        for row in cursor.fetchall():
            print(row)

    elif choice == "3":
        cursor.execute("SELECT * FROM PitchingLeaders")
        for row in cursor.fetchall():
            print(row)

    elif choice == "4":
        for long_team, short_team in team_map.values():
            cursor.execute("""
                SELECT p.Name, p.Team, p.Value, s.Wins, s.Losses
                FROM PitchingLeaders p, Standings s
                WHERE p.Team = ? AND s.Team = ? AND p.Statistic = 'Batting Average'
            """, (short_team, long_team))
            for row in cursor.fetchall():
                print(row)

    elif choice == "5":
        cursor.execute("SELECT DISTINCT Year FROM Standings")
        years = cursor.fetchall()
        print("Available years:", [y[0] for y in years])
        year = input("Enter year: ")
        cursor.execute("SELECT * FROM Standings WHERE Year = ?", (year,))
        for row in cursor.fetchall():
            print(row)
    
    elif choice == "6":
        cursor.execute("""
            SELECT DISTINCT Name 
            FROM BattingLeaders 
            WHERE Name IS NOT NULL 
            AND Name NOT IN ('Name(s)', 'Team(s)', 'Statistic', 'Boston', 'Philadelphia', 'Washington', 'Detroit', 'St. Louis')
        """)
        players = [p[0] for p in cursor.fetchall()]
        print("Available players:", players)

        player = input("Enter player name: ")
        cursor.execute("SELECT * FROM BattingLeaders WHERE LOWER(Name) = LOWER(?)", (player,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No batting leader found for", player)

    elif choice == "7":
        cursor.execute("SELECT DISTINCT Name FROM PitchingLeaders")
        players = cursor.fetchall()
        print("Available players:", [p[0] for p in players])
        player = input("Enter player name: ")
        cursor.execute("SELECT * FROM PitchingLeaders WHERE Name = ?", (player,))
        for row in cursor.fetchall():
            print(row)
   
    elif choice == "8":
        cursor.execute("SELECT DISTINCT Team FROM Standings")
        teams = cursor.fetchall()
        print("Available teams:", [t[0] for t in teams])
        team = input("Enter team name: ")

        long_team, short_team = normalize_team(team)

        print("\n--- Standings ---")
        cursor.execute("SELECT * FROM Standings WHERE Team = ?", (long_team,))
        for row in cursor.fetchall():
            print(row)

        print("\n--- Batting Leaders ---") 
        cursor.execute("SELECT * FROM BattingLeaders WHERE Team = ?", (short_team,)) 
        for row in cursor.fetchall(): print(row)

        print("\n--- Pitching Leaders ---")
        cursor.execute("SELECT * FROM PitchingLeaders WHERE Team = ?", (short_team,))
        pitching_rows = cursor.fetchall()
        if pitching_rows:
            for row in pitching_rows:
                print(row)
        else:
            print("No pitching leaders found for", short_team)

    if choice == "9":
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Try Again.")

conn.close()

