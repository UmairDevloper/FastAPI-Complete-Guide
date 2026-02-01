from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column, selectinload, joinedload, subqueryload

DB_URL="postgresql+psycopg2://postgres:9092257@localhost:5432/sqlalchemy"

engine = create_engine(DB_URL,echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
#--------------------------------
# Lazy Loading (By Default.)    \
#-------------------------------


# class User2(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     addresses = relationship("Address2", back_populates="user")  # lazy by default

#     def __repr__ (self):
#         return f"User {self.name}"


# class Address2(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     city = Column(Text)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     user = relationship("User2", back_populates="addresses")

#     def __repr__ (self):
#         return f"Address {self.city}"

# Base.metadata.create_all(engine)


# user1 = User2(name="Ali")
# user2 = User2(name="Mad")
# address1 = Address2(city="Lahore") 
# address2 = Address2(city="Karachi")
# address3 = Address2(city="Multan")

# user1.addresses.extend([address1, address2])
# user2.addresses.append(address3)

# session.add_all([user1, user2])
# session.commit()

# user = session.query(User2).all()
# for x in user:
#     print(x.name, [val.city for val in x.addresses])

# new_user = User2(
#     name = "ali",
#     addresses = [
#         Address2(city=f"My address in Multan {x}")
#         for x in range(1, 10)
#     ]
# )

# session.add(new_user)
# session.commit()

# user = session.query(User2).all()
# for x in user:
#     print(x.name, x.addresses)

# It causes the N + 1 problem. For one user we have to call the address n times

#--------------------------------
# SelectIn                      | 
#-------------------------------


# Load parents then fetch the children

# class User2(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     addresses = relationship("Address2", back_populates="user")  

#     def __repr__ (self):
#         return f"User {self.name}"


# class Address2(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     city = Column(Text)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     user = relationship("User2", back_populates="addresses")

#     def __repr__ (self):
#         return f"Address {self.city}"

# Base.metadata.create_all(engine)

# new_user = User2(
#     name = "ali",
#     addresses = [
#         Address2(city=f"My address in Multan {x}")
#         for x in range(1, 10)
#     ]
# )

# session.add(new_user)
# session.commit()

# user = session.query(User2).options(selectinload(User2.addresses)).all()
# for x in user:
#     print(x.name, x.addresses)



#--------------------------------
#   Joined                        \
#-------------------------------


# class User2(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     addresses = relationship("Address2", back_populates="user")  

#     def __repr__ (self):
#         return f"User {self.name}"


# class Address2(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     city = Column(Text)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     user = relationship("User2", back_populates="addresses")

#     def __repr__ (self):
#         return f"Address {self.city}"

# Base.metadata.create_all(engine)

# new_user = User2(
#     name = "ali",
#     addresses = [
#         Address2(city=f"My address in Multan {x}")
#         for x in range(1, 10)
#     ]
# )

# session.add(new_user)
# session.commit()

# user = session.query(User2).options(joinedload(User2.addresses)).all()
# for x in user:
#     print(x.name, x.addresses)

#--------------------------------
#   Subquery                        \
#-------------------------------



# user = session.query(User2).options(subqueryload(User2.addresses)).all()
# for x in user:
#     print(x.name, x.addresses)

#--------------------------------
#   Raise                        \
#-------------------------------


# class User2(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     addresses = relationship("Address2", back_populates="user", lazy="raise")  

#     def __repr__ (self):
#         return f"User {self.name}"


# class Address2(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     city = Column(Text)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     user = relationship("User2", back_populates="addresses")

#     def __repr__ (self):
#         return f"Address {self.city}"

# Base.metadata.create_all(engine)

# new_user = User2(
#     name = "ali",
#     addresses = [
#         Address2(city=f"My address in Multan {x}")
#         for x in range(1, 10)
#     ]
# )

# session.add(new_user)
# session.commit()

# user = session.query(User2).first()
# try:
#     print(user.addresses)
# except Exception as e:
#     print(e)




#--------------------------------
#   Write-Only                        \
#-------------------------------


# class User2(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     addresses = relationship("Address2", back_populates="user", lazy="write_only")  

#     def __repr__ (self):
#         return f"User {self.name}"


# class Address2(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     city = Column(Text)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     user = relationship("User2", back_populates="addresses")

#     def __repr__ (self):
#         return f"Address {self.city}"

# Base.metadata.create_all(engine)

# user = User2(name="Jack")
# user.addresses.append(Address2(city="Pindi"))

# print(user)

# REMEMBER The write-only is to write the data only. You cannot read it.


#--------------------------------
#   Dynamic                        \
#-------------------------------

class User2(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses = relationship("Address2", back_populates="user", lazy="dynamic")  

    def __repr__ (self):
        return f"User {self.name}"


class Address2(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    city = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User2", back_populates="addresses")

    def __repr__ (self):
        return f"Address {self.city}"

Base.metadata.create_all(engine)

user1 = User2(name="Ali")
user2 = User2(name="Mad")
address1 = Address2(city="Lahore") 
address2 = Address2(city="Karachi")
address3 = Address2(city="Multan")

user1.addresses.extend([address1, address2])
user2.addresses.append(address3)

session.add_all([user1, user2])
session.commit()

user = session.query(User2).filter_by(name="Ali").first()
address = user.addresses.filter(Address2.city == "Lahore").all()

print(address)