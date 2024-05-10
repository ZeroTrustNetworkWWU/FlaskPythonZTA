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


@REM REM Start EdgeNode server
@REM cd "%0/../EdgeNode"
@REM cmd /c start.bat

REM Start TrustEngine server
cd "%0/../TrustEngine"
cmd /c start.bat

@REM REM Start TestClient
@REM cd "%0/../PythonAPI"
@REM cmd /c start.bat

@REM REM Start Admin GUI
@REM cd "%0/../AdminGUI"
@REM cmd /c start.bat

REM Start test TrustEngineAPI
cd "%0/.."
start cmd /k venv\Scripts\python.exe src\testing\Trying.py
