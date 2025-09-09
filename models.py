from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table, Date
from sqlalchemy.orm import relationship, declarative_base
from datetime import date

Base = declarative_base()


class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    exercises = relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Workout(id={self.id}, name='{self.name}')>"


class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(String)

    workouts = relationship("WorkoutExercise", back_populates="exercise")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', muscle_group='{self.muscle_group}')>"


class WorkoutExercise(Base):
    __tablename__ = 'workout_exercises'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    note = Column(String)

    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workouts")
    sets = relationship(
        "Set", back_populates="workout_exercise", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkoutExercise(workout_id={self.workout_id}, exercise_id={self.exercise_id})>"


class Set(Base):
    __tablename__ = 'sets'

    id = Column(Integer, primary_key=True)
    workout_exercise_id = Column(Integer, ForeignKey(
        "workout_exercises.id"), nullable=False)
    # no = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    workout_exercise = relationship("WorkoutExercise", back_populates="sets")

    def __repr__(self):
        return f"<Set(id={self.id}, reps={self.reps}, weight={self.weight})>"


class PerformedSet(Base):
    __tablename__ = 'performed_sets'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    performed_date = Column(Date, default=date.today, nullable=False)
    set_no = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    workout = relationship("Workout")
    exercise = relationship("Exercise")

    def __repr__(self):
        return (
            f"<PerformedSet(id={self.id}, date={self.performed_date}, "
            f"workout_id={self.workout_id}, exercise_id={self.exercise_id}, "
            f"reps={self.reps}, weight={self.weight})>"
        )
