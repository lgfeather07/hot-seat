import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hot Seat", layout="wide")

st.markdown("""
<style>
.block-container { padding-top: 2.5rem; max-width: 1100px; }
h1 { font-weight: 700; letter-spacing: -0.01em; margin-bottom: 0; }
.sub { color: #6f6a5d; margin: 4px 0 28px 0; font-size: 1rem; }
.card { border: 1px solid #d6d0c2; background: #fbf9f4; padding: 14px 16px; height: 100%; }
.card .rank { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: #8a8576; }
.card .name { font-size: 17px; font-weight: 600; margin-top: 4px; line-height: 1.2; }
.card .meta { color: #6f6a5d; font-size: 13px; margin-top: 2px; }
.card .pct { font-size: 34px; font-weight: 700; margin-top: 10px; }
.card .tier { font-size: 11px; letter-spacing: .08em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

from pathlib import Path
df = pd.read_csv(Path(__file__).parent / "hot_seat.csv")

def tier(p):
    if p >= 60: return "Blazing", "#9b2c1d"
    if p >= 30: return "Hot", "#b5651d"
    if p >= 10: return "Warm", "#8f7a1f"
    return "Stable", "#4d6a4d"

df["tier"] = df["hot_seat_pct"].apply(lambda p: tier(p)[0])

st.title("Hot Seat")
st.markdown(
    f"<div class='sub'>Estimated chance each NFL head coach is fired this season, "
    f"based on results and expectations. Updated {df['updated'].iloc[0]}.</div>",
    unsafe_allow_html=True,
)

# Top five
cols = st.columns(5)
for i, (col, (_, r)) in enumerate(zip(cols, df.head(5).iterrows()), start=1):
    label, color = tier(r["hot_seat_pct"])
    col.markdown(
        f"""<div class='card'>
        <div class='rank'>No. {i}</div>
        <div class='name'>{r['coach']}</div>
        <div class='meta'>{r['team']} &middot; {r['record']}</div>
        <div class='pct' style='color:{color}'>{r['hot_seat_pct']:.0f}%</div>
        <div class='tier' style='color:{color}'>{label}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("&nbsp;")
st.subheader("All coaches")

st.dataframe(
    df[["coach", "team", "record", "pt_diff", "vs_exp_pg", "tenure", "tier", "hot_seat_pct"]],
    column_config={
        "coach": "Coach",
        "team": "Team",
        "record": "Record",
        "pt_diff": st.column_config.NumberColumn("Point diff", format="%+d"),
        "vs_exp_pg": st.column_config.NumberColumn("Vs. spread / game", format="%+.1f"),
        "tenure": "Seasons with team",
        "tier": "Tier",
        "hot_seat_pct": st.column_config.ProgressColumn(
            "Fire probability", min_value=0, max_value=100, format="%.0f%%"),
    },
    hide_index=True,
    use_container_width="stretch",
)

st.markdown("---")
st.subheader("Method")
st.write(
    "Logistic regression trained on NFL coach seasons from 2010 to 2024. Inputs are win "
    "percentage, point differential, seasons with the team, last season's win percentage, "
    "and how the team has performed against the betting spread. Tested on one future "
    "season at a time, it averaged about 0.85 AUC, and its probabilities matched "
    "actual firing rates closely, predicting 34 overall firings compared to 34 actual firings."
)
st.write(
    "Limitations: contract buyouts, ownership, and off-field issues."
    " The numbers are a ranking of statistical risk, not a "
    "prediction of any team's decision."
)
st.caption("Game data from nflverse. Built by Logan Feather.")