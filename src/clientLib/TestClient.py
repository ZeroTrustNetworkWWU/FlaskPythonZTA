from ZTRequests import ZTRequests
import requests


# Edge node server URL TODO don't hard code this
edge_node_url = "http://127.0.0.1:5000"  # Replace with the actual address and port
# TODO compare the requests routed through edge nodes to direct requests
backend_server_url = "http://127.0.0.1:5002" # Replace with the actual address and port

# Function to send a request to the edge node
def TestRequests(data):
    try:
        print("Posting...")
        response = ZTRequests.post(f"{edge_node_url}/testPost", json=data)
        response2 = requests.post(f"{backend_server_url}/testPost", json=data)
        checkResponse(response)
        checkResponseSimilarity(response, response2)

        print("Geting...")
        response = ZTRequests.get(f"{edge_node_url}/testGet")
        checkResponse(response)

        print("Puting...")
        response = ZTRequests.put(f"{edge_node_url}/testPut", json=data)
        checkResponse(response)

        print("Deleting...")
        response = ZTRequests.delete(f"{edge_node_url}/testDelete")
        checkResponse(response)

        print("Heading...")
        response = ZTRequests.head(f"{edge_node_url}/testHead")
        checkResponse(response)

        print("\nDone")

    except Exception as e:
        print(f"An error occurred: {e}")

def checkResponse(response):
    if response.status_code == 200:
            print("Request successfully sent to edge node")

            # print data if there is any
            if response.text:
                print(response.text)
    else:
        print("Request failed to send to edge node with status code:", response.status_code)

def checkResponseSimilarity(r1, r2):
    if r1.status_code == r2.status_code:
        if r1.text == r2.text:
            print("Responses are the same")
            return 
    print("Responses are different")

if __name__ == "__main__":
    # dummy data to send
    data = {"key": "theValue"}

    # Send the request to the edge node
    TestRequests(data)
