"""
===========================================================
SQLAlchemy Indexing — Complete Practical Guide
===========================================================

Definition:
Indexing improves query performance by allowing the database
to quickly locate rows instead of scanning the entire table.

Indexes are used for:
- Searching
- Filtering
- Sorting
- Joining tables

This file demonstrates:
- Single column index
- Unique index
- Composite (multi-column) index
- Creating indexes manually
- Querying indexed columns

Run this file directly.
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================================================
# Engine Setup
# =========================================================
engine = create_engine("sqlite:///indexing.db", echo=True)
Base = declarative_base()

# =========================================================
# Model with Indexes
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    """
    index=True creates a database index
    Useful for frequently searched columns
    """
    username = Column(String, index=True)

    """
    unique=True automatically creates a unique index
    Prevents duplicate values
    """
    email = Column(String, unique=True)

    age = Column(Integer)

    def __repr__(self):
        return f"User(username={self.username}, age={self.age})"


"""
Composite Index:
Creates index using multiple columns
Useful when filtering by both fields together
"""

Index("idx_username_age", User.username, User.age)

# =========================================================
# Create Tables + Indexes
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
users = [
    User(username="Ali", email="ali@example.com", age=23),
    User(username="Sara", email="sara@example.com", age=25),
    User(username="John", email="john@example.com", age=23),
    User(username="Ayesha", email="ayesha@example.com", age=22),
]

session.add_all(users)
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# Query Using Indexed Columns
# =========================================================
"""
Fast search using indexed username
"""

result = session.query(User).filter_by(username="Ali").first()
print("Search by username:", result)

"""
Composite index search
"""

results = session.query(User)\
    .filter(User.username == "John", User.age == 23)\
    .all()

print("\nComposite index result:", results)

# =========================================================
# Sorting (Index helps ORDER BY)
# =========================================================
sorted_users = session.query(User)\
    .order_by(User.username)\
    .all()

print("\nSorted users:")
for user in sorted_users:
    print(user)

# =========================================================
# Summary
# =========================================================
"""
Index Types:

index=True        -> single column index
unique=True       -> unique index
Index(...)        -> composite index

Benefits:
- Faster searching
- Faster filtering
- Faster sorting
- Better join performance

Tradeoff:
Indexes slightly slow down inserts/updates
because database must maintain index structure.
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_indexing.txt

Push to GitHub for practice.
"""
