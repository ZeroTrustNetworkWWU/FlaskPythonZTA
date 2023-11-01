import requests
from TrustDataBuilder import TrustDataBuilder

# a class that provides the functinallity of the requests library but with zero trust data
class ZTRequests:
    # send a get request
    @staticmethod
    def get(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.get(url, **kwargs)

    # send a post request
    @staticmethod
    def post(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.post(url, **kwargs)

    # send a put request
    @staticmethod
    def put(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.put(url, **kwargs)

    # send a delete request
    @staticmethod
    def delete(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.delete(url, **kwargs)

    # send a head request
    @staticmethod
    def head(url, **kwargs):
        ZTRequests.__addTrustData(kwargs)
        return requests.head(url, **kwargs)
    
    # append the trust data to the json data of the request
    @staticmethod
    def __addTrustData(requestKwargs):
        if "json" in requestKwargs.keys():
            TrustDataBuilder.addTrustData(requestKwargs["json"])
        else:
            requestKwargs["json"] = TrustDataBuilder.getTrustData()
        
