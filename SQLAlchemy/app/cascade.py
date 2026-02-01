"""
===========================================================
SQLAlchemy Cascades — Complete Practical Guide
===========================================================

Definition:
Cascade controls how operations on a parent object affect
its related child objects.

When a parent is saved, deleted, or updated,
cascades decide what happens to its children.

Think of cascade as automatic propagation of actions.

Common cascade types:
- save-update
- merge
- delete
- delete-orphan
- all

This file demonstrates:
- Parent → Child relationship
- Cascade behaviors
- Insert
- Update
- Delete
- Orphan removal

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
engine = create_engine("sqlite:///cascade.db", echo=True)
Base = declarative_base()

# =========================================================
# Models
# =========================================================

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    """
    cascade explanation:

    save-update -> child auto saved with parent
    delete      -> deleting parent deletes children
    delete-orphan -> child removed if detached
    all         -> includes all behaviors

    "all, delete-orphan" is most common.
    """

    children = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Parent(name={self.name})"


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("parents.id"))

    parent = relationship("Parent", back_populates="children")

    def __repr__(self):
        return f"Child(name={self.name})"

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
# Insert Parent + Children
# =========================================================
"""
Children auto saved because of cascade save-update
"""

p = Parent(name="Parent1")
p.children = [
    Child(name="ChildA"),
    Child(name="ChildB")
]

session.add(p)
session.commit()

print("\n===== INSERTED =====\n")

# =========================================================
# Remove One Child (Orphan)
# =========================================================
"""
delete-orphan removes child automatically
"""

p.children.pop(0)
session.commit()

print("\n===== ORPHAN REMOVED =====\n")

# =========================================================
# Delete Parent
# =========================================================
"""
Deleting parent deletes remaining children
"""

session.delete(p)
session.commit()

print("\n===== PARENT DELETED =====\n")

# =========================================================
# Summary
# =========================================================
"""
Cascade Types:

save-update  -> auto save children
merge        -> merge operations cascade
delete       -> delete children with parent
delete-orphan-> remove detached children
all          -> includes everything

Most common usage:
cascade="all, delete-orphan"

Benefits:
- Automatic relationship management
- Prevent orphan records
- Cleaner database logic
- Less manual coding

Cascades act like smart automation
for parent-child relationships.
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_cascade.txt

Push to GitHub as advanced ORM topic.
"""
