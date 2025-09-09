import streamlit as st
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Workout, Exercise, WorkoutExercise, Set, PerformedSet

# --- Setup DB ---
engine = create_engine("sqlite:///workouts.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

st.set_page_config(page_title="Workout Logger")  # , layout="wide")
st.title("📆 Workout Logger")

session = Session()

# --- Choose Workout Template ---
workouts = session.query(Workout).all()
workout_options = {w.name: w.id for w in workouts}

if not workouts:
    st.warning("No workouts found. Please define one first.")
    st.stop()

selected_workout_name = st.selectbox(
    "Select Workout", list(workout_options.keys()))
selected_workout = session.query(Workout).get(
    workout_options[selected_workout_name])

# --- Date of Workout ---
workout_date = st.date_input("Workout Date", date.today())

# --- Load Assigned Exercises ---
assigned_exercises = (
    session.query(WorkoutExercise)
    .filter_by(workout_id=selected_workout.id)
    .all()
)

if not assigned_exercises:
    st.warning("This workout has no exercises assigned.")
    st.stop()

# --- State to hold inputs before saving ---
if "performed_sets" not in st.session_state:
    st.session_state.performed_sets = []

# --- Loop over Exercises ---
st.header(f"🏋️ Logging: {selected_workout.name}")

for we in assigned_exercises:
    exercise = we.exercise
    st.subheader(f"💪 {exercise.name} (unknown muscle)")
    st.caption(we.note or "No note")

    # Template sets
    template_sets = session.query(Set).filter_by(
        workout_exercise_id=we.id).all()
    if not template_sets:
        st.info("No sets defined for this exercise — you can still log manually.")

    set_count = len(template_sets) or 1  # Fallback to at least 1 input row

    for i in range(set_count):
        t_set = template_sets[i] if i < len(template_sets) else None

        col1, col2 = st.columns(2)
        with col1:
            reps = st.number_input(
                f"Reps (Set {i+1}) - {exercise.name}",
                min_value=1,
                max_value=100,
                value=t_set.reps if t_set else 10,
                key=f"reps_{we.id}_{i}",
            )
        with col2:
            weight = st.number_input(
                f"Weight (kg) (Set {i+1}) - {exercise.name}",
                min_value=0.0,
                max_value=1000.0,
                value=t_set.weight if t_set else 20.0,
                key=f"weight_{we.id}_{i}",
            )

        # Collect in session state
        st.session_state.performed_sets.append({
            "workout_id": selected_workout.id,
            "exercise_id": exercise.id,
            "performed_date": workout_date,
            "reps": reps,
            "weight": weight
        })

# --- Save Button ---
if st.button("💾 Save Workout Log"):
    saved = 0
    for entry in st.session_state.performed_sets:
        if entry["reps"] > 0:
            pset = PerformedSet(
                workout_id=entry["workout_id"],
                exercise_id=entry["exercise_id"],
                performed_date=entry["performed_date"],
                reps=entry["reps"],
                weight=entry["weight"]
            )
            session.add(pset)
            saved += 1

    session.commit()
    session.close()
    st.success(f"✅ Saved {saved} performed sets.")
    st.session_state.performed_sets = []
