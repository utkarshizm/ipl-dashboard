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
tab1, tab2, tab3 = st.tabs(["🏏 Top Batsmen", "⚾ Top Bowlers", "⚔️ Head to Head"])

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

with tab3:
    all_teams_h2h = sorted(matches["team1"].unique())

    hcol1, hcol2 = st.columns(2)
    with hcol1:
        team_a = st.selectbox("Team A", all_teams_h2h,
                              index=all_teams_h2h.index("Mumbai Indians") if "Mumbai Indians" in all_teams_h2h else 0)
    with hcol2:
        default_b = "Chennai Super Kings" if "Chennai Super Kings" in all_teams_h2h else all_teams_h2h[1]
        team_b = st.selectbox("Team B", [t for t in all_teams_h2h if t != team_a],
                              index=[t for t in all_teams_h2h if t != team_a].index(default_b)
                              if default_b in [t for t in all_teams_h2h if t != team_a] else 0)

    # filter matches between these two teams only
    h2h = matches[
        ((matches["team1"] == team_a) & (matches["team2"] == team_b)) |
        ((matches["team1"] == team_b) & (matches["team2"] == team_a))
    ].copy()

    if len(h2h) == 0:
        st.info("No matches found between these two teams.")
    else:
        a_wins = int((h2h["winner"] == team_a).sum())
        b_wins = int((h2h["winner"] == team_b).sum())
        total  = len(h2h)
        a_pct  = round(a_wins / total * 100, 1)
        b_pct  = round(b_wins / total * 100, 1)

        # ── KPIs ──────────────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4, k5 = st.columns(5)
        for col, val, lbl in zip(
            [k1, k2, k3, k4, k5],
            [total, a_wins, b_wins, f"{a_pct}%", f"{b_pct}%"],
            ["Total Matches", f"{team_a.split()[0]} Wins", f"{team_b.split()[0]} Wins",
             f"{team_a.split()[0]} Win %", f"{team_b.split()[0]} Win %"]
        ):
            col.markdown(
                f'<div class="metric-card"><div class="metric-value">{val}</div>'
                f'<div class="metric-label">{lbl}</div></div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Wins per season grouped bar ────────────────────────────────────────
        season_wins = []
        for season, grp in h2h.groupby("season"):
            season_wins.append({
                "season": season,
                team_a: int((grp["winner"] == team_a).sum()),
                team_b: int((grp["winner"] == team_b).sum()),
            })
        sw = pd.DataFrame(season_wins)

        import plotly.graph_objects as go

        fig_h1 = go.Figure()
        fig_h1.add_trace(go.Bar(name=team_a, x=sw["season"], y=sw[team_a],
                                marker_color="#3b82f6", text=sw[team_a], textposition="outside"))
        fig_h1.add_trace(go.Bar(name=team_b, x=sw["season"], y=sw[team_b],
                                marker_color="#f59e0b", text=sw[team_b], textposition="outside"))
        fig_h1.update_layout(
            barmode="group", title=f"{team_a.split()[0]} vs {team_b.split()[0]} — Wins per Season",
            height=360, margin=dict(l=10,r=10,t=45,b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", y=1.12),
            xaxis=dict(tickmode="linear", gridcolor="#f0f0f0", title="Season"),
            yaxis=dict(gridcolor="#f0f0f0", title="Wins", dtick=1),
        )
        st.plotly_chart(fig_h1, use_container_width=True)

        # ── Overall win share donut + avg scores side by side ─────────────────
        dc1, dc2 = st.columns(2)

        with dc1:
            st.markdown('<div class="section-title">🏆 Overall Win Share</div>', unsafe_allow_html=True)
            fig_h2 = go.Figure(go.Pie(
                labels=[team_a, team_b],
                values=[a_wins, b_wins],
                hole=0.55,
                marker_colors=["#3b82f6","#f59e0b"],
                textinfo="percent+label",
                pull=[0.04, 0.04],
            ))
            fig_h2.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10),
                                 paper_bgcolor="white",
                                 legend=dict(orientation="h", y=-0.05))
            st.plotly_chart(fig_h2, use_container_width=True)

        with dc2:
            st.markdown('<div class="section-title">📊 Avg Score When Batting First</div>', unsafe_allow_html=True)
            a_bat_first = h2h[h2h["team1"] == team_a]["team1_score"].tolist() + \
                          h2h[h2h["team2"] == team_a]["team2_score"].tolist()
            b_bat_first = h2h[h2h["team1"] == team_b]["team1_score"].tolist() + \
                          h2h[h2h["team2"] == team_b]["team2_score"].tolist()
            avg_a = round(sum(a_bat_first)/len(a_bat_first), 1) if a_bat_first else 0
            avg_b = round(sum(b_bat_first)/len(b_bat_first), 1) if b_bat_first else 0
            fig_h3 = go.Figure(go.Bar(
                x=[team_a.split()[0] + " " + team_a.split()[1],
                   team_b.split()[0] + " " + team_b.split()[1]],
                y=[avg_a, avg_b],
                marker_color=["#3b82f6","#f59e0b"],
                text=[avg_a, avg_b], textposition="outside",
            ))
            fig_h3.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10),
                                 plot_bgcolor="white", paper_bgcolor="white",
                                 yaxis=dict(gridcolor="#f0f0f0", range=[0, max(avg_a,avg_b)+20]),
                                 xaxis=dict(gridcolor="#f0f0f0"))
            st.plotly_chart(fig_h3, use_container_width=True)

        # ── Win streak tracker ────────────────────────────────────────────────
        st.markdown('<div class="section-title">📅 Match-by-Match Result Timeline</div>', unsafe_allow_html=True)
        h2h_sorted = h2h.sort_values("season").reset_index(drop=True)
        h2h_sorted["result"] = h2h_sorted["winner"].apply(
            lambda w: 1 if w == team_a else -1
        )
        h2h_sorted["match_num"] = range(1, len(h2h_sorted)+1)
        h2h_sorted["color"] = h2h_sorted["result"].apply(
            lambda r: "#3b82f6" if r == 1 else "#f59e0b"
        )
        h2h_sorted["label"] = h2h_sorted["winner"].apply(
            lambda w: f"{team_a.split()[0]} won" if w == team_a else f"{team_b.split()[0]} won"
        )

        fig_h4 = go.Figure()
        fig_h4.add_trace(go.Bar(
            x=h2h_sorted["match_num"],
            y=h2h_sorted["result"],
            marker_color=h2h_sorted["color"],
            text=h2h_sorted["season"],
            textposition="outside",
            hovertext=h2h_sorted["label"],
            hoverinfo="text",
            name="Result"
        ))
        fig_h4.add_hline(y=0, line_dash="dot", line_color="gray", line_width=1)
        fig_h4.update_layout(
            height=280,
            margin=dict(l=10,r=10,t=10,b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="Match number", gridcolor="#f0f0f0"),
            yaxis=dict(title="", tickvals=[-1,1],
                       ticktext=[f"{team_b.split()[0]} won", f"{team_a.split()[0]} won"],
                       gridcolor="#f0f0f0"),
            showlegend=False,
            annotations=[
                dict(x=0.01, y=0.95, xref="paper", yref="paper",
                     text=f"🔵 {team_a.split()[0]}", showarrow=False,
                     font=dict(color="#3b82f6", size=12)),
                dict(x=0.12, y=0.95, xref="paper", yref="paper",
                     text=f"🟡 {team_b.split()[0]}", showarrow=False,
                     font=dict(color="#f59e0b", size=12)),
            ]
        )
        st.plotly_chart(fig_h4, use_container_width=True)

        # ── Recent form table ──────────────────────────────────────────────────
        st.markdown('<div class="section-title">🗂️ Recent Matches</div>', unsafe_allow_html=True)
        recent = h2h_sorted.sort_values("season", ascending=False).head(10)[
            ["season","venue","team1","team2","team1_score","team2_score","winner"]
        ].rename(columns={"season":"Season","venue":"Venue","team1":"Team 1","team2":"Team 2",
                          "team1_score":"Score 1","team2_score":"Score 2","winner":"Winner"})
        st.dataframe(recent, use_container_width=True, hide_index=True)

