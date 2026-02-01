from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column

DB_URL="postgresql+psycopg2://postgres:9092257@localhost:5432/sqlalchemy"

engine = create_engine(DB_URL)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

#   Simple table

# class User(Base):
#     __tablename__  = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


#   Relationship.
# class BaseModel(Base):
#     __abstract__ = True
#     __allow_unmapped__ = True

#     id = Column(Integer, primary_key=True)


#   One-To-Many Relationship.

# class Address(BaseModel):
#     __tablename__ = "addresses"

#     city = Column(String)
#     state = Column(String)
#     zip_code = Column(Integer)
#     user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user : Mapped["User"] =  relationship(back_populates="addresses")

#     def __repr__(self):
#         return f"<Address (city = {self.city}, state = {self.state}, )>"

# class User(BaseModel):
#     __tablename__ = "users"

#     name = Column(String)
#     age = Column(Integer)
#     addresses : Mapped[list["Address"]] = relationship()

#     def __repr__(self):
#         return f"<User (name = {self.name}, age = {self.age}, )>"


#   Self Relationship by association

# class BaseModel(Base):
#     __abstract__ = True
#     __allow_unmapped__ = True

#     id = Column(Integer, primary_key=True)


# class FollowingAssociation(BaseModel):
#     __tablename__ = "following_association"

#     user_id = Column(Integer, ForeignKey("users.id"))
#     following_id = Column(Integer, ForeignKey("users.id"))


# class User(BaseModel):
#     __tablename__ = "users"

#     username = Column(String)
#     following = relationship("User", secondary="following_association",
#                             primaryjoin=("following_association.c.user_id == User.id"),
#                             secondaryjoin=("following_association.c.following_id == User.id"))

#     def __repr__(self):
#         return f"<User (name = {self.id}, username = {self.username}, following = {self.following})>"

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


#   One-To-One Relationship.


# class User1(Base):
#     __tablename__ = "users1"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     address = relationship(
#         "Address1",
#         back_populates="user",
#         uselist=False
#     )

#     def __repr__(self):
#         return f"<User(name={self.name}, address={self.address})>"


# class Address1(Base):
#     __tablename__ = "address1"

#     id = Column(Integer, primary_key=True)
#     city = Column(String)

#     user_id = Column(Integer, ForeignKey("users1.id"), unique=True)

#     user = relationship(
#         "User1",
#         back_populates="address"
#     )

#     def __repr__(self):
#         return f"<Address(city={self.city})>"

# Base.metadata.create_all(engine)

# Self Relationship by association
class NodeAssociation(Base):
    __tablename__ = "node_association"

    id = Column(Integer, primary_key=True)
    current_node_id = Column(Integer, ForeignKey("node.id"))
    next_node_id = Column(Integer, ForeignKey("node.id"))


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True)
    value = Column(Integer)

    next_node = relationship(
        "Node",
        secondary="node_association",
        primaryjoin="Node.id == node_association.c.current_node_id",
        secondaryjoin="Node.id == node_association.c.next_node_id",
        uselist=False
    )

    def __repr__(self):
        return f"<Node id={self.id}, value={self.value}>"
    
Base.metadata.create_all(engine)
