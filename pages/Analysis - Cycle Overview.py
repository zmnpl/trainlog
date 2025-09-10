import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import util
import streamlit as st
from training_db import TrainingDB

st.set_page_config(layout="wide", page_title="Analysis")

if "datum" not in st.session_state:
    st.session_state.datum = datetime.now().date() - timedelta(days=28)


def color_coding(row):
    color = ['background-color:black'] * len(row)
    if row[1] == 'Ring Chin-Up':
        color = ['background-color:gray'] * len(row)
    return color


cols = []


def weekday_colors(df):
    bg_colors = []
    for col in df.index:
        color = 'background-color: #0E1117'
        if 'Monday' in col or 'Wednesday' in col or 'Friday' in col or 'Sunday' in col:
            color = 'background-color: #262730'
        bg_colors.append(color)
    return bg_colors


def make_analysis():
    db = TrainingDB()
    # df = db.get_cycle_view(util.get_date_string(st.session_state.datum))
    df = db.get_cycle_view(st.session_state.datum)
    exercises = df.reset_index()['name'].unique()

    foo = df.sort_values(['year_cw', 'name'], ascending=[False, True])
    foo = foo.fillna('').astype(str)
    foo = foo.style.highlight_max(axis=1).apply(
        weekday_colors, axis=1).format(precision=0, thousands="", decimal=".")
    st.dataframe(foo)

    for e in exercises:
        df_e = df.xs(e, level=0, axis=0, drop_level=False).fillna(
            '').astype(str)
        # .format(precision=0, thousands="", decimal=".")#.highlight_null(props="--gdg-text-medium: transparent;")
        styled = df_e.style.highlight_max(axis=1).apply(weekday_colors, axis=1)
        styled = df_e.style.highlight_max(axis=1).apply(weekday_colors, axis=1).format(
            # .highlight_null(props="--gdg-text-medium: transparent;")
            precision=0, thousands="", decimal=".")

        st.header(e)
        st.dataframe(styled)


date = st.date_input("Date", key='datum')
st.write(st.session_state.datum)
make_analysis()
