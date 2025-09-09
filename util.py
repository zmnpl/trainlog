bizeps = "💪"
lifter = "🏋️"
cal = "📅"

# st.markdown("---")  # divider between exercises

# # --- Workout history ---
# st.subheader("📊 Workout History")

# with db.get_session() as session:
#     from models import PerformedSet
#     logs = (
#         session.query(PerformedSet)
#         .filter(PerformedSet.workout_id == workout_id)
#         .order_by(PerformedSet.performed_date.desc())
#         .all()
#     )

# if logs:
#     for log in logs:
#         ex_name = ex_lookup.get(log.exercise_id, f"ExID {log.exercise_id}")
#         st.write(
#             f"📅 {log.performed_date} — **{ex_name}**: "
#             f"{log.reps} reps @ {log.weight} kg"
#         )
# else:
#     st.info("No logs yet for this workout.")
