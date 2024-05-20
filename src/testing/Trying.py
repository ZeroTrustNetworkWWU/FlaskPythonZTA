import requests

url = 'http://127.0.0.1:5001'

# Trying getRoles
print("\nTesting roles gathering...")
response = requests.get(url+'/getRoles')
print(response.content)

# Trying addRole
print("\nTesting role adding...")
data = {
    "role": {
        "name": "testRole", 
        "routes": ["/testHead"], 
        "types": ["HEAD"]
    }
}
# response = requests.post(url+'/addRole', json=data)
# print(response.content)

# Trying removeRole
print("\nTesting role removal...")
data = {
    "name": "testRole"
}
response = requests.put(url+'/removeRole', json=data)
print(response.content)

# Trying getUsers
print("\nTesting users gathering...")
response = requests.get(url+'/getUsers')
print(response.content)

# Trying addUser
print("\nTesting user adding...")
response = requests.post(url+'/addUser')
print(response.content)
# Using register instead
print("\nUsing already implemented user registration...")
data = {
    "user": "testUser",
    "password": "testPassword"
}
response = requests.post(url+'/register', json=data)
print(response.content)

# Trying removeUser
print("\nTesting user removal...")
data = {
    "user": "testUser"
}
response = requests.put(url+'/removeUser', json=data)
print(response.content)
