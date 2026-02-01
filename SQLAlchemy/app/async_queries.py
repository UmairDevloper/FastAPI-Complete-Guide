"""
===========================================================
SQLAlchemy Async Queries with FastAPI — Complete Guide
===========================================================

Definition:
Async queries allow non-blocking database operations.
Useful when building APIs with FastAPI to improve performance
under high concurrency.

Key Concepts:
- Async engine: connect asynchronously to DB
- Async session: use async context managers
- Await queries: must use 'await' keyword
- Compatible with async frameworks like FastAPI

This file demonstrates:
- Async engine setup
- Async session
- Insert, query, update, delete operations
- FastAPI integration
"""

# =========================================================
# Imports
# =========================================================
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, select, update, delete

# =========================================================
# Async Engine Setup
# =========================================================
"""
- Use "sqlite+aiosqlite:///" for SQLite async
- pool_size and max_overflow can also be configured
"""

DATABASE_URL = "sqlite+aiosqlite:///async_queries.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
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
# Async Session Setup
# =========================================================
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# =========================================================
# Create Tables Async
# =========================================================
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created!")

# =========================================================
# Async Insert
# =========================================================
async def insert_users():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user1 = User(name="Ali", age=23)
            user2 = User(name="Sara", age=25)
            user3 = User(name="John", age=30)
            session.add_all([user1, user2, user3])
        await session.commit()
    print("Users inserted!")

# =========================================================
# Async Query
# =========================================================
async def query_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print("\n----- QUERY RESULTS -----")
        for user in users:
            print(user)

# =========================================================
# Async Update
# =========================================================
async def update_user():
    async with AsyncSessionLocal() as session:
        stmt = update(User).where(User.name == "Ali").values(age=35)
        await session.execute(stmt)
        await session.commit()
    print("\nUser Ali updated!")

# =========================================================
# Async Delete
# =========================================================
async def delete_user():
    async with AsyncSessionLocal() as session:
        stmt = delete(User).where(User.name == "John")
        await session.execute(stmt)
        await session.commit()
    print("\nUser John deleted!")

# =========================================================
# Main Async Runner
# =========================================================
async def main():
    await init_db()
    await insert_users()
    await query_users()
    await update_user()
    await query_users()
    await delete_user()
    await query_users()

# Run async main
asyncio.run(main())

# =========================================================
# Summary
# =========================================================
"""
Async SQLAlchemy Queries:

- Use create_async_engine
- Use AsyncSession
- All DB operations must be awaited
- Integrates seamlessly with FastAPI
- Reduces blocking during high concurrency
- Supports all CRUD operations asynchronously

Benefits:
- High-performance APIs
- Non-blocking DB access
- Scalable web apps

Tips:
- Always use 'async with' for session
- Use 'scalars()' to get ORM objects from results
- For complex joins or relationships, await queries similarly
"""

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_async_queries.txt

Push to GitHub as advanced ORM + FastAPI concept.
"""
