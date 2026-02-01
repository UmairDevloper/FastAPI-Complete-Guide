from main import User,  session

# user1 = User(username="Ali")
# user2 = User(username="Muneeb")
# user3 = User(username="Rehman")

# address1 = Address(city="Multan", state="Punjab", zip_code=224)
# address2 = Address(city="Karachi", state="Sindh", zip_code=3456)
# address3 = Address(city="Kotli", state="Peshawar", zip_code=345) 

# user1.addresses.extend([address1, address2])
# user2.addresses.append(address3)

# session.add(user1, user2)
# session.commit()

# print(user1.name, user1.age, user1.addresses)
# print(user2.name, user2.age, user2.addresses)
# print(address2.user)


# Self Relationship by association.

user1 = User(username="Ali")
user2 = User(username="Muneeb")
user3 = User(username="Rehman")

session.add_all([user1, user2, user3])
session.commit()

user1.following.append(user2)
user2.following.append(user3)
user3.following.append(user1)

session.commit()


print(user1.following)
print(user2.following)
print(user3.following)




