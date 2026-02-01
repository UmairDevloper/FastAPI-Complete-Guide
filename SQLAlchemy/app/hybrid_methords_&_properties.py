"""
===========================================================
SQLAlchemy Hybrid Methods & Properties — Complete Guide
===========================================================

Definition:
Hybrid properties and methods allow attributes and methods
to work both at the **Python object level** and the **SQL expression level**.

Use Case:
- You can use them like normal Python attributes
- Also use them in queries (filter/order_by)
- Useful for computed columns and complex logic

This file demonstrates:
- hybrid_property
- hybrid_method
- Computed attributes
- Querying via hybrid properties/methods
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

# =========================================================
# Engine Setup
# =========================================================
engine = create_engine("sqlite:///hybrid.db", echo=True)
Base = declarative_base()

# =========================================================
# Model with Hybrid Property & Method
# =========================================================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    salary = Column(Integer)

    # =====================================================
    # HYBRID PROPERTY
    # =====================================================
    """
    full_name behaves like a Python property:
    emp.full_name -> 'First Last'
    Can also be used in queries
    """
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # =====================================================
    # HYBRID METHOD
    # =====================================================
    """
    bonus(amount) works like a method:
    emp.bonus(1000) -> returns salary + 1000
    Can also be used in queries
    """
    @hybrid_method
    def bonus(self, amount):
        return self.salary + amount

    def __repr__(self):
        return f"Employee({self.full_name}, salary={self.salary})"

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
e1 = Employee(first_name="Ali", last_name="Khan", salary=50000)
e2 = Employee(first_name="Sara", last_name="Ali", salary=60000)
e3 = Employee(first_name="John", last_name="Doe", salary=45000)

session.add_all([e1, e2, e3])
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# Access Hybrid Property
# =========================================================
employees = session.query(Employee).all()
for emp in employees:
    print(f"{emp.full_name} has salary {emp.salary}")

# =========================================================
# Access Hybrid Method
print("\n----- Using Hybrid Method -----")
for emp in employees:
    print(f"{emp.full_name} salary with 5000 bonus: {emp.bonus(5000)}")

# =========================================================
# Query using Hybrid Property
print("\n----- Query using Hybrid Property -----")
high_paid = session.query(Employee).filter(Employee.full_name == "Ali Khan").all()
for emp in high_paid:
    print("High paid:", emp)

# =========================================================
# Query using Hybrid Method (SQL expression)
from sqlalchemy import func

# Using method in filter with SQL expression
high_bonus = session.query(Employee).filter(Employee.bonus(10000) > 55000).all()
print("\nEmployees with bonus > 55000:")
for emp in high_bonus:
    print(emp)

# =========================================================
# Summary
# =========================================================
"""
Hybrid Properties & Methods:

@hybrid_property -> acts like attribute
@hybrid_method   -> acts like method

Benefits:
- Compute derived data
- Use same property/method in Python & SQL queries
- Clean code, avoids manual query computation

Use Cases:
- Full names
- Computed scores, age, price, salary
- Complex query logic with Python simplicity
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_hybrid_properties_methods.txt

Push to GitHub as advanced ORM topic.
"""
