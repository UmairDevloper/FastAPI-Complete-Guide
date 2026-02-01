"""
===========================================================
SQLAlchemy Events & Listeners — Complete Practical Guide
===========================================================

Definition:
Events allow you to hook into SQLAlchemy’s internal lifecycle.
Listeners execute custom logic when specific database actions occur.

Think of them as triggers in Python.

You can listen to:
- Insert events
- Update events
- Delete events
- Session events
- Engine/connection events

This file demonstrates:
- before_insert
- after_insert
- before_update
- after_delete
- session commit event
- logging behavior

Run this file directly.
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================================================
# Engine Setup
# =========================================================
engine = create_engine("sqlite:///events.db", echo=True)
Base = declarative_base()

# =========================================================
# Model
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"User(name={self.name}, age={self.age})"

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
# EVENT LISTENERS
# =========================================================

"""
1. BEFORE INSERT EVENT
Runs before a row is inserted into database.
"""

@event.listens_for(User, "before_insert")
def before_insert(mapper, connection, target):
    print(f"[EVENT] Before Insert -> {target}")
    if target.age < 0:
        target.age = 0   # auto-fix invalid data


"""
2. AFTER INSERT EVENT
Runs after insertion is complete.
"""

@event.listens_for(User, "after_insert")
def after_insert(mapper, connection, target):
    print(f"[EVENT] After Insert -> {target}")


"""
3. BEFORE UPDATE EVENT
Runs before updating a record.
"""

@event.listens_for(User, "before_update")
def before_update(mapper, connection, target):
    print(f"[EVENT] Before Update -> {target}")


"""
4. AFTER DELETE EVENT
Runs after deleting a record.
"""

@event.listens_for(User, "after_delete")
def after_delete(mapper, connection, target):
    print(f"[EVENT] After Delete -> {target}")


"""
5. SESSION EVENT
Triggered after session commit.
"""

@event.listens_for(session, "after_commit")
def after_commit(session):
    print("[EVENT] Session committed successfully")


# =========================================================
# Test Events
# =========================================================

print("\n===== INSERT =====")
user = User(name="Ali", age=-5)  # invalid age
session.add(user)
session.commit()

print("\n===== UPDATE =====")
user.age = 30
session.commit()

print("\n===== DELETE =====")
session.delete(user)
session.commit()

# =========================================================
# Summary
# =========================================================
"""
Event Summary:

before_insert -> validate/modify data
after_insert  -> logging/auditing
before_update -> track changes
after_delete  -> cleanup actions
after_commit  -> session lifecycle hook

Use cases:
- Validation
- Logging
- Auditing
- Auto timestamps
- Security checks
- Business rules

Events act like database triggers,
but implemented in Python.
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_events_listeners.txt

Push to GitHub as advanced ORM concept.
"""
