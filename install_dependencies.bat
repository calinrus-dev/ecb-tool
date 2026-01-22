@echo off
echo ========================================
echo Installing ECB Tool Dependencies
echo ========================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install core dependencies
echo Installing core dependencies...
pip install PyQt6>=6.4.0
pip install ffmpeg-python>=0.2.0

REM Install Google/YouTube dependencies
echo Installing YouTube API dependencies...
pip install google-auth>=2.16.0
pip install google-auth-oauthlib>=1.0.0
pip install google-auth-httplib2>=0.1.0
pip install google-api-python-client>=2.70.0

REM Install other dependencies
echo Installing other dependencies...
pip install Pillow>=9.0.0
pip install requests>=2.28.0

REM Install dev dependencies (optional)
echo.
echo Do you want to install development dependencies? (Y/N)
set /p install_dev=
if /i "%install_dev%"=="Y" (
    echo Installing dev dependencies...
    pip install pytest>=7.0.0
    pip install pytest-qt>=4.0.0
    pip install pytest-cov>=4.0.0
    pip install flake8>=6.0.0
    pip install black>=23.0.0
    pip install mypy>=1.0.0
)

REM Install package in editable mode
echo.
echo Installing ECB Tool package...
pip install -e .

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Run the application with:
echo   python main_new.py
echo.
echo Or run tests with:
echo   pytest
echo.
pause
