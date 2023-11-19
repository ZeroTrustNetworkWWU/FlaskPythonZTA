from flask import Flask, request, jsonify
from TrustEngineExceptions import MissingResourceAccess, UserNotFound, InvalidLogin
import casbin

from datetime import datetime, timedelta

# Create a Flask app instance
app = Flask(__name__)

class TrustEngine:
    def __init__(self, host, port, enforcerModel, enforcerPolicy):
        # Define a static enforcer and user database for all TrustEngine instances
        TrustEngine.accessEnforcer = casbin.Enforcer(enforcerModel, enforcerPolicy)
        TrustEngine.userDatabase = {
            "user1": {
                "role": "admin",
                "session": None,
                "sessionExpiration": None
            },
            "user2": {
                "role": "user",
                "session": None,
                "sessionExpiration": None
            }
        }
        TrustEngine.tokenIndex = 0

        self.host = host
        self.port = port
    
    @app.route('/getDecision', methods=['POST'])
    def getDecision():
        response_data = {"trustLevel": False, "session": None}
        try:
            data = request.get_json()
            session = data.get("session", None)

            # TODO make a route for login requests specifically
            # It the session is not in the request data then this is a login request and should be handled differently
            if session is None and TrustEngine.validateUser(data):
                session = TrustEngine.getNewSessionToken(data["login"]["user"])
                response_data["session"] = session
                response_data["trustLevel"] = True
                return jsonify(response_data), 200

            if not TrustEngine.validateSession(session):
                raise InvalidLogin("Invalid session token")

            role = TrustEngine.getRoleFromSession(session)
            if role is None:
                raise UserNotFound("cannot match session to user")
        
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
            return jsonify(response_data), 500
        except Exception as e:
            print(e)
            return jsonify(response_data), 500
    
    @staticmethod
    def getRoleFromUser(user):
        return TrustEngine.userDatabase.get(user, None).get("role", None)
    
    @staticmethod
    def getRoleFromSession(session):
        for user in TrustEngine.userDatabase.keys():
            if TrustEngine.userDatabase[user]["session"] == session:
                return TrustEngine.userDatabase[user]["role"]
        return None
    
    @staticmethod
    def validateUser(data):
        if "login" in data.keys():
            user = data["login"].get("user", None)
            password = data["login"].get("password", None)
            if not TrustEngine.userExists(user):
                raise InvalidLogin("Invalid username")
            return True
        else:
            return False
        
    @staticmethod
    def validateSession(session):
        if session is None:
            return False
        for user in TrustEngine.userDatabase.keys():
            if TrustEngine.userDatabase[user]["session"] == session:
                return TrustEngine.userDatabase[user]["sessionExpiration"] > datetime.now()
        return False
        
    @staticmethod
    def getNewSessionToken(user):
        # set the data base session token to the new session token
        TrustEngine.userDatabase[user]["session"] = TrustEngine.tokenIndex
        TrustEngine.userDatabase[user]["sessionExpiration"] = datetime.now() + timedelta(minutes=30)

        # increment the token index
        TrustEngine.tokenIndex += 1

        return TrustEngine.userDatabase[user]["session"]
    
    @staticmethod
    def userExists(user):
        return user in TrustEngine.userDatabase.keys()
        
    # Start the Flask app
    def run(self):
        app.run(host=self.host, port=self.port)
        

# Entry point
if __name__ == "__main__":
    engine = TrustEngine(host='0.0.0.0', port=5001, enforcerModel="src/trustEngine/enforcerModel.conf", enforcerPolicy="src/trustEngine/enforcerPolicy.csv")
    engine.run()