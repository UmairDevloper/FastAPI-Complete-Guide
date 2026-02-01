"""
===========================================================
SQLAlchemy Joins — Complete Practical Guide
===========================================================

Definition:
A JOIN combines rows from multiple tables based on a relationship.

SQLAlchemy supports:
- Inner Join
- Left Outer Join
- Right Join (via outer logic)
- Full Join (database dependent)
- Explicit Join
- Relationship Join

This file demonstrates:
- Engine setup
- Table relationships
- Insert data
- Different join queries
- Explanation inside comments

Run this file directly.
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# =========================================================
# Engine Setup
# =========================================================
engine = create_engine("sqlite:///joins.db", echo=True)
Base = declarative_base()

# =========================================================
# Models
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses = relationship("Address", back_populates="user")

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
User 1 has addresses
User 2 has no address
This helps demonstrate outer joins
"""

u1 = User(name="Ali", addresses=[Address(city="Multan"), Address(city="Lahore")])
u2 = User(name="Sara")  # no address

session.add_all([u1, u2])
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# 1. INNER JOIN
# =========================================================
"""
Returns only matching rows.
Users WITHOUT addresses will not appear.
"""

print("----- INNER JOIN -----")

results = session.query(User, Address)\
    .join(Address)\
    .all()

for user, address in results:
    print(user.name, "->", address.city)

# =========================================================
# 2. LEFT OUTER JOIN
# =========================================================
"""
Returns all users.
Users without addresses appear with NULL.
"""

print("\n----- LEFT OUTER JOIN -----")

results = session.query(User, Address)\
    .outerjoin(Address)\
    .all()

for user, address in results:
    print(user.name, "->", address)

# =========================================================
# 3. JOIN USING RELATIONSHIP
# =========================================================
"""
SQLAlchemy automatically understands relationships.
Cleaner syntax.
"""

print("\n----- RELATIONSHIP JOIN -----")

results = session.query(User)\
    .join(User.addresses)\
    .all()

for user in results:
    print(user.name)

# =========================================================
# 4. FILTERED JOIN
# =========================================================
"""
Join with condition filtering.
"""

print("\n----- FILTERED JOIN -----")

results = session.query(User, Address)\
    .join(Address)\
    .filter(Address.city == "Multan")\
    .all()

for user, address in results:
    print(user.name, "lives in", address.city)

# =========================================================
# 5. MULTIPLE JOIN CONDITIONS
# =========================================================
"""
Example: selecting specific columns after join
"""

print("\n----- SELECT SPECIFIC COLUMNS -----")

results = session.query(User.name, Address.city)\
    .join(Address)\
    .all()

for name, city in results:
    print(name, "->", city)

# =========================================================
# Summary
# =========================================================
"""
Join Summary:

join()       -> INNER JOIN
outerjoin()  -> LEFT OUTER JOIN
join(rel)    -> relationship-based join

Inner join = only matching records
Outer join = include unmatched records

SQLAlchemy converts joins into SQL automatically.
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_joins.txt

This file demonstrates real ORM joins.
Push to GitHub for practice.
"""
