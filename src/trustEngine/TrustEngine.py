from flask import Flask, request, jsonify

# Create a Flask app instance
app = Flask(__name__)

class TrustEngine:
    def __init__(self, trustModel, host, port):
        self.trustModel = trustModel
        self.host = host
        self.port = port
    
    @app.route('/getDecision', methods=['POST'])
    def getDecision():
        try:
            data = request.get_json()

            # TODO validate the request through the trust model

            # Respond with the decision
            response_data = {"trustLevel": True}

            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({"error": "An error occurred"}), 500
        
    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port)
        

# Entry point
if __name__ == "__main__":
    engine = TrustEngine(True, host='0.0.0.0', port=5001)
    engine.run()