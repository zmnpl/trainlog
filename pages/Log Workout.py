import streamlit as st
from datetime import date
from training_db import TrainingDB
from models import Exercise

db = TrainingDB()

st.set_page_config(page_title="Workout Logger", layout="wide")
st.title("Workout Logger")


# select a workout
workouts = db.get_all_workouts()
if not workouts:
    st.warning("Do you even workout, bro?")
    st.stop()

workout_map = {w.name: w.id for w in workouts}
workout_name = st.selectbox("Select Workout", list(workout_map.keys()))
workout_id = workout_map[workout_name]


# exercises for this workout
workout_exercises = db.get_workout_exercises(workout_id)
if not workout_exercises:
    st.warning(
        "No exercises here.")
    st.stop()

all_exercises = db.get_all_exercises()
ex_lookup = {ex.id: ex.id for ex in all_exercises}

perf_date = st.date_input(
    f"Date", value=date.today(), key=f"date_{workout_id}"
)

if "setlog" not in st.session_state:
    st.session_state.setlog = []

for we in workout_exercises:
    st.markdown("---")

    ex_name = ex_lookup.get(we.exercise_id, f"ExID {we.exercise_id}")
    st.markdown(f"## {ex_name}")

    sets = db.get_sets_for_workout_exercise(we.id)
    if not sets:
        st.caption("No sets defined for this exercise.")
        continue

    st.write("Reps / Weight (kg)")

    set_no = 0
    for s in sets:
        set_no += 1

        if f"logged_{s.id}" not in st.session_state:
            st.session_state[f"logged_{s.id}"] = False

        c1, c2, c3, c4 = st.columns([1, 10, 10, 4])
        with c1:
            st.write(set_no)
        with c2:
            reps = st.number_input(
                f"Reps_{s.id}", min_value=1, step=1, value=s.reps, label_visibility="collapsed", key=f"reps_{s.id}", disabled=st.session_state[f"logged_{s.id}"]
            )
        with c3:
            weight = st.number_input(
                f"Weight_{s.id}", min_value=0.0, step=0.5, value=float(s.weight), label_visibility="collapsed", key=f"weight_{s.id}", disabled=st.session_state[f"logged_{s.id}"]
            )
        with c4:
            with st.container(horizontal=True):
                if st.button(f"✅ Done", key=f"log_{s.id}"):

                    db.log_performed_set(
                        workout_id=workout_id,
                        exercise_id=we.exercise_id,
                        set_no=set_no,
                        reps=reps,
                        weight=weight,
                        performed_date=perf_date,
                    )
                    st.session_state[f"logged_{s.id}"] = True

                    st.session_state.setlog.append(
                        f"Set {set_no}:\t{reps:2d} @ {weight} kg for {ex_name}")

                    st.rerun()

st.markdown("---")  # divider between exercises

for s in st.session_state.setlog:
    st.write(f":green[{s}]")
