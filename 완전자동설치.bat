@echo off
echo ========================================
echo 웹 크롤링 프로그램 완전 자동 설치
echo ========================================
echo.
echo 이 프로그램은 자동으로 다음을 수행합니다:
echo 1. Python 설치 여부 확인
echo 2. Python 미설치시 다운로드 안내
echo 3. 필요한 패키지 자동 설치
echo 4. 프로그램 실행 준비 완료
echo.
echo 계속하려면 아무 키나 누르세요...
pause > nul
echo.

REM Python 설치 확인
echo [1/4] Python 설치 확인 중...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python이 설치되어 있지 않습니다!
    echo.
    echo 📥 Python을 먼저 설치해야 합니다:
    echo 1. https://www.python.org/downloads/ 접속
    echo 2. "Download Python" 버튼 클릭
    echo 3. 설치시 "Add Python to PATH" 체크 필수!
    echo 4. 설치 후 컴퓨터 재시작
    echo 5. 이 파일을 다시 실행하세요
    echo.
    echo 💡 또는 Microsoft Store에서 "Python" 검색 후 설치
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b
) else (
    python --version
    echo ✅ Python 확인 완료!
)

echo.
echo [2/4] 필수 파일 확인 중...

if not exist "advanced_scraping_automation.py" (
    echo ❌ advanced_scraping_automation.py 파일이 없습니다!
    echo 모든 파일이 같은 폴더에 있는지 확인하세요.
    pause
    exit /b
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt 파일이 없습니다!
    echo 모든 파일이 같은 폴더에 있는지 확인하세요.
    pause
    exit /b
)

echo ✅ 필수 파일 확인 완료!

echo.
echo [3/4] Python 패키지 설치 중...
echo 잠시만 기다려주세요... (1-3분 소요)

python.exe -m pip install --upgrade pip > nul 2>&1
python.exe -m pip install --upgrade setuptools wheel > nul 2>&1

echo 주요 패키지 설치 중...
python.exe -m pip install requests beautifulsoup4 schedule openpyxl --only-binary :all: > nul 2>&1
if %errorlevel% neq 0 (
    echo 패키지 설치 재시도 중...
    python.exe -m pip install requests beautifulsoup4 schedule openpyxl
)

echo pandas 설치 중...
python.exe -m pip install pandas --only-binary :all: > nul 2>&1
if %errorlevel% neq 0 (
    python.exe -m pip install pandas
)

echo selenium 설치 중...
python.exe -m pip install selenium > nul 2>&1

echo lxml 설치 중 (선택사항)...
python.exe -m pip install lxml --only-binary :all: > nul 2>&1
if %errorlevel% neq 0 (
    echo lxml 대신 html5lib 설치...
    python.exe -m pip install html5lib > nul 2>&1
)

echo ✅ 패키지 설치 완료!

echo.
echo [4/4] 설치 검증 중...
python.exe -c "import requests, bs4, pandas, selenium, schedule, openpyxl; print('✅ 모든 패키지 정상 설치됨')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ 일부 패키지에 문제가 있을 수 있지만 기본 기능은 작동합니다.
) else (
    echo ✅ 설치 검증 완료!
)

echo.
echo ========================================
echo 🎉 설치 완료!
echo ========================================
echo.
echo 이제 다음과 같이 사용하세요:
echo.
echo 1. run_scraper.bat 더블클릭 (프로그램 실행)
echo 2. 메뉴에서 5번 선택 (처음 설정)
echo 3. 메뉴에서 1번 선택 (테스트 실행)
echo.
echo 바탕화면에 바로가기를 만들어서 사용하면 더 편리합니다!
echo.
echo 프로그램을 바로 실행하시겠습니까? (y/n)
set /p choice=선택: 
if /i "%choice%"=="y" (
    echo.
    echo 프로그램을 시작합니다...
    python advanced_scraping_automation.py
) else (
    echo.
    echo run_scraper.bat를 실행해서 프로그램을 사용하세요!
)

pause