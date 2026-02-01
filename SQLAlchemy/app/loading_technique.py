"""
===========================================================
SQLAlchemy Loading Techniques — Complete Practical Guide
===========================================================

Definition:
Loading techniques control HOW and WHEN related data is fetched
from the database in SQLAlchemy ORM.

Goal:
- Improve performance
- Avoid unnecessary queries
- Control SQL behavior

This file covers:
1. Lazy Loading (default)
2. Select Loading
3. Joined Loading
4. Subquery Loading
5. Select IN Loading
6. Comparison of techniques

All explanations are written as comments.
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import joinedload, subqueryload, selectinload

# =========================================================
# Engine Setup
# =========================================================
"""
Engine connects the application to the database.
Connection pooling is automatically enabled.
"""

engine = create_engine("sqlite:///loading.db", echo=True)
Base = declarative_base()

# =========================================================
# Models
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    """
    lazy='select' is the DEFAULT loading strategy.
    Related data loads ONLY when accessed.
    """
    addresses = relationship(
        "Address",
        back_populates="user",
        lazy="select"
    )

    def __repr__(self):
        return f"User(name={self.name})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(city={self.city})"

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
# Insert Sample Data
# =========================================================
"""
Creating users with addresses.
"""

user1 = User(name="Ali", addresses=[
    Address(city="Multan"),
    Address(city="Lahore")
])

user2 = User(name="Sara", addresses=[
    Address(city="Karachi")
])

session.add_all([user1, user2])
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# 1. Lazy Loading (DEFAULT)
# =========================================================
"""
Lazy Loading:
- Data loads when attribute is accessed
- Causes N+1 problem if used improperly
"""

print("----- Lazy Loading -----")

users = session.query(User).all()   # Only users loaded

for user in users:
    print(user.name)
    print(user.addresses)   # Separate query per user

# =========================================================
# 2. Joined Loading
# =========================================================
"""
Joined Loading:
- Uses SQL JOIN
- Fetches related data in ONE query
- Best for small datasets
"""

print("\n----- Joined Loading -----")

users = session.query(User).options(
    joinedload(User.addresses)
).all()

for user in users:
    print(user.name, user.addresses)

# =========================================================
# 3. Subquery Loading
# =========================================================
"""
Subquery Loading:
- Executes one main query
- Executes one extra query using subquery
- Better than lazy for large datasets
"""

print("\n----- Subquery Loading -----")

users = session.query(User).options(
    subqueryload(User.addresses)
).all()

for user in users:
    print(user.name, user.addresses)

# =========================================================
# 4. Select IN Loading (Recommended)
# =========================================================
"""
Select IN Loading:
- Executes two queries
- Uses WHERE IN (...)
- Very efficient
- Recommended for most cases
"""

print("\n----- Select IN Loading -----")

users = session.query(User).options(
    selectinload(User.addresses)
).all()

for user in users:
    print(user.name, user.addresses)

# =========================================================
# Summary (Important for Interviews)
# =========================================================
"""
Loading Technique Summary:

lazy='select'  -> Default, may cause N+1 problem
joinedload     -> Single JOIN query
subqueryload   -> Separate subquery
selectinload   -> Best balance (recommended)

Rule of Thumb:
- Small dataset  -> joinedload
- Large dataset -> selectinload
- Avoid lazy loading in production
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Push this file to GitHub as:
sqlalchemy_loading_techniques.txt

This demonstrates real ORM behavior.
"""
