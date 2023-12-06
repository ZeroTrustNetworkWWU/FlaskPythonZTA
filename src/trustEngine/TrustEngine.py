from flask import Flask, request, jsonify
from TrustEngineExceptions import MissingResourceAccess, UserNotFound, InvalidLogin
from UserDataHandler import UserDataHandler
import casbin
import casbin_sqlalchemy_adapter

# Create a Flask app instance
app = Flask(__name__)

class TrustEngine:
    def __init__(self, host, port, enforcerModel, accessEnforcer, userDb):
        # Prepare the user database
        TrustEngine.userDatabase = UserDataHandler(userDb)

        # Define the access enforcer for the trust engine
        adapter = casbin_sqlalchemy_adapter.Adapter("sqlite:///" + accessEnforcer)
        TrustEngine.accessEnforcer = casbin.Enforcer(enforcerModel, adapter)

        # TODO remove this
        TrustEngine.accessEnforcer.add_policy("admin", "/*", "*")
            
        self.host = host
        self.port = port
    
    @app.route('/getDecision', methods=['POST'])
    def getDecision():
        response_data = {"trustLevel": False, "session": None}
        try:
            data = request.get_json()
            session = data.get("session", None)

            if not TrustEngine.userDatabase.validateSession(session):
                raise InvalidLogin("Invalid session token")

            role = TrustEngine.userDatabase.getRoleFromSession(session)
            if role is None:
                raise UserNotFound("Cannot match session to role")
        
            # Validate that the user has access to the resource
            if not TrustEngine.accessEnforcer.enforce(role, data["resource"], data["action"]):
                raise MissingResourceAccess("User does not have access to this resource")

            # TODO validate the request more rigurously

            # Respond with the decision
            response_data["trustLevel"] = True
            response_data["session"] = session
            return jsonify(response_data), 200

        except MissingResourceAccess as e:
            return jsonify(response_data), 200
        except UserNotFound as e:
            return jsonify(response_data), 200
        except InvalidLogin as e:
            return jsonify(response_data), 200
        
    @app.route('/login', methods=['POST'])
    def login():
        response_data = {"trustLevel": False, "session": None}
        try:
            data = request.get_json()

            if not TrustEngine.userDatabase.validateUser(data):
                raise InvalidLogin("Invalid login request")

            # TODO validate the request more rigurously

            session = TrustEngine.userDatabase.getNewSessionToken(data["user"])
            
            response_data["trustLevel"] = True
            response_data["session"] = session
            
            return jsonify(response_data), 200
        
        except InvalidLogin as e:
            return jsonify(response_data), 200

    @app.route('/logout', methods=['POST'])
    def logout():
        pass

    @app.route('/register', methods=['POST'])
    def register():
        pass

    @app.route('/removeAccount', methods=['POST'])
    def removeAccount():
        pass
        
    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port, ssl_context=('cert.pem', 'key.pem'))

# Entry point
if __name__ == "__main__":
    engine = TrustEngine(host='0.0.0.0', port=5001, enforcerModel="src/trustEngine/enforcerModel.conf", accessEnforcer="src/trustEngine/AccessEnforcer.db", userDb="src/trustEngine/UserData.db")
    engine.run()