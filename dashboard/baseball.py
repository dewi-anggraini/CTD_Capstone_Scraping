# 4. Dashboard Program
import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

conn = sqlite3.connect("my_database.db")

# Sidebar controls
st.sidebar.header("Dashboard Controls")
allowed_years = [1901, 1902, 1903] # limit to only 3 for the demo 
year = st.sidebar.selectbox("Select Year", allowed_years)
num_players = st.sidebar.radio("Number of Players to Display", [1]) # limit to only 1 player for the demo
batting_stat = st.sidebar.selectbox("Batting Stat", ["Home Runs", "RBI", "Runs", "Doubles"])
pitching_stat = st.sidebar.selectbox("Pitching Stat", ["Batting Average", "Slugging Average"])

# Query data for the selected year
standings = pd.read_sql(f"SELECT * FROM standings WHERE Year={year}", conn)
batting = pd.read_sql(f"SELECT * FROM battingleaders WHERE Year={year}", conn)
pitching = pd.read_sql(f"SELECT * FROM pitchingleaders WHERE Year={year}", conn)
#st.write(batting[batting["Year"] == year][batting["Statistic"] == "AVG"]) # Checking when needed.
#st.write(pitching["Statistic"].unique())

conn.close()

# -------------------------------
# Visualization 1: Team Standings
st.subheader(f"Team Standings ({year})")
fig1 = px.bar(
    standings,
    x="Wins",
    y="Team",
    title="Wins by Team"
)
st.plotly_chart(fig1)

# -------------------------------
# Visualization 2: Sidebar toggle for chart type: Batting Leader
chart_type = st.sidebar.radio("Chart Type", ["Bar", "Pie"])

# Filter batting data
batting_filtered = batting[(batting["Year"] == year) & (batting["Statistic"] == batting_stat)].copy()
batting_filtered["Value"] = pd.to_numeric(batting_filtered["Value"], errors="coerce")
batting_filtered = batting_filtered.dropna(subset=["Value"])

if batting_filtered.empty:
    st.warning(f"No data available for {batting_stat} in {year}")
else:
    if chart_type == "Bar":
        st.subheader(f"{batting_stat} Leader ({year})")
        fig_bat = px.bar(
            batting_filtered.sort_values(by="Value", ascending=False).head(num_players),
            x="Value",
            y="Name",
            orientation="h",
            title=f"{batting_stat} Leader ({year})"
        )
        st.plotly_chart(fig_bat)
    
    # Variation for the demo
    elif chart_type == "Pie":
        st.subheader(f"{batting_stat} Distribution ({year})")
        fig_pie_bat = px.pie(
            batting_filtered,
            values="Value",
            names="Name",
            title=f"{batting_stat} Distribution among Players ({year})",
            hole=0.3  # donut style
        )
        st.plotly_chart(fig_pie_bat)

# -------------------------------
# Visualization 3: Pitching Leaders
st.subheader(f"{pitching_stat} Leader ({year}) - {pitching_stat}")

# Filter rows = Statistic matches the selected stat
pitching_filtered = pitching[pitching["Statistic"] == pitching_stat].copy()

# Convert Value column to numeric
pitching_filtered["Value"] = pd.to_numeric(pitching_filtered["Value"], errors="coerce")
pitching_filtered = pitching_filtered.dropna(subset=["Value"])

# Sort and take only top
pitching_sorted = pitching_filtered.sort_values(by="Value", ascending=False).head(num_players)

# Plot
fig3 = px.bar(
    pitching_sorted,
    x="Value",
    y="Name",
    orientation="h",
    title=f"{pitching_stat} Leader ({year})"
)
st.plotly_chart(fig3)

# Visualization: Team Wins Pie Chart
st.subheader(f"Team Wins Distribution ({year})")

# Filter standings for the selected year
standings_filtered = standings[standings["Year"] == year].copy()

# Convert Wins to numeric
standings_filtered["Wins"] = pd.to_numeric(standings_filtered["Wins"], errors="coerce")

# Create pie chart
fig_pie = px.pie(
    standings_filtered,
    values="Wins",
    names="Team",
    title=f"Wins Distribution by Team ({year})",
    hole=0.3  
)

st.plotly_chart(fig_pie)

# -------------------------------
# Footer
st.write("Interactive Baseball History Dashboard Based On https://www.baseball-almanac.com/yearmenu.shtml- Powered by Streamlit")





