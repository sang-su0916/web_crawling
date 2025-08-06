@echo off
echo ========================================
echo 🕷️ Web Scraping Automation Tool
echo ========================================
echo.
echo 웹 크롤링 프로그램을 시작합니다...
echo.

REM Python 설치 확인
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되어 있지 않습니다!
    echo 완전자동설치.bat를 먼저 실행하세요.
    pause
    exit /b
)

REM 메인 프로그램 실행
python advanced_scraping_automation.py

echo.
echo 프로그램이 종료되었습니다.
pause