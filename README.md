# 🏏 IPL Analytics Dashboard

An interactive cricket analytics dashboard built with **Streamlit** and **Plotly**, analyzing IPL data across 16 seasons (2008–2024).

## 🔍 Features

- **KPI cards** — matches played, average scores, top team, total sixes
- **Wins by team** — horizontal bar chart with color scale
- **Toss decision split** — donut chart (bat vs field)
- **Score trend** — average first-innings runs per season (line chart)
- **Venue analysis** — matches played per ground
- **Top batsmen** — runs, average, 4s, 6s, 50s, 100s with interactive table
- **Top bowlers** — wickets vs economy scatter plot
- **Sidebar filters** — filter by season and team dynamically

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core language |
| Streamlit | Web app framework |
| Plotly | Interactive charts |
| Pandas | Data manipulation |
| NumPy | Synthetic data generation |

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ipl-dashboard.git
cd ipl-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python generate_data.py

# 4. Launch the dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** — live in ~2 minutes!

> **Note:** Add `generate_data.py` execution in `app.py` startup, or commit the CSV files directly to GitHub for cloud deployment.

## 📁 Project Structure

```
ipl_dashboard/
├── app.py              # Main Streamlit dashboard
├── generate_data.py    # Synthetic data generator
├── matches.csv         # Match results (988 rows)
├── batting.csv         # Batting stats (192 rows)
├── bowling.csv         # Bowling stats (160 rows)
├── requirements.txt    # Python dependencies
└── README.md
```

## 📊 Dataset

This project uses a **synthetic dataset** generated to mimic real IPL statistics. To use real data, download from:
- [Kaggle — IPL Complete Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)

## 💡 Key Insights (from synthetic data)

- Mumbai Indians lead with the most wins across seasons
- Teams increasingly choose to field first after winning the toss
- Average first-innings scores have risen from ~148 (2008) to ~176 (2023)
- Wankhede Stadium hosts the most high-scoring matches

## 🧑‍💻 Author

Built as a portfolio project to demonstrate data engineering, EDA, and dashboard development skills.

---
⭐ If you found this useful, give it a star!
