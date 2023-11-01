# A very simple test server 

from flask import Flask, request, jsonify

app = Flask(__name__)

class testServer:
    def __init__(self):
        pass

    # Test post
    @app.route('/testPost', methods=['POST'])
    def testPost():
        return jsonify({'data': "What did you think I was going to do with that POST"})
    
    # Test get
    @app.route('/testGet', methods=['GET'])
    def testGet():
        return jsonify({'data': "What did you you think You would GET"})
    
    # Test put 
    @app.route('/testPut', methods=['PUT'])
    def testPut():
        return jsonify({'data': "What did you think I was going to do with that PUT"})
    
    # Test delete
    @app.route('/testDelete', methods=['DELETE'])
    def testDelete():
        return jsonify({'data': "What did you think I was going to DELETE"})
    
    # Test head
    @app.route('/testHead', methods=['HEAD'])
    def testHead():
        return jsonify({'data': "What did you think I was going to do with that HEAD"})
    
    # Start the server
    def run(self):
        app.run(host='0.0.0.0', port=5002)

# Entry point
if __name__ == "__main__":
    server = testServer()
    server.run()

    

