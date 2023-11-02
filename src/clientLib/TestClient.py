from ZTRequests import ZTRequests
import requests
import time


# Edge node server URL TODO don't hard code this
edge_node_url = "http://127.0.0.1:5000"

# used to test responses directly from the backend server vs the edge node
backend_server_url = "http://127.0.0.1:5002"

# Function to send a request to the edge node
def TestRequests(data):
    try:
        print("Posting...")
        response = ZTRequests.post(f"{edge_node_url}/testPost", json=data)
        response2 = requests.post(f"{backend_server_url}/testPost", json=data)
        validateResponse(response, response2)

        print("Geting...")
        response = ZTRequests.get(f"{edge_node_url}/testGet")
        response2 = requests.get(f"{backend_server_url}/testGet")
        validateResponse(response, response2)

        print("Puting...")
        response = ZTRequests.put(f"{edge_node_url}/testPut", json=data)
        response2 = requests.put(f"{backend_server_url}/testPut", json=data)
        validateResponse(response, response2)

        print("Deleting...")
        response = ZTRequests.delete(f"{edge_node_url}/testDelete")
        response2 = requests.delete(f"{backend_server_url}/testDelete")
        validateResponse(response, response2)

        print("Heading...")
        response = ZTRequests.head(f"{edge_node_url}/testHead")
        response2 = requests.head(f"{backend_server_url}/testHead")
        validateResponse(response, response2)

        print("\nDone\n")

        print("Testing transit time...")
        start = time.time()
        response = ZTRequests.get(f"{edge_node_url}/testGet")
        end = time.time()
        print(f"Edge Node Transit time: {end - start}")
        start = time.time()
        response = requests.get(f"{backend_server_url}/testGet")
        end = time.time()
        print(f"Backend server transit time: {end - start}")

    except Exception as e:
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
