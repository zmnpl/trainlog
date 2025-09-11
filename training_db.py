from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Workout, Exercise, WorkoutExercise, Set, PerformedSet
from datetime import date
from pathlib import Path
import os
import pandas as pd

homedir = Path.home()


class TrainingDB:
    def __init__(self, db_path=f"sqlite:///{os.path.join(homedir, "Documents", "training.db")}"):
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # bodges
    def raw_query(self, query):
        df = pd.read_sql_query(
            query, self.engine)
        return df

    def get_cycle_view(self, start_date):
        # start_date = get_week_start_date_string(weeks)
        selection = f"select name, set_no, reps, weight, year_cw, week_day, week_day_name from vw_workout_with_details  where performed_date >=:start_date order by name asc, year_cw asc, week_day asc, set_no asc"
        df = pd.read_sql_query(selection, self.engine, params={
                               'start_date': start_date})
        df = df.pivot_table(index=['name', 'year_cw'], columns=[
                            'week_day_name', 'week_day', 'set_no'], values=['reps', 'weight'], aggfunc='sum')
        df = df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(
            2, 3, axis=1).sort_index(level=[1, 2], axis=1).droplevel(1, axis=1)
        df = df.sort_index(level=[0, 1], axis=0)
        df = df.rename(columns={'weight': 'kg'})
        return df

    # actual crud

    def get_session(self):
        return self.Session()

    def create_workout(self, name: str):
        with self.get_session() as session:
            workout = Workout(name=name)
            session.add(workout)
            session.commit()
            return workout

    def rename_workout(self, workout_id: int, new_name: str):
        with self.get_session() as session:
            workout = session.get(Workout, workout_id)
            workout.name = new_name
            session.commit()

    def delete_workout(self, workout_id: int):
        with self.get_session() as session:
            workout = session.get(Workout, workout_id)
            session.delete(workout)
            session.commit()

    def get_all_workouts(self):
        with self.get_session() as session:
            return session.query(Workout).all()

    def get_workout_by_id(self, workout_id: int):
        with self.get_session() as session:
            return session.get(Workout, workout_id)

    def get_all_exercises(self):
        with self.get_session() as session:
            return session.query(Exercise).all()

    def add_exercise_to_workout(self, workout_id: int, exercise_id: str, note: str = ""):
        with self.get_session() as session:
            exists = session.query(WorkoutExercise).filter_by(
                workout_id=workout_id, exercise_id=exercise_id
            ).first()
            if exists:
                return None
            we = WorkoutExercise(workout_id=workout_id,
                                 exercise_id=exercise_id, note=note)
            session.add(we)
            session.commit()
            return we

    def remove_exercise_from_workout(self, workout_exercise_id: str):
        with self.get_session() as session:
            we = session.get(WorkoutExercise, workout_exercise_id)
            session.delete(we)
            session.commit()

    def get_workout_exercises(self, workout_id: int):
        with self.get_session() as session:
            return session.query(WorkoutExercise).filter_by(workout_id=workout_id).all()

    def get_sets_for_workout_exercise(self, workout_exercise_id: str):
        with self.get_session() as session:
            return session.query(Set).filter_by(workout_exercise_id=workout_exercise_id).all()

    def add_set(self, workout_exercise_id: str, reps: int, weight: float):
        with self.get_session() as session:
            s = Set(workout_exercise_id=workout_exercise_id,
                    reps=reps, weight=weight)
            session.add(s)
            session.commit()

    def update_set(self, set_id: int, reps: int, weight: float):
        with self.get_session() as session:
            s = session.get(Set, set_id)
            s.reps = reps
            s.weight = weight
            session.commit()

    def delete_set(self, set_id: int):
        with self.get_session() as session:
            s = session.get(Set, set_id)
            session.delete(s)
            session.commit()

    def get_all_performed_sets(self):
        with self.get_session() as session:
            return session.query(PerformedSet).all()

    def log_performed_set(self, workout_id: int, exercise_id: str, set_no: int, reps: int, weight: float, performed_date: date):
        with self.get_session() as session:
            p = PerformedSet(
                workout_id=workout_id,
                exercise_id=exercise_id,
                set_no=set_no,
                reps=reps,
                weight=weight,
                performed_date=performed_date
            )
            session.add(p)
            session.commit()
