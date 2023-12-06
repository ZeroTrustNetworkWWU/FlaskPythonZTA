import requests
from TrustDataBuilder import TrustDataBuilder

# a class that provides the functinallity of the requests library but with zero trust data
class ZTRequests:
    verifyCert = "cert.pem"
    
    # send a get request
    @staticmethod
    def get(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)        
        return requests.get(url, **kwargs, verify=ZTRequests.verifyCert)

    # send a post request
    @staticmethod
    def post(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.post(url, **kwargs, verify=ZTRequests.verifyCert)

    # send a put request
    @staticmethod
    def put(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.put(url, **kwargs, verify=ZTRequests.verifyCert)

    # send a delete request
    @staticmethod
    def delete(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.delete(url, **kwargs, verify=ZTRequests.verifyCert)

    # send a head request
    @staticmethod
    def head(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.head(url, **kwargs, verify=ZTRequests.verifyCert)
    
    # send a special request to the edge node to tell it we want to login
    @staticmethod
    def login(url, user, password, **kwargs):
        payload = {"user": user, "password": password}
        ZTRequests.__addTrustData(kwargs, requestType="login")
        kwargs["json"]["_trustData"].update(payload)
        response = requests.post(url, **kwargs, verify=ZTRequests.verifyCert)
        TrustDataBuilder.sessionToken = response.json().get("session", None)
        return response
    
    # send a special request to the edge node to tell it we want to logout
    @staticmethod
    def logout(url, **kwargs):
        ZTRequests.__addTrustData(kwargs, requestType="logout")
        return requests.post(url, **kwargs, verify=ZTRequests.verifyCert)
    
    # send a special request to the edge node to tell it we want to register
    @staticmethod
    def register(url, user, password, **kwargs):
        pass

    # send a special request to the edge node to tell it we want to remove our account
    @staticmethod
    def removeAccount(url, **kwargs):
        pass
        
    # append the trust data to the json data of the request
    @staticmethod
    def __addTrustData(requestKwargs, requestType="generic"):
        if "json" in requestKwargs.keys():
            TrustDataBuilder.addTrustData(requestKwargs["json"], requestType)
        else:
            requestKwargs["json"] = TrustDataBuilder.getTrustData(requestType)
        
