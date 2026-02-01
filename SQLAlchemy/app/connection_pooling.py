"""
===========================================================
SQLAlchemy Connection Pooling — Complete Practical Guide
===========================================================

Definition:
Connection pooling is a technique to **reuse database connections**
instead of creating a new connection for each request.

Benefits:
- Improves performance
- Reduces database load
- Manages simultaneous connections efficiently

In SQLAlchemy:
- Pooling is built-in for most database engines
- You can configure pool size, overflow, and timeout
- Works for synchronous and asynchronous engines

This file demonstrates:
- Engine setup with pooling
- Pool configuration options
- Simple query usage
- Monitoring pool stats
"""

# =========================================================
# Imports
# =========================================================
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================================================
# Engine Setup with Connection Pooling
# =========================================================
"""
pool_size      -> maximum number of persistent connections (default 5)
max_overflow   -> additional temporary connections (default 10)
pool_timeout   -> seconds to wait for connection before raising error (default 30)
pool_recycle   -> recycle connection after N seconds (default -1)
"""

engine = create_engine(
    "sqlite:///pooling.db",
    echo=True,
    pool_size=3,
    max_overflow=2,
    pool_timeout=5,
    pool_recycle=3600
)

Base = declarative_base()

# =========================================================
# Models
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
# Insert Sample Data
# =========================================================
users = [
    User(name="Ali", age=23),
    User(name="Sara", age=25),
    User(name="John", age=30)
]

session.add_all(users)
session.commit()

print("\n===== DATA INSERTED =====\n")

# =========================================================
# Query Data
# =========================================================
all_users = session.query(User).all()
for user in all_users:
    print(user)

# =========================================================
# Demonstrate Pooling Behavior
# =========================================================
"""
In a real app:
- Connections are reused automatically
- New connections are created only if pool_size + max_overflow is not exceeded
- Pool logs can be monitored using echo=True or pool events
"""

# Optional: Monitoring pool events
from sqlalchemy import event

@event.listens_for(engine, "connect")
def connect_listener(dbapi_connection, connection_record):
    print("[POOL EVENT] New connection created!")

@event.listens_for(engine, "checkout")
def checkout_listener(dbapi_connection, connection_record, connection_proxy):
    print("[POOL EVENT] Connection checked out from pool!")

@event.listens_for(engine, "checkin")
def checkin_listener(dbapi_connection, connection_record):
    print("[POOL EVENT] Connection returned to pool!")

# Trigger events by opening and closing sessions
s1 = Session()
s2 = Session()
s3 = Session()
s1.close()
s2.close()
s3.close()

# =========================================================
# Summary
# =========================================================
"""
Connection Pooling in SQLAlchemy:

- Built-in for all database engines
- Configurable using engine parameters
- pool_size -> persistent connections
- max_overflow -> temporary connections
- pool_timeout -> wait for connection
- pool_recycle -> refresh connection after N seconds

Benefits:
- Faster queries
- Efficient resource usage
- Better scalability
- Avoid "too many connections" errors

Monitoring:
- Use event listeners: connect, checkout, checkin
- Use echo=True for SQL & connection logs
"""

session.close()

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_connection_pooling.txt

Push to GitHub as intermediate/advanced ORM concept.
"""
