import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# ── Auto-generate data if CSVs don't exist (needed for Streamlit Cloud) ───────
def generate_data():
    np.random.seed(42)
    TEAMS = ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bangalore",
             "Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad",
             "Rajasthan Royals","Punjab Kings"]
    VENUES = ["Wankhede Stadium","MA Chidambaram Stadium","Eden Gardens",
              "M. Chinnaswamy Stadium","Arun Jaitley Stadium","Rajiv Gandhi Intl Stadium",
              "Sawai Mansingh Stadium","PCA Stadium Mohali"]
    BATSMEN = [("Virat Kohli","Royal Challengers Bangalore"),("Rohit Sharma","Mumbai Indians"),
               ("MS Dhoni","Chennai Super Kings"),("AB de Villiers","Royal Challengers Bangalore"),
               ("David Warner","Sunrisers Hyderabad"),("Shikhar Dhawan","Delhi Capitals"),
               ("KL Rahul","Punjab Kings"),("Suresh Raina","Chennai Super Kings"),
               ("Hardik Pandya","Mumbai Indians"),("Andre Russell","Kolkata Knight Riders"),
               ("Jos Buttler","Rajasthan Royals"),("Shubman Gill","Kolkata Knight Riders")]
    BOWLERS = [("Lasith Malinga","Mumbai Indians"),("Jasprit Bumrah","Mumbai Indians"),
               ("Dwayne Bravo","Chennai Super Kings"),("Yuzvendra Chahal","Royal Challengers Bangalore"),
               ("Rashid Khan","Sunrisers Hyderabad"),("Amit Mishra","Delhi Capitals"),
               ("Ravindra Jadeja","Chennai Super Kings"),("Sunil Narine","Kolkata Knight Riders"),
               ("Kagiso Rabada","Delhi Capitals"),("Bhuvneshwar Kumar","Sunrisers Hyderabad")]
    rows, match_id = [], 1
    for season in range(2008, 2024):
        for _ in range(60 if season < 2022 else 74):
            t1, t2 = np.random.choice(TEAMS, 2, replace=False)
            s1 = int(np.clip(np.random.normal(165,18), 80, 263))
            s2 = int(np.clip(np.random.normal(158,18), 80, 263))
            winner = t1 if s1 > s2 else t2
            rows.append({"match_id":match_id,"season":season,
                         "date":f"{season}-04-{np.random.randint(1,30):02d}",
                         "venue":np.random.choice(VENUES),"team1":t1,"team2":t2,
                         "toss_winner":np.random.choice([t1,t2]),
                         "toss_decision":np.random.choice(["bat","field"],p=[0.55,0.45]),
                         "team1_score":s1,"team2_score":s2,"winner":winner,
                         "win_by_runs":abs(s1-s2) if winner==t1 else 0,
                         "win_by_wickets":np.random.randint(1,10) if winner==t2 else 0})
            match_id += 1
    pd.DataFrame(rows).to_csv("matches.csv", index=False)
    bat_rows = []
    for season in range(2008, 2024):
        for name, team in BATSMEN:
            inn = np.random.randint(10,18)
            runs = int(np.clip(np.random.normal(420,180), 50, 973))
            bat_rows.append({"season":season,"player":name,"team":team,"innings":inn,
                             "runs":runs,"average":round(runs/inn,1),
                             "strike_rate":round(np.random.uniform(118,195),1),
                             "fours":np.random.randint(30,80),"sixes":np.random.randint(10,50),
                             "fifties":np.random.randint(1,6),"hundreds":1 if runs>700 else 0})
    pd.DataFrame(bat_rows).to_csv("batting.csv", index=False)
    bowl_rows = []
    for season in range(2008, 2024):
        for name, team in BOWLERS:
            bowl_rows.append({"season":season,"player":name,"team":team,
                              "matches":np.random.randint(10,17),"wickets":np.random.randint(8,28),
                              "economy":round(np.random.uniform(6.5,9.8),2),
                              "average":round(np.random.uniform(18,32),1),
                              "best":f"{np.random.randint(2,6)}/{np.random.randint(10,45)}"})
    pd.DataFrame(bowl_rows).to_csv("bowling.csv", index=False)

if not os.path.exists("matches.csv"):
    generate_data()

st.set_page_config(page_title="IPL Analytics Dashboard", page_icon="🏏", layout="wide")

st.markdown("""
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
.metric-card { background:#f8f9fb; border-radius:10px; padding:1rem 1.2rem;
               border:1px solid #e8eaf0; text-align:center; }
.metric-value { font-size:1.8rem; font-weight:700; color:#1a1a2e; }
.metric-label { font-size:0.78rem; color:#6b7280; margin-top:2px; }
.section-title { font-size:1rem; font-weight:600; color:#374151; margin-bottom:0.4rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv", parse_dates=["date"])
    batting = pd.read_csv("batting.csv")
    bowling = pd.read_csv("bowling.csv")
    return matches, batting, bowling

matches, batting, bowling = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🏏 IPL Dashboard")
st.sidebar.markdown("---")

all_seasons = sorted(matches["season"].unique())
selected_seasons = st.sidebar.multiselect("Season", all_seasons, default=all_seasons)

all_teams = sorted(matches["team1"].unique())
selected_teams = st.sidebar.multiselect("Team", all_teams, default=all_teams)

st.sidebar.markdown("---")
st.sidebar.caption("📊 Synthetic IPL dataset · Built with Streamlit + Plotly")

if not selected_seasons: selected_seasons = all_seasons
if not selected_teams:   selected_teams   = all_teams

# ── Filter ────────────────────────────────────────────────────────────────────
m = matches[
    matches["season"].isin(selected_seasons) &
    (matches["team1"].isin(selected_teams) | matches["team2"].isin(selected_teams))
]
bat  = batting[batting["season"].isin(selected_seasons) & batting["team"].isin(selected_teams)]
bowl = bowling[bowling["season"].isin(selected_seasons) & bowling["team"].isin(selected_teams)]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏏 IPL Analytics Dashboard")
st.caption(f"Showing data for {len(selected_seasons)} season(s) · {len(selected_teams)} team(s)")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_matches = len(m)
avg_score     = round((m["team1_score"].mean() + m["team2_score"].mean()) / 2, 1) if total_matches else 0
highest_score = int(max(m["team1_score"].max(), m["team2_score"].max())) if total_matches else 0
total_sixes   = int(bat["sixes"].sum())
top_team      = m["winner"].value_counts().idxmax() if total_matches else "N/A"
top_wins      = int(m["winner"].value_counts().max()) if total_matches else 0

for col, val, lbl in zip(
    st.columns(5),
    [f"{total_matches:,}", str(avg_score), str(highest_score), f"{total_sixes:,}", top_team],
    ["Total Matches", "Avg First Innings", "Highest Score", "Total Sixes", f"Most Wins ({top_wins})"]
):
    col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div>'
                 f'<div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Wins by team + Toss ────────────────────────────────────────────────
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown('<div class="section-title">🏆 Wins by Team</div>', unsafe_allow_html=True)
    wins = m["winner"].value_counts().reset_index()
    wins.columns = ["team", "wins"]
    wins = wins.sort_values("wins", ascending=True).tail(8)
    fig = px.bar(wins, x="wins", y="team", orientation="h",
                 color="wins", color_continuous_scale="Blues",
                 labels={"wins": "Wins", "team": ""}, text="wins")
    fig.update_traces(textposition="outside")
    fig.update_layout(height=340, margin=dict(l=10,r=20,t=10,b=10),
                      showlegend=False, coloraxis_showscale=False,
                      plot_bgcolor="white", paper_bgcolor="white",
                      yaxis=dict(gridcolor="#f0f0f0"), xaxis=dict(gridcolor="#f0f0f0"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">🪙 Toss Decision Split</div>', unsafe_allow_html=True)
    toss = m["toss_decision"].value_counts().reset_index()
    toss.columns = ["decision", "count"]
    fig2 = px.pie(toss, values="count", names="decision",
                  color_discrete_sequence=["#3b82f6","#f59e0b"], hole=0.55)
    fig2.update_traces(textinfo="percent+label", pull=[0.03, 0.03])
    fig2.update_layout(height=340, margin=dict(l=10,r=10,t=10,b=10),
                       legend=dict(orientation="h", y=-0.05), paper_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Season trend + Venues ──────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="section-title">📈 Average Score per Season</div>', unsafe_allow_html=True)
    ss = m.groupby("season")["team1_score"].mean().reset_index()
    ss["team1_score"] = ss["team1_score"].round(1)
    fig3 = px.line(ss, x="season", y="team1_score", markers=True,
                   labels={"team1_score":"Avg Runs","season":"Season"},
                   color_discrete_sequence=["#3b82f6"])
    fig3.update_traces(line_width=2.5, marker_size=7)
    fig3.update_layout(height=310, margin=dict(l=10,r=10,t=10,b=10),
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis=dict(gridcolor="#f0f0f0", tickmode="linear"),
                       yaxis=dict(gridcolor="#f0f0f0"))
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown('<div class="section-title">🏟️ Matches per Venue</div>', unsafe_allow_html=True)
    vc = m["venue"].value_counts().head(6).reset_index()
    vc.columns = ["venue","matches"]
    vc["short"] = vc["venue"].str.replace(" Stadium","").str.replace(" International","")
    fig4 = px.bar(vc, x="short", y="matches",
                  color="matches", color_continuous_scale="Teal",
                  labels={"short":"","matches":"Matches"}, text="matches")
    fig4.update_traces(textposition="outside")
    fig4.update_layout(height=310, margin=dict(l=10,r=10,t=10,b=10),
                       showlegend=False, coloraxis_showscale=False,
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis=dict(tickangle=-20, gridcolor="#f0f0f0"),
                       yaxis=dict(gridcolor="#f0f0f0"))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Tabs for batsmen / bowlers ─────────────────────────────────────────
st.markdown("---")
tab1, tab2 = st.tabs(["🏏 Top Batsmen", "⚾ Top Bowlers"])

with tab1:
    tb = (bat.groupby(["player","team"])
          .agg(innings=("innings","sum"), runs=("runs","sum"),
               fours=("fours","sum"), sixes=("sixes","sum"),
               fifties=("fifties","sum"), hundreds=("hundreds","sum"))
          .reset_index())
    tb["average"] = (tb["runs"] / tb["innings"]).round(1)
    tb = tb.sort_values("runs", ascending=False).head(10).reset_index(drop=True)
    tb.index += 1

    ca, cb = st.columns([3,2])
    with ca:
        st.dataframe(tb[["player","team","innings","runs","average","fours","sixes","fifties","hundreds"]]
                     .rename(columns={"player":"Player","team":"Team","innings":"Inn","runs":"Runs",
                                      "average":"Avg","fours":"4s","sixes":"6s","fifties":"50s","hundreds":"100s"}),
                     use_container_width=True, height=350)
    with cb:
        fig5 = px.bar(tb.head(8), x="runs", y="player", orientation="h",
                      color="team", text="runs",
                      labels={"runs":"Runs","player":""}, title="Runs comparison")
        fig5.update_traces(textposition="outside")
        fig5.update_layout(height=350, margin=dict(l=10,r=10,t=30,b=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           yaxis=dict(gridcolor="#f0f0f0"), xaxis=dict(gridcolor="#f0f0f0"))
        st.plotly_chart(fig5, use_container_width=True)

with tab2:
    tb2 = (bowl.groupby(["player","team"])
           .agg(matches=("matches","sum"), wickets=("wickets","sum"),
                economy=("economy","mean"))
           .reset_index())
    tb2["economy"] = tb2["economy"].round(2)
    tb2 = tb2.sort_values("wickets", ascending=False).head(10).reset_index(drop=True)
    tb2.index += 1

    cc, cd = st.columns([3,2])
    with cc:
        st.dataframe(tb2[["player","team","matches","wickets","economy"]]
                     .rename(columns={"player":"Player","team":"Team",
                                      "matches":"Matches","wickets":"Wickets","economy":"Economy"}),
                     use_container_width=True, height=350)
    with cd:
        fig6 = px.scatter(tb2, x="economy", y="wickets", size="wickets",
                          color="team", hover_name="player", text="player",
                          labels={"economy":"Economy Rate","wickets":"Wickets"},
                          title="Wickets vs Economy")
        fig6.update_traces(textposition="top center", textfont_size=9)
        fig6.update_layout(height=350, margin=dict(l=10,r=10,t=30,b=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"))
        st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.caption("🏏 IPL Analytics Dashboard · Portfolio project · Synthetic data")
