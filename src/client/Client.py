from ZTRequests import ZTRequests


# Edge node server URL TODO don't hard code this
edge_node_url = "http://127.0.0.1:5000"  # Replace with the actual address and port

# Function to send a request to the edge node
def TestRequests(data):
    try:
        print("Posting...")
        response = ZTRequests.post(f"{edge_node_url}/arandomroute", json=data)
        checkResponse(response)

        print("Geting...")
        response = ZTRequests.get(f"{edge_node_url}/arandomroute")
        checkResponse(response)

        print("Puting...")
        response = ZTRequests.put(f"{edge_node_url}/arandomroute", json=data)
        checkResponse(response)

        print("Deleting...")
        response = ZTRequests.delete(f"{edge_node_url}/arandomroute")
        checkResponse(response)

        print("Heading...")
        response = ZTRequests.head(f"{edge_node_url}/arandomroute")
        checkResponse(response)

        print("\nDone")

    except Exception as e:
        print(f"An error occurred: {e}")

def checkResponse(response):
    if response.status_code == 200:
            print("Request successfully sent to edge node")
    else:
        print("Request failed to send to edge node with status code:", response.status_code)

if __name__ == "__main__":
    # dummy data to send
    data = {"key": "theValue"}

    # Send the request to the edge node
    TestRequests(data)
