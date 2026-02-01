"""
===========================================================
SQLAlchemy association_proxy — Complete Practical Guide
===========================================================

Definition:
`association_proxy` allows you to simplify access to attributes
of related objects through a proxy property.

Use Case:
Instead of manually looping through child objects to get a property,
you can use association_proxy to access it directly from the parent.

Example:
- A parent has multiple children
- Each child has a 'name'
- Instead of parent.children[i].name,
  you can access parent.child_names

This file demonstrates:
- association_proxy setup
- Parent → Child relationship
- Insert data
- Access child attributes via proxy
- Query examples

Run this file directly.
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

# =========================================================
# Engine Setup
# =========================================================
engine = create_engine("sqlite:///association_proxy.db", echo=True)
Base = declarative_base()

# =========================================================
# Models
# =========================================================

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("parents.id"))

    def __repr__(self):
        return f"Child(name={self.name})"


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationship to children
    children = relationship("Child", backref="parent", cascade="all, delete-orphan")

    """
    Association proxy:
    - 'child_names' acts as a list of child names
    - Behind the scenes, it maps to child.name
    """
    child_names = association_proxy('children', 'name')

    def __repr__(self):
        return f"Parent(name={self.name})"

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
p = Parent(name="Parent1")
p.children = [
    Child(name="ChildA"),
    Child(name="ChildB"),
    Child(name="ChildC")
]

session.add(p)
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# Access children via association_proxy
# =========================================================
"""
Instead of iterating:
for child in parent.children:
    print(child.name)

Use association_proxy:
parent.child_names
"""

parent = session.query(Parent).first()
print("Parent:", parent.name)
print("Child Names via proxy:", parent.child_names)

# =========================================================
# Add child via proxy
# =========================================================
"""
You can append directly to the proxy list
"""
parent.child_names.append("ChildD")
session.commit()

print("\nAfter adding ChildD via proxy:", parent.child_names)

# =========================================================
# Remove child via proxy
# =========================================================
parent.child_names.remove("ChildB")
session.commit()

print("\nAfter removing ChildB via proxy:", parent.child_names)

# =========================================================
# Query children normally
children = session.query(Child).all()
print("\nAll child objects in DB:", children)

# =========================================================
# Summary
# =========================================================
"""
association_proxy:

- Simplifies access to child attributes
- Works like a virtual property
- Can append/remove items directly
- Supports many-to-one and one-to-many relationships
- Reduces boilerplate code when dealing with collections

Use Cases:
- Access child names, emails, IDs, or other attributes
- Easy CRUD operations on related objects
- Clean and readable code
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_association_proxy.txt

Push to GitHub as advanced ORM concept.
"""
