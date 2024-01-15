from ZTRequests import ZTRequests
import requests
import time
from ClientAPIConfig import ClientAPIConfig

config = ClientAPIConfig()

# Function to send a request to the edge node
def TestRequests(data):
    try:
        print("Testing without logging in...")
        print("Posting...")
        response = ZTRequests.post(f"{config.edgeNodeUrl}/testPost", json=data)
        response2 = requests.post(f"{config.backendServerUrl}/testPost", json=data, verify="cert.pem")

        validateResponse(response, response2)

        input("Press enter to continue...")

        print("Logging in...")
        response = ZTRequests.login(f"{config.edgeNodeUrl}/login", user=input("Enter Username: "), password=input("Enter Password: "))
        if response.status_code != 200:
            print("Login Failed")
            return
        else:
            print("Login Successful")
            print(f"Session: {response.json()['session']}\n")


        print("Posting...")
        response = ZTRequests.post(f"{config.edgeNodeUrl}/testPost", json=data)
        response2 = requests.post(f"{config.backendServerUrl}/testPost", json=data, verify="cert.pem")
        validateResponse(response, response2)

        print("Geting...")
        response = ZTRequests.get(f"{config.edgeNodeUrl}/testGet")
        response2 = requests.get(f"{config.backendServerUrl}/testGet", verify="cert.pem")
        validateResponse(response, response2)

        print("Puting...")
        response = ZTRequests.put(f"{config.edgeNodeUrl}/testPut", json=data)
        response2 = requests.put(f"{config.backendServerUrl}/testPut", json=data, verify="cert.pem")
        validateResponse(response, response2)

        print("Deleting...")
        response = ZTRequests.delete(f"{config.edgeNodeUrl}/testDelete")
        response2 = requests.delete(f"{config.backendServerUrl}/testDelete", verify="cert.pem")
        validateResponse(response, response2)

        print("Heading...")
        response = ZTRequests.head(f"{config.edgeNodeUrl}/testHead")
        response2 = requests.head(f"{config.backendServerUrl}/testHead", verify="cert.pem")
        validateResponse(response, response2)

        print("Logging out...")
        response = ZTRequests.logout(f"{config.edgeNodeUrl}/logout")

        input("Press enter to continue...")

        print("Registering...")
        response = ZTRequests.register(f"{config.edgeNodeUrl}/register", user=input("Enter Username: "), password=input("Enter Password: "))
        if response.status_code != 200:
            print("Registration Failed")
            return
        else:
            print("Registration Successful")

        print("Logging in...")
        response = ZTRequests.login(f"{config.edgeNodeUrl}/login", user=input("Enter Username: "), password=input("Enter Password: "))
        if response.status_code != 200:
            print("Login Failed")
            return
        else:
            print("Login Successful")
            print(f"Session: {response.json()['session']}\n")

        print("Posting...")
        response = ZTRequests.post(f"{config.edgeNodeUrl}/testPost", json=data)
        response2 = requests.post(f"{config.backendServerUrl}/testPost", json=data, verify="cert.pem")
        validateResponse(response, response2)

        print("Geting...")
        response = ZTRequests.get(f"{config.edgeNodeUrl}/testGet")
        response2 = requests.get(f"{config.backendServerUrl}/testGet", verify="cert.pem")
        validateResponse(response, response2)

        print("\nDone\n")

        print("Testing transit time...")
        start = time.time()
        response = ZTRequests.get(f"{config.edgeNodeUrl}/testGet")
        end = time.time()
        print(f"Edge Node Transit time: {end - start}")
        start = time.time()
        response = requests.get(f"{config.backendServerUrl}/testGet", verify="cert.pem")
        end = time.time()
        print(f"Backend server transit time: {end - start}")

    except Exception as e:
        # print the stack trace
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")

def validateResponse(response, trueResponse):
    checkResponseSimilarity(response, trueResponse)
    print(f"EdgeNode response: {response.status_code}")
    print(f"Backend server response: {trueResponse.status_code}")
    print()

def checkResponseSimilarity(r1, r2):
    if r1.status_code == r2.status_code:
        if r1.content == r2.content:
            print("Responses are the same")
            return 
    print("Responses are different")
    print(f"EdgeNode response: {r1.content}")
    print(f"Backend server response: {r2.content}")

if __name__ == "__main__":
    # dummy data to send
    data = {"This is some Data" : "Data", "This is some more data" : "More Data"}

    # Send the request to the edge node
    TestRequests(data)
