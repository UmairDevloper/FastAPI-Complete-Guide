"""
===========================================================
SQLAlchemy Many-to-Many Relationship — Complete Guide
===========================================================

Definition:
A many-to-many relationship occurs when multiple records in one
table relate to multiple records in another table.

Example:
A student can enroll in many courses.
A course can have many students.

To implement this in SQLAlchemy:
We use an association table (junction table).

This file includes:
- Engine setup
- Table creation
- Many-to-many relationship
- Random data insertion
- Querying data
- Explanation inside comments

You can run this file directly.
"""

# =============================
# Imports
# =============================
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import random

# =============================
# Engine Setup
# =============================
"""
The engine connects Python to the database.
SQLite is used for simplicity.
Connection pooling is automatically enabled.
"""

engine = create_engine("sqlite:///many_to_many.db")

Base = declarative_base()

# =============================
# Association Table
# =============================
"""
This is the junction table.
It connects students and courses.

student_id -> references students table
course_id  -> references courses table
"""

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)

# =============================
# Students Table
# =============================
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    """
    relationship() creates the many-to-many link.

    secondary=student_course tells SQLAlchemy to use
    the association table.

    back_populates allows reverse access from Course.
    """
    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )

    def __repr__(self):
        return f"Student(name={self.name})"

# =============================
# Courses Table
# =============================
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String)

    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )

    def __repr__(self):
        return f"Course(title={self.title})"

# =============================
# Create Tables
# =============================
"""
Creates tables in the database if they don't exist.
"""
Base.metadata.create_all(engine)

# =============================
# Session Setup
# =============================
Session = sessionmaker(bind=engine)
session = Session()

# =============================
# Insert Random Data
# =============================
"""
We create students and courses,
then randomly assign relationships.
"""

student_names = ["Ali", "Sara", "John", "Ayesha", "David"]
course_titles = ["Math", "Physics", "AI", "Databases", "Python"]

students = [Student(name=name) for name in student_names]
courses = [Course(title=title) for title in course_titles]

# randomly assign courses to students
for student in students:
    student.courses = random.sample(courses, k=random.randint(1, 3))

session.add_all(students + courses)
session.commit()

print("\n===== Data Inserted =====\n")

# =============================
# Query Data
# =============================

"""
Example queries:
- Show students and their courses
- Show courses and enrolled students
"""

all_students = session.query(Student).all()

for student in all_students:
    print(f"{student.name} enrolled in:")
    for course in student.courses:
        print("  -", course.title)
    print()

print("\n===== Reverse Query =====\n")

all_courses = session.query(Course).all()

for course in all_courses:
    print(f"{course.title} has students:")
    for student in course.students:
        print("  -", student.name)
    print()

# =============================
# Close Session
# =============================
session.close()

"""
===========================================================
Summary:
- Many-to-many uses an association table
- relationship() connects both tables
- secondary links the junction table
- back_populates enables bidirectional access
- Data is added using normal Python objects
- SQLAlchemy handles joins automatically
===========================================================

You now have a complete working example.
Push this to GitHub as practice.
"""
