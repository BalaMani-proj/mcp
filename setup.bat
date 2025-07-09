@echo off
REM Create virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies (you can add more here)
pip install flask connexion

REM Freeze dependencies to requirements.txt
pip freeze > requirements.txt

echo.
echo Virtual environment set up and requirements.txt created!
pause
