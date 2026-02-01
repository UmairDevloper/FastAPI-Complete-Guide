from main import session, User, session
from sqlalchemy import func
import random


names = ["ali", "hadi", "hammad", "khurram", "umair", "huzaifa"]
ages = [34, 23, 56, 45, 56, 67]


# INSERTION

for i in range(1, 20):
    user = User(name=random.choice(names), age = random.choice(ages))
    session.add(user)

session.commit()


# READ

# users = session.query(User).all()

# for user in users:
#     print(user.name, user.age)


# UPDATE

# user = session.query(User).filter(User.id ==3).first()
# print(user.name, user.age)
# user.name = "Hashim"
# session.commit()
# print(user.name, user.age)

# DELETION

# user = session.query(User).filter(User.id ==3).first()
# session.delete(user)
# session.commit()

# user = session.query(User).all()
# for x in user:
#     print(x.id, x.name, x.age)


# ORDERING

# users = session.query(User).order_by(User.age.desc()).all()
# for x in users:
#     print(x.id, x.name, x.age)

# FILTERING

# users = (
#     session.query(User)
#     .filter(User.age > 25, User.age < 70)
#     .order_by(User.name.desc())
#     .all()
# )

# for x in users:
#     print(x.id, x.name, x.age)

# GROUP BY

# users = (
#     session.query(User.name, 
#                 func.max(User.age).label("max_age"))
#     .group_by(User.name)
#     .all()
# )

# for name, max_age in users:
#     print(name, max_age)