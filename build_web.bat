@echo off
echo.
echo ========================================
echo   PAC-MAN - Web Deployment Build
echo ========================================
echo.

REM Check if pygbag is installed
python -m pygbag --version >nul 2>&1
if errorlevel 1 (
    echo Installing Pygbag...
    pip install pygbag --break-system-packages
)

REM Create build directory
if not exist build mkdir build

echo Copying game files...
xcopy /Y /Q main.py build\ >nul 2>&1
xcopy /E /I /Y /Q src build\src\ >nul 2>&1
xcopy /E /I /Y /Q assets build\assets\ >nul 2>&1
xcopy /Y /Q requirements.txt build\ >nul 2>&1

echo.
echo Building with Pygbag...
cd build
python -m pygbag .

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo To test locally:
echo   1. Stay in the build directory
echo   2. Run: python -m http.server 8000
echo   3. Open http://localhost:8000
echo.
echo To deploy:
echo   Upload the build folder to your web host
echo.
pause
