import pandas as pd
import numpy as np
import os

np.random.seed(42)

TEAMS = ["Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
         "Kolkata Knight Riders", "Delhi Capitals", "Sunrisers Hyderabad",
         "Rajasthan Royals", "Punjab Kings"]

VENUES = ["Wankhede Stadium", "MA Chidambaram Stadium", "Eden Gardens",
          "M. Chinnaswamy Stadium", "Arun Jaitley Stadium", "Rajiv Gandhi Intl Stadium",
          "Sawai Mansingh Stadium", "PCA Stadium Mohali"]

BATSMEN = [
    ("Virat Kohli", "Royal Challengers Bangalore"),
    ("Rohit Sharma", "Mumbai Indians"),
    ("MS Dhoni", "Chennai Super Kings"),
    ("AB de Villiers", "Royal Challengers Bangalore"),
    ("David Warner", "Sunrisers Hyderabad"),
    ("Shikhar Dhawan", "Delhi Capitals"),
    ("KL Rahul", "Punjab Kings"),
    ("Suresh Raina", "Chennai Super Kings"),
    ("Hardik Pandya", "Mumbai Indians"),
    ("Andre Russell", "Kolkata Knight Riders"),
    ("Jos Buttler", "Rajasthan Royals"),
    ("Shubman Gill", "Kolkata Knight Riders"),
]

BOWLERS = [
    ("Lasith Malinga", "Mumbai Indians"),
    ("Jasprit Bumrah", "Mumbai Indians"),
    ("Dwayne Bravo", "Chennai Super Kings"),
    ("Yuzvendra Chahal", "Royal Challengers Bangalore"),
    ("Rashid Khan", "Sunrisers Hyderabad"),
    ("Amit Mishra", "Delhi Capitals"),
    ("Ravindra Jadeja", "Chennai Super Kings"),
    ("Sunil Narine", "Kolkata Knight Riders"),
    ("Kagiso Rabada", "Delhi Capitals"),
    ("Bhuvneshwar Kumar", "Sunrisers Hyderabad"),
]

SEASONS = list(range(2008, 2024))

# ── matches.csv ──────────────────────────────────────────────────────────────
rows = []
match_id = 1
for season in SEASONS:
    n_matches = 60 if season < 2022 else 74
    for _ in range(n_matches):
        t1, t2 = np.random.choice(TEAMS, 2, replace=False)
        venue = np.random.choice(VENUES)
        toss_winner = np.random.choice([t1, t2])
        toss_decision = np.random.choice(["bat", "field"], p=[0.55, 0.45])
        score1 = int(np.random.normal(165, 18))
        score2 = int(np.random.normal(158, 18))
        score1 = max(80, min(score1, 263))
        score2 = max(80, min(score2, 263))
        winner = t1 if score1 > score2 else t2
        win_by_runs = abs(score1 - score2) if winner == t1 else 0
        win_by_wkts = np.random.randint(1, 10) if winner == t2 else 0
        rows.append({
            "match_id": match_id,
            "season": season,
            "date": f"{season}-04-{np.random.randint(1,30):02d}",
            "venue": venue,
            "team1": t1,
            "team2": t2,
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "team1_score": score1,
            "team2_score": score2,
            "winner": winner,
            "win_by_runs": win_by_runs,
            "win_by_wickets": win_by_wkts,
        })
        match_id += 1

matches = pd.DataFrame(rows)
matches.to_csv("/home/claude/ipl_dashboard/matches.csv", index=False)
print(f"✅  matches.csv — {len(matches)} rows")

# ── batting.csv ───────────────────────────────────────────────────────────────
bat_rows = []
for season in SEASONS:
    for name, team in BATSMEN:
        innings = np.random.randint(10, 18)
        runs    = int(np.random.normal(420, 180))
        runs    = max(50, min(runs, 973))
        avg     = round(runs / innings, 1)
        sr      = round(np.random.uniform(118, 195), 1)
        fours   = np.random.randint(30, 80)
        sixes   = np.random.randint(10, 50)
        fifties = np.random.randint(1, 6)
        hundreds = 1 if runs > 700 else 0
        bat_rows.append({"season": season, "player": name, "team": team,
                         "innings": innings, "runs": runs, "average": avg,
                         "strike_rate": sr, "fours": fours, "sixes": sixes,
                         "fifties": fifties, "hundreds": hundreds})

batting = pd.DataFrame(bat_rows)
batting.to_csv("/home/claude/ipl_dashboard/batting.csv", index=False)
print(f"✅  batting.csv  — {len(batting)} rows")

# ── bowling.csv ───────────────────────────────────────────────────────────────
bowl_rows = []
for season in SEASONS:
    for name, team in BOWLERS:
        matches_played = np.random.randint(10, 17)
        wickets = np.random.randint(8, 28)
        economy = round(np.random.uniform(6.5, 9.8), 2)
        avg     = round(np.random.uniform(18, 32), 1)
        best    = f"{np.random.randint(2,6)}/{np.random.randint(10,45)}"
        bowl_rows.append({"season": season, "player": name, "team": team,
                          "matches": matches_played, "wickets": wickets,
                          "economy": economy, "average": avg, "best": best})

bowling = pd.DataFrame(bowl_rows)
bowling.to_csv("/home/claude/ipl_dashboard/bowling.csv", index=False)
print(f"✅  bowling.csv  — {len(bowling)} rows")
print("\nAll datasets generated successfully!")
