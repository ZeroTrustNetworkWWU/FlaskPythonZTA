call venv\Scripts\activate
start venv\Scripts\python.exe src\edgeNode\EdgeNode.py
start venv\Scripts\python.exe src\trustEngine\TrustEngine.py
start venv\Scripts\python.exe testing\TestServer.py
start cmd /k venv\Scripts\python.exe src\clientLib\TestClient.py