import requests
import platform
from datetime import datetime

# Class that gets the data needed to verify the trust of the client
class TrustDataBuilder:
    # Appends trust data to the data object
    @staticmethod
    def addTrustData(data):
        user = TrustDataBuilder.__getUser()
        device = TrustDataBuilder.__getDevice()
        time = TrustDataBuilder.__getTime()

        trustData = {
            "user": user,
            "device": device,
            "time": time
        }

        data["_trustData"] = trustData

    # Returns a dict with the trust data and nothing else
    @staticmethod
    def getTrustData():
        user = TrustDataBuilder.__getUser()
        device = TrustDataBuilder.__getDevice()
        time = TrustDataBuilder.__getTime()

        trustData = {
            "user": user,
            "device": device,
            "time": time
        }
        trustData = {"_trustData": trustData}

        return trustData

    # Get the user
    @staticmethod
    def __getUser():
        return "user"

    # Get info about the device
    @staticmethod
    def __getDevice():
        uname = platform.uname()
        return {"System" : uname.system,
                "NodeName" : uname.node,
                "Release" : uname.release,
                "Version" : uname.version,
                "Machine" : uname.machine,
                }

    # Get the time
    @staticmethod
    def __getTime():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        
