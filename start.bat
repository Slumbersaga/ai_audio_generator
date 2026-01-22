@echo off
REM Quick Start Script for Gemini TTS Audio Generator
REM This script helps you set up and run the application

echo ========================================
echo  Gemini TTS Audio Generator - Setup
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [!] .env file not found
    echo [+] Creating .env from template...
    copy .env.example .env
    echo.
    echo [!] IMPORTANT: Please edit .env and add your API key
    echo     Get your key from: https://aistudio.google.com/app/apikey
    echo.
    pause
)

REM Check if virtual environment exists
if not exist venv (
    echo [+] Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo [+] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [+] Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo [+] Starting application...
echo.

REM Run the application
python app.py

pause
