# A very simple test server 

from flask import Flask, request, jsonify

app = Flask(__name__)

class testServer:
    def __init__(self):
        pass

    # Test post
    @app.route('/testPost', methods=['POST'])
    def testPost():
        return jsonify("POST was successful")
    
    # Test get
    @app.route('/testGet', methods=['GET'])
    def testGet():
        return jsonify("GET was successful")
    
    # Test put 
    @app.route('/testPut', methods=['PUT'])
    def testPut():
        return jsonify("PUT was successful")
    
    # Test delete
    @app.route('/testDelete', methods=['DELETE'])
    def testDelete():
        return jsonify("DELETE was successful")
    
    # Test head
    @app.route('/testHead', methods=['HEAD'])
    def testHead():
        return jsonify("HEAD was successful")
    
    # Start the server
    def run(self):
        app.run(host='0.0.0.0', port=5002, ssl_context=('cert.pem', 'key.pem'))

# Entry point
if __name__ == "__main__":
    server = testServer()
    server.run()

    

