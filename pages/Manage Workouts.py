import streamlit as st
from training_db import TrainingDB  # adjust if your file is named differently

db = TrainingDB()

st.set_page_config(page_title="Workout Manager", layout="wide")
st.title("Workout Manager")


# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Workouts", "Exercises"])


# --- WORKOUTS PAGE ---
if page == "Workouts":
    st.header("Workouts")

    # Add workout
    with st.expander("Add Workout"):
        new_name = st.text_input("Name", key="new_workout")
        if st.button("Create"):
            if new_name.strip():
                db.create_workout(new_name.strip())
                st.rerun()

    # list workouts
    workouts = db.get_all_workouts()
    for w in workouts:
        with st.expander(f"{w.name} (ID: {w.id})"):
            # rename
            new_name = st.text_input(
                f"Rename", value=w.name, key=f"rename_{w.id}")

            with st.container(horizontal=True):
                if st.button("Update", key=f"update_{w.id}"):
                    db.rename_workout(w.id, new_name)
                    st.rerun()

                if st.button("Delete", key=f"delete_{w.id}"):
                    db.delete_workout(w.id)
                    st.rerun()

            workout_exercises = db.get_workout_exercises(w.id)

            # add exercise
            exercises = db.get_all_exercises()
            if exercises:
                ex_map = {ex.id: ex.id for ex in exercises}
                chosen_ex = st.selectbox("Exercise", list(
                    ex_map.keys()), key=f"addex_{w.id}")
                note = st.text_input("Note", key=f"note_{w.id}")
                if st.button("Add", key=f"addbtn_{w.id}"):
                    db.add_exercise_to_workout(w.id, ex_map[chosen_ex], note)
                    st.rerun()

            # Display workout exercises and sets (NO nested expanders)
            for we in workout_exercises:
                st.markdown("---")  # separator for clarity

                ex = [ex for ex in exercises if ex.id == we.exercise_id][0]

                st.markdown(
                    f"**{ex.data_dict.get("name", "")}** (WE_ID: {we.id})")
                # Remove exercise
                if st.button(f"🗑 Trash {ex.id}", key=f"rem_{we.id}"):
                    db.remove_exercise_from_workout(we.id)
                    st.rerun()

                st.caption(f"Note: {we.note}")

                # Sets
                st.write("Reps / Weight (kg)")

                sets = db.get_sets_for_workout_exercise(we.id)
                for s in sets:
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        reps = st.number_input(
                            "Reps", value=s.reps, key=f"reps_{s.id}", label_visibility="collapsed")
                    with c2:
                        weight = st.number_input(
                            "Weight", value=float(s.weight), key=f"w_{s.id}", label_visibility="collapsed")
                    with c3:
                        with st.container(horizontal=True):
                            if st.button("Update", key=f"up_set_{s.id}"):
                                db.update_set(s.id, reps, weight)
                                st.rerun()
                            if st.button("Remove", key=f"del_set_{s.id}"):
                                db.delete_set(s.id)
                                st.rerun()

                # st.write("Reps / Weight kg")
                # for s in sets:
                #     c1, c2 = st.columns([3, 1])
                #     with c1:
                #         with st.container(horizontal=True):
                #             reps = st.number_input(
                #                 "Reps", value=s.reps, key=f"reps_{s.id}", label_visibility="collapsed")
                #             weight = st.number_input(
                #                 "Weight", value=float(s.weight), key=f"w_{s.id}", label_visibility="collapsed")
                #     with c2:
                #         with st.container(horizontal=True):
                #             if st.button("Update", key=f"up_set_{s.id}"):
                #                 db.update_set(s.id, reps, weight)
                #                 st.rerun()
                #             if st.button("Remove", key=f"del_set_{s.id}"):
                #                 db.delete_set(s.id)
                #                 st.rerun()

                # add set
                "Add Set"
                c1, c2 = st.columns([3, 1])
                with c1:
                    with st.container(horizontal=True):
                        reps_new = st.number_input(
                            "Reps", min_value=1, step=1, key=f"new_reps_{we.id}", label_visibility="collapsed")
                        weight_new = st.number_input(
                            "Weight", min_value=0.0, step=0.5, key=f"new_w_{we.id}", label_visibility="collapsed")
                with c2:
                    if st.button("Add", key=f"addset_{we.id}"):
                        db.add_set(we.id, reps_new, weight_new)
                        st.rerun()


# --- EXERCISES PAGE ---
elif page == "Exercises":
    st.header("Exercises")

    # Add exercise
    with st.expander("➕ Add Exercise"):
        ex_name = st.text_input("Exercise name", key="new_ex")
        if st.button("Create Exercise"):
            from models import Exercise
            with db.get_session() as session:
                ex = Exercise(name=ex_name.strip())
                session.add(ex)
                session.commit()
            st.success(f"Exercise '{ex_name}' created!")
            st.rerun()

    # List all exercises
    exercises = db.get_all_exercises()
    for ex in exercises:
        st.write(f"🏋️ {ex.id} (ID: {ex.id})")
