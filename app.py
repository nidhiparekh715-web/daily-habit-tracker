import streamlit as st
import json
import calendar
from datetime import datetime

FILE = "progress_calendar.json"

ACTIVITIES = [
    "Prayer",
    "Gym / Workout",
    "Study / Learning",
    "Work / Assignments",
    "Skincare (AM/PM)",
    "Meals",
    "Hydration",
    "Self-care",
    "Leisure / Hobby",
    "Reflection",
    "Sleep"
]

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

st.title("📅 Daily Habit Tracker")


# 🌙 Force Dark Theme
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

div[data-testid="stSidebar"] {
    background-color: #161B22;
}

label, .stCheckbox span {
    color: #FAFAFA !important;
}
</style>
""", unsafe_allow_html=True)


month = st.selectbox("Month", range(1, 13), index=datetime.now().month - 1)
year = st.number_input("Year", 2000, 2100, datetime.now().year)

key = f"{year}-{month:02d}"
data = load_data()

total_days = calendar.monthrange(year, month)[1]

# Create month if not exists
if key not in data:
    data[key] = {
        str(d): {activity: False for activity in ACTIVITIES}
        for d in range(1, total_days + 1)
    }
    save_data(data)

st.subheader("Select Day")
day = st.selectbox("Day", range(1, total_days + 1))

st.subheader(f"Habits for Day {day}")

for activity in ACTIVITIES:
    data[key][str(day)][activity] = st.checkbox(
        activity,
        value=data[key][str(day)][activity],
        key=f"{key}-{day}-{activity}"
    )

# ✅ Calculate performance AFTER all checkboxes
completed = sum(data[key][str(day)].values())
total = len(ACTIVITIES)
percent = completed / total if total else 0

bar_color = "#2ECC71" if percent >= 0.75 else "#F1C40F" if percent >= 0.4 else "#E74C3C"

dot = "🟢" if percent >= 0.75 else "🟡" if percent >= 0.4 else "🔴"
st.write(f"{dot} **Performance:** {completed}/{total} ({percent*100:.1f}%)")

st.markdown(f"""
<style>
div[role="progressbar"] > div {{
    background-color: {bar_color};
}}
</style>
""", unsafe_allow_html=True)

st.progress(percent)

save_data(data)

st.success("Your habits are saved ✔")
col1, col2 = st.columns(2)

# # 📊 Habit Strength Indicator (LEFT)
with col1:
    st.subheader("📊 Habit Strength Indicator")

    for activity in ACTIVITIES:
        completed_days = sum(
            data[key][str(d)][activity]
            for d in range(1, total_days + 1)
        )

        strength = completed_days / total_days if total_days else 0

        dot = "🟢" if strength >= 0.75 else "🟡" if strength >= 0.4 else "🔴"

        st.write(f"{dot} **{activity}** — {strength*100:.0f}%")
        st.progress(strength)


st.sidebar.subheader("🗓 Monthly Overview")

cols = st.sidebar.columns(7)
d = 1

while d <= total_days:
    for col in cols:
        if d > total_days:
            break

        score = sum(data[key][str(d)].values()) / total if total else 0

        emoji = "🟢" if score >= 0.75 else "🟡" if score >= 0.4 else "🔴"
        col.markdown(f"**{d} {emoji}**")
        d += 1

# 📈 Monthly Performance %
total_possible = total_days * len(ACTIVITIES)
total_completed = 0

for d in range(1, total_days + 1):
    total_completed += sum(data[key][str(d)].values())

monthly_percent = total_completed / total_possible if total_possible else 0

st.sidebar.subheader("📈 Monthly Performance")
st.sidebar.progress(monthly_percent)
st.sidebar.write(f"**{monthly_percent*100:.1f}% completed**")

# 🔥 Streak Counter
current_streak = 0
best_streak = 0
temp_streak = 0

for d in range(1, total_days + 1):
    day_score = sum(data[key][str(d)].values()) / len(ACTIVITIES)
    if day_score >= 0.5:
        temp_streak += 1
        best_streak = max(best_streak, temp_streak)
    else:
        temp_streak = 0

current_streak = temp_streak

st.sidebar.markdown("### 🔥 Streaks")
st.sidebar.write(f"🔥 Current: **{current_streak} days**")
st.sidebar.write(f"🏆 Best: **{best_streak} days**")

