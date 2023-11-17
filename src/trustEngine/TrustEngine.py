from flask import Flask, request, jsonify
from TrustEngineExceptions import MissingResourceAccess
import casbin

# Create a Flask app instance
app = Flask(__name__)

class TrustEngine:
    def __init__(self, host, port, enforcerModel, enforcerPolicy):
        # Define a static enforcer for all TrustEngine instances
        TrustEngine.accessEnforcer = casbin.Enforcer(enforcerModel, enforcerPolicy)
        self.host = host
        self.port = port
    
    @app.route('/getDecision', methods=['POST'])
    def getDecision():
        response_data = {"trustLevel": False}
        try:
            data = request.get_json()

            # Validate that the user has access to the resource
            if not TrustEngine.accessEnforcer.enforce(data["user"], data["resource"], data["action"]):
                raise MissingResourceAccess("User does not have access to this resource")

            # TODO validate the request more rigurously

            # Respond with the decision
            response_data["trustLevel"] = True
            return jsonify(response_data), 200

        except MissingResourceAccess as e:
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({"error": e.args}), 500
        
    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port)
        

# Entry point
if __name__ == "__main__":
    engine = TrustEngine(host='0.0.0.0', port=5001, enforcerModel="src/trustEngine/enforcerModel.conf", enforcerPolicy="src/trustEngine/enforcerPolicy.csv")
    engine.run()