import platform
from datetime import datetime

# Class that gets the data needed to verify the trust of the client
class TrustDataBuilder:
    # Static members that are used to store trust data for this device
    sessionToken = None

    # Appends trust data to the data object
    @staticmethod
    def addTrustData(data, requestType):
        device = TrustDataBuilder.__getDevice()
        time = TrustDataBuilder.__getTime()

        trustData = {
            "session": TrustDataBuilder.sessionToken,
            "device": device,
            "time": time,
            "requestType": requestType
        }

        data["_trustData"] = trustData

    # Returns a dict with the trust data and nothing else
    @staticmethod
    def getTrustData(requestType):
        device = TrustDataBuilder.__getDevice()
        time = TrustDataBuilder.__getTime()

        trustData = {
            "session": TrustDataBuilder.sessionToken,
            "device": device,
            "time": time,
            "requestType": requestType
        }
        trustData = {"_trustData": trustData}

        return trustData

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

        
