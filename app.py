import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hot Seat", page_icon="🔥", layout="wide")

df = pd.read_csv("hot_seat.csv")

def tier(p):
    if p >= 60: return "🔥 On Fire"
    if p >= 30: return "🌶️ Hot"
    if p >= 10: return "🟡 Warm"
    return "🧊 Cold"

df["status"] = df["hot_seat_pct"].apply(tier)

st.title("🔥 Hot Seat")
st.caption("A statistical estimate of how close each NFL head coach is to being fired. "
           f"Last updated {df['updated'].iloc[0]}.")

# Top 5 spotlight
cols = st.columns(5)
for col, (_, row) in zip(cols, df.head(5).iterrows()):
    col.metric(f"{row['coach']} ({row['team']})", f"{row['hot_seat_pct']:.0f}%", row["record"])

st.subheader("Full leaderboard")
st.dataframe(
    df[["status", "coach", "team", "record", "pt_diff", "vs_exp_pg", "tenure", "hot_seat_pct"]],
    column_config={
        "status": "Status",
        "coach": "Coach",
        "team": "Team",
        "record": "Record",
        "pt_diff": "Point diff",
        "vs_exp_pg": "vs. spread / game",
        "tenure": "Seasons w/ team",
        "hot_seat_pct": st.column_config.ProgressColumn(
            "Fire probability", min_value=0, max_value=100, format="%.0f%%"),
    },
    hide_index=True,
    use_container_width=True,
)

with st.expander("How it works"):
    st.write(
        "The model is a logistic regression trained on NFL coach seasons from 2010 to 2024. "
        "It uses win percentage, point differential, tenure, performance against the betting "
        "spread, and last season's record. It can't see contract buyouts, owner patience, or "
        "off-field issues, so treat it as a ranking of statistical risk, not a prediction "
        "of any team's decision."
    )