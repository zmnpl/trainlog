import streamlit as st
import pandas as pd
import util
from training_db import TrainingDB

db = TrainingDB()
st.title("Lifetime Reps")
st.write(db.raw_query(
    "select exercise_id, sum(reps) as reps from performed_sets group by exercise_id order by reps desc"))
