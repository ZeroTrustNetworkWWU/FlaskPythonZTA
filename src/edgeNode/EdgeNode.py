from flask import Flask, request, jsonify
import requests
from TrustExceptions import MissingTrustData, LowTrustLevel

# Trust Engine server URL TODO don't hard code this
trustEngineUrl = "http://127.0.0.1:5001"  # Replace with the actual address and port
backendServerUrl = "http://127.0.0.1:5002"  # Replace with the actual address and port

# Create a Flask app instance
app = Flask(__name__)

# Class that handles reciving data from the client and verifying the trust of the client before passing it on to the servers
class EdgeNodeReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    # Route all requests to this function for verification
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=['POST', 'GET', 'PUT', 'DELETE', 'HEAD'])
    def receive_request(path):
        try:
            data = request.get_json()
            
            # Verify the trust data is here
            trustData, data = EdgeNodeReceiver.getTrustData(data)
            EdgeNodeReceiver.validateTrustData(trustData)
            EdgeNodeReceiver.getRemainingTrustData(request, trustData)

            # print the trust data
            EdgeNodeReceiver.__printTrustData(trustData)

            trust = EdgeNodeReceiver.getPEPDecision(trustData)
            if not trust:
                raise LowTrustLevel("Trust level is too low")
            
            # Forward the request to the backend server and return the response
            response = EdgeNodeReceiver.forwardToBackendServer(request, data)

            return response.text, response.status_code
        
        except MissingTrustData as e:
            error_message = f"Trust data is invalid: {e}"
            print(error_message)
            return jsonify({"error": error_message}), 401
        except LowTrustLevel as e:
            error_message = f"Trust level is too low: {e}"
            print(error_message)
            return jsonify({"error": error_message}), 402
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(error_message)
            return jsonify({"error": error_message}), 500
    
    # get the Trust engines decision on the trust of the client 
    # returns true if the client is trusted and false if not
    @staticmethod
    def getPEPDecision(trustData):
        try:
            response = requests.post(f"{trustEngineUrl}/getDecision", json=trustData)
            if response.status_code == 200:
                return response.json()["trustLevel"]
            else:
                print("Request failed to send to trust engine with status code:", response.status_code)
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    @staticmethod
    def getTrustData(data):
        trustData = data.get("_trustData")
        data.pop("_trustData", None)
        return trustData, data
    
    # TODO validate the trust data is complete not just that it exists
    @staticmethod
    def validateTrustData(data):
        if data == None:
            raise MissingTrustData("Trust data is missing")

    # TODO get any remaining trust data that is not provided by the client from the request ie., geolocation, ip, etc.
    @staticmethod  
    def getRemainingTrustData(request, trustData):
        trustData["ip"] = request.remote_addr

    # Prints the trust data in a readable format
    @staticmethod
    def __printTrustData(data):
        for key in data:
            print(f"{key}:", end=" ")
            if type(data[key]) == dict:
                print()
                for key2 in data[key]:
                    print(f"\t{key2}: {data[key][key2]}")
            else:
                print(f"{data[key]}")
        print()

    @staticmethod
    def forwardToBackendServer(request, data):
        # forward the request to the backend server
        full_url = backendServerUrl + request.path

        # Make the request to the backend server
        return requests.request(request.method, full_url, json=data)

    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port)

# Entry point
if __name__ == "__main__":
    edge_node = EdgeNodeReceiver(host='0.0.0.0', port=5000)
    edge_node.run()