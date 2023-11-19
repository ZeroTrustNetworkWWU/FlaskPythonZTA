from flask import Flask, request, jsonify
from TrustEngineExceptions import MissingResourceAccess, UserNotFound
import casbin

# Create a Flask app instance
app = Flask(__name__)

class TrustEngine:
    def __init__(self, host, port, enforcerModel, enforcerPolicy):
        # Define a static enforcer and user database for all TrustEngine instances
        TrustEngine.accessEnforcer = casbin.Enforcer(enforcerModel, enforcerPolicy)
        TrustEngine.userDatabase = {
            "user1": {
                "role": "admin"
            },
            "user2": {
                "role": "user"
            }
        }
        self.host = host
        self.port = port
    
    @app.route('/getDecision', methods=['POST'])
    def getDecision():
        response_data = {"trustLevel": False}
        try:
            data = request.get_json()

            # TODO add a sql database to store the users their roles and their passwords
            role = TrustEngine.getRole(data["user"])
            if role is None:
                raise UserNotFound("No user found with the given name")
        
            # Validate that the user has access to the resource
            if not TrustEngine.accessEnforcer.enforce(role, data["resource"], data["action"]):
                raise MissingResourceAccess("User does not have access to this resource")

            # TODO validate the request more rigurously

            # Respond with the decision
            response_data["trustLevel"] = True
            return jsonify(response_data), 200

        except MissingResourceAccess as e:
            return jsonify(response_data), 200
        except UserNotFound as e:
            return jsonify(response_data), 200
        except Exception as e:
            print(e)
            return jsonify(response_data), 500
    
    @staticmethod
    def getRole(user):
        return TrustEngine.userDatabase.get(user, None).get("role", None)
        
    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port)
        

# Entry point
if __name__ == "__main__":
    engine = TrustEngine(host='0.0.0.0', port=5001, enforcerModel="src/trustEngine/enforcerModel.conf", enforcerPolicy="src/trustEngine/enforcerPolicy.csv")
    engine.run()