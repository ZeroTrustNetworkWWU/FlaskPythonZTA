import requests

url = 'http://127.0.0.1:5001'

# Trying getRoles
print("\nTesting roles gathering...")
response = requests.get(url+'/getRoles')
print(response.content)

# Trying addRole
print("\nTesting role adding...")
response = requests.post(url+'/addRole')
print(response.content)

# Trying removeRole
print("\nTesting role removal...")
response = requests.put(url+'/removeRole')
print(response.content)

# Trying getUsers
print("\nTesting users gathering...")
response = requests.get(url+'/getUsers')
print(response.content)

# Trying addUser (line ~63 in UserDataHandler)
print("\nTesting user adding...")
response = requests.post(url+'/addUser')
print(response.content)

# Trying removeUser
print("\nTesting user removal...")
response = requests.put(url+'/removeUser')
print(response.content)

