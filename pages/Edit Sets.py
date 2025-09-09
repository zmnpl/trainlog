import streamlit as st
import pandas as pd
from datetime import date
from training_db import TrainingDB
from models import Exercise, PerformedSet

db = TrainingDB()

st.set_page_config(page_title="Edit Sets", layout="wide")
st.title("Edit Sets")


# --- Select date ---
chosen_date = st.date_input("Select Date", value=date.today())


# --- Load performed sets for that date ---
with db.get_session() as session:
    logs = (
        session.query(PerformedSet)
        .filter(PerformedSet.performed_date == chosen_date)
        .all()
    )

if not logs:
    st.info("No sets here.")
    st.stop()


# --- Build DataFrame for editing ---
all_exercises = {ex.id: ex.name for ex in db.get_all_exercises()}
all_workouts = {w.id: w.name for w in db.get_all_workouts()}

df = pd.DataFrame(
    [
        {
            "id": log.id,
            "workout": all_workouts.get(log.workout_id, f"W{log.workout_id}"),
            "exercise": all_exercises.get(log.exercise_id, f"E{log.exercise_id}"),
            "reps": log.reps,
            "weight": float(log.weight),
            "date": log.performed_date,
        }
        for log in logs
    ]
)

edited_df = st.data_editor(
    df,
    hide_index=True,
    num_rows="fixed",
    column_config={
        "id": st.column_config.Column("ID", disabled=True),
        "workout": st.column_config.Column("Workout", disabled=True),
        "exercise": st.column_config.Column("Exercise", disabled=True),
        "date": st.column_config.DateColumn("Date", disabled=True),
        "reps": st.column_config.NumberColumn("Reps", min_value=1, step=1),
        "weight": st.column_config.NumberColumn("Weight", min_value=0.0, step=0.5),
    },
    use_container_width=True,
)

if st.button("💾 Save"):
    with db.get_session() as session:
        for _, row in edited_df.iterrows():
            s = session.get(PerformedSet, int(row["id"]))
            if s:
                s.reps = int(row["reps"])
                s.weight = float(row["weight"])
        session.commit()
    st.success("✅ saved!")
