# from main import User1, Address1, session

# user1 = User1(name="Ali")
# user2 = User1(name="Hammd")
# user3 = User1(name="Hadi")

# address1 = Address1(city="Multan")
# address2 = Address1(city="Lahore")

# user1.address = address1
# user2.address = address2

# # user3 has no address

# session.add_all([user1, user2, user3])
# session.commit()

# print(user1.address)
# print(user2.address)
# print(user3.address)  # None


#   Self relationship by association.
from main import Node, session

node1 = Node(value=1)
node2 = Node(value=2)
node3 = Node(value=3)

node1.next_node = node2
node2.next_node = node3
node3.next_node = node1

session.add_all([node1, node2, node3])
session.commit()

print(node1.next_node)
print(node2.next_node)
print(node3.next_node)
