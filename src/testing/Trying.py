import requests
import json

url = 'http://127.0.0.1:5001'

# Trying getRoles
print("\nTesting roles gathering...")
response = requests.get(url+'/getRoles')
print(response.text)

# Save to revert changes later
old_roles = json.loads(response.text)

# Trying addRole
print("\nTesting role adding...")
data = {
    "role": {
        "name": "testRole", 
        "routes": "/testHead", 
        "types": "HEAD"
    }
}
response = requests.post(url+'/addRole', json=data)
print(response.text)

# Confirmation
print("\nConfirming role addition...")
response = requests.get(url+'/getRoles')
print(response.text)

# Save for future test
withtestrole = json.loads(response.text)

# Trying removeRole
print("\nTesting role removal...")
data = {
    "role": {
        "name": "testRole",
        "routes": "/testHead",
        "types": "HEAD"
    }
}
response = requests.put(url+'/removeRole', json=data)
print(response.text)

# Confirmation
print("\nConfirming role deletion...")
response = requests.get(url+'/getRoles')
print(response.text)

# Trying getUsers
print("\nTesting users gathering...")
response = requests.get(url+'/getUsers')
print(response.text)

# Save to revert changes later
old_users = json.loads(response.text)

# Trying addUser
print("\nTesting user adding, using already implemented user registration...")
data = {
    "user": "testUser",
    "password": "testPassword"
}
response = requests.post(url+'/addUser', json=data)
print(response.text)

# Confirmation
print("\nConfirming user addition...")
response = requests.get(url+'/getUsers')
print(response.text)

# Save for future test
withtestuser = json.loads(response.text)

# Trying removeUser
print("\nTesting user removal...")
data = {
    "user": "testUser"
}
response = requests.put(url+'/removeUser', json=data)
print(response.text)

# Confirmation
print("\nConfirming user deletion...")
response = requests.get(url+'/getUsers')
print(response.text)

# Trying updateUserList
print("\nTesting user list updating...")
print("unchanged original:")
response = requests.post(url+'/updateUserList', json=old_users)
print(response.text)
print("return of testUser:")
response = requests.post(url+'/updateUserList', json=withtestuser)
print(response.text)
print("back to original:")
response = requests.post(url+'/updateUserList', json=old_users)
print(response.text)

# Trying updateRoleList
print("\nTesting role list updating...")
print("unchanged original:")
response = requests.post(url+'/updateRoleList', json=old_roles)
print(response.text)
print("return of testRole:")
response = requests.post(url+'/updateRoleList', json=withtestrole)
print(response.text)
print("back to original:")
response = requests.post(url+'/updateRoleList', json=old_roles)
print(response.text)
