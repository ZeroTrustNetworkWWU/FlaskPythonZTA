@echo off

@echo off

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    REM Activate existing venv
    call venv\Scripts\activate.bat
)


REM Start Backend server
start cmd /k venv\Scripts\python.exe src\testing\TestServer.py

REM Start EdgeNode server
cd "EdgeNode"
cmd /c start.bat

REM Start TrustEngine server
cd "../TrustEngine"
cmd /c start.bat

REM Start TestClient
cd "../PythonAPI"
cmd /c start.bat

