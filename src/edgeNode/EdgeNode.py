from flask import Flask, request, jsonify
import requests
from EdgeNodeExceptions import MissingTrustData, LowClientTrust

# Trust Engine server URL TODO don't hard code this
trustEngineUrl = "http://127.0.0.1:5001"
backendServerUrl = "http://127.0.0.1:5002"

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

            # Print the trust data
            EdgeNodeReceiver.__printTrustData(trustData)

            trust, session = EdgeNodeReceiver.getPEPDecision(trustData)
            if not trust:
                raise LowClientTrust("Trust Engine Denied Access")
            
            # TODO send login requests to a different trust engine route
            # If this is a login request do not forward it to the backend server
            if EdgeNodeReceiver.isLoginRequest(trustData):
                return jsonify({"session": session}), 200
            
            # Forward the request to the backend server and return the response
            response = EdgeNodeReceiver.forwardToBackendServer(request, data)

            return response.content, response.status_code
        
        except MissingTrustData as e:
            print(e)
            return jsonify({"error": f"{e}"}), 500
        except LowClientTrust as e:
            print(e)
            return jsonify({"error": f"{e}"}), 500
    
    # Get the Trust engines decision on the trust of the client 
    # Returns true if the client is trusted and false if not
    @staticmethod
    def getPEPDecision(trustData):
        try:
            response = requests.post(f"{trustEngineUrl}/getDecision", json=trustData)
            if response.status_code == 200:
                return response.json().get("trustLevel"), response.json().get("session", None)
            else:
                print("Trust Engine failed:", response.status_code)
                return False, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, None
        
    @staticmethod
    def getTrustData(data):
        trustData = data.get("_trustData")
        data.pop("_trustData", None)
        return trustData, data
    
    @staticmethod
    def isLoginRequest(trustData):
        return "login" in trustData.keys()
    
    # TODO validate the trust data is complete not just that it exists
    @staticmethod
    def validateTrustData(data):
        if data == None:
            raise MissingTrustData("Trust data is missing")

    # TODO get any remaining trust data that is not provided by the client from the request ie., geolocation, ip, etc.
    @staticmethod  
    def getRemainingTrustData(request, trustData):
        # Add the ip of the request to the trust data
        trustData["ip"] = request.remote_addr

        # Add the path of the request to the trust data
        trustData["resource"] = request.path

        # Add the request method to the trust data
        trustData["action"] = request.method

    # Prints the trust data in a readable format
    @staticmethod
    def __printTrustData(data):
        for key in data:
            print(f"{key}:", end=" ")
            if type(data[key]) == dict:
                print()
                for key2 in data[key]:
                    print(f"  {key2}: {data[key][key2]}")
            else:
                print(f"{data[key]}")
        print()

    @staticmethod
    def forwardToBackendServer(request, data):
        # Forward the request to the backend server
        full_url = backendServerUrl + request.path

        # Make the request to the backend server
        return requests.request(request.method, full_url, data=data)

    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port)

# Entry point
if __name__ == "__main__":
    edge_node = EdgeNodeReceiver(host='0.0.0.0', port=5000)
    edge_node.run()