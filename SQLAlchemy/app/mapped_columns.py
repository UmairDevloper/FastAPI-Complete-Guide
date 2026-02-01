"""
===========================================================
SQLAlchemy Mapped Columns — Complete Practical Guide
===========================================================

Definition:
Mapped columns connect Python class attributes to database
table columns using SQLAlchemy ORM.

Each column defines:
- Data type
- Constraints
- Default values
- Primary keys
- Indexing
- Nullability

This file demonstrates:
- Basic column mapping
- Primary keys
- Unique constraints
- Default values
- Nullable columns
- Indexed columns
- Auto increment
- Column naming
- Querying mapped columns

Run this file directly.
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================================================
# Engine Setup
# =========================================================
engine = create_engine("sqlite:///mapped_columns.db", echo=True)
Base = declarative_base()

# =========================================================
# Model with Mapped Columns
# =========================================================

class User(Base):
    __tablename__ = "users"

    """
    Column Mapping Explanation:

    Column(type, options...)

    Common options:
    primary_key=True -> unique identifier
    nullable=False   -> cannot be empty
    unique=True      -> prevents duplicates
    default=value    -> auto default value
    index=True       -> speeds up searching
    """

    id = Column(Integer, primary_key=True)

    # required field
    username = Column(String, nullable=False, unique=True, index=True)

    # optional field
    email = Column(String, nullable=True)

    # default value
    is_active = Column(Boolean, default=True)

    # custom column name in database
    age = Column("user_age", Integer, default=18)

    def __repr__(self):
        return f"User(username={self.username}, age={self.age})"

# =========================================================
# Create Tables
# =========================================================
Base.metadata.create_all(engine)

# =========================================================
# Session Setup
# =========================================================
Session = sessionmaker(bind=engine)
session = Session()

# =========================================================
# Insert Data
# =========================================================
"""
Notice:
- age defaults to 18
- is_active defaults to True
"""

u1 = User(username="Ali", email="ali@example.com")
u2 = User(username="Sara")
u3 = User(username="John", age=25)

session.add_all([u1, u2, u3])
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# Query Mapped Columns
# =========================================================
"""
We can query full objects or specific columns.
"""

users = session.query(User).all()

for user in users:
    print(user)

print("\n----- Query Specific Columns -----")

results = session.query(User.username, User.age).all()

for username, age in results:
    print(username, "->", age)

# =========================================================
# Update Columns
# =========================================================
"""
Mapped columns behave like normal Python attributes.
"""

user = session.query(User).filter_by(username="Ali").first()
user.age = 30
session.commit()

print("\nUpdated Ali:", user)

# =========================================================
# Delete Record
# =========================================================
session.delete(user)
session.commit()

print("\nAli deleted")

# =========================================================
# Summary
# =========================================================
"""
Mapped Column Features:

primary_key -> unique identifier
nullable    -> allow NULL values
unique      -> prevent duplicates
default     -> automatic values
index       -> faster search
custom name -> map Python attribute to DB column

Columns behave like Python attributes.
SQLAlchemy syncs them with database automatically.
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_mapped_columns.txt

Push to GitHub as practice.
"""
