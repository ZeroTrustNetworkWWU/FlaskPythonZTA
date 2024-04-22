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


@REM REM Start test Backend server
@REM start cmd /k venv\Scripts\python.exe src\testing\TestServer.py

REM Start EdgeNode server
cd "EdgeNode"
cmd /c start.bat

REM Start TrustEngine server
cd "../TrustEngine"
cmd /c start.bat

@REM REM Start TestClient
@REM cd "../PythonAPI"
@REM cmd /c start.bat

REM Start Admin GUI
cd "../AdminGUI"
cmd /c start.bat

