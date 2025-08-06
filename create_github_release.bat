@echo off
echo ========================================
echo 🚀 GitHub CLI로 릴리스 생성
echo ========================================
echo.

REM GitHub CLI 설치 확인
gh --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ GitHub CLI가 설치되어 있지 않습니다!
    echo.
    echo 📥 설치 방법:
    echo 1. https://cli.github.com/ 접속
    echo 2. "Download for Windows" 클릭
    echo 3. 설치 후 이 스크립트 다시 실행
    echo.
    echo 또는 winget으로 설치:
    echo winget install GitHub.cli
    echo.
    start https://cli.github.com/
    pause
    exit /b
)

echo ✅ GitHub CLI 확인 완료!
echo.

REM 로그인 상태 확인
gh auth status > nul 2>&1
if %errorlevel% neq 0 (
    echo 🔐 GitHub 로그인이 필요합니다...
    gh auth login
    
    if %errorlevel% neq 0 (
        echo ❌ 로그인 실패
        pause
        exit /b
    )
)

echo ✅ GitHub 인증 완료!
echo.

echo [1/3] 저장소 확인 중...
cd /d "%~dp0"

if not exist ".git" (
    echo Git 저장소 초기화...
    git init
    git remote add origin https://github.com/sang-su0916/web_crawling.git
    git branch -M main
    git add .
    git commit -m "feat: Initial release preparation"
    git push -u origin main
)

echo [2/3] v1.0.0 태그 생성...
git tag -a v1.0.0 -m "Production-ready web scraping automation tool" --force
git push origin v1.0.0 --force

echo [3/3] GitHub 릴리스 생성...
gh release create v1.0.0 ^
--title "🕷️ Web Scraping Automation Tool v1.0.0" ^
--notes "## 🎉 첫 번째 프로덕션 릴리스!

### ✨ 주요 기능
- **🌐 다양한 웹사이트 크롤링**: 뉴스, 금융, 쇼핑, 부동산 등
- **⏰ 24시간 자동 스케줄링**: 매분/매시간/매일 설정 가능  
- **📊 Excel 자동 내보내기**: 데이터 분석 및 그래프 생성
- **🔔 실시간 알림**: 이메일/Slack/Discord 지원
- **🛡️ 안정적인 시스템**: 재시도 로직 및 에러 핸들링
- **👥 비개발자 친화적**: 프로그래밍 지식 없이도 3분 설치

### 🚀 빠른 시작
1. **Windows**: `완전자동설치.bat` → `run_scraper.bat`
2. **macOS/Linux**: `./quick_start.sh` → `python3 advanced_scraping_automation.py`
3. **수동 설치**: `pip install -r requirements.txt`

### 📦 포함된 파일
- `advanced_scraping_automation.py` - 메인 프로그램
- `requirements.txt` - 의존성 패키지  
- `완전자동설치.bat` - Windows 원클릭 설치
- `run_scraper.bat` - Windows 실행 도구
- `quick_start.sh` - macOS/Linux 설치 스크립트
- `docs/` - 상세 문서 및 가이드
- `examples/` - 설정 파일 예시

### 🎯 실전 활용
- **부동산 시세 모니터링**: 매일 아침 자동 수집
- **쇼핑 할인 추적**: 가격 변동시 즉시 알림  
- **뉴스 모니터링**: 키워드별 뉴스 자동 수집
- **주식 정보 추적**: 관심 종목 자동 모니터링

### ⚠️ 사용 시 주의사항
- 웹사이트 이용약관 준수 필수
- 적절한 스케줄 간격 설정 (최소 30분 권장)
- 개인정보 수집 금지
- 상업적 사용 제한

### 📞 지원
- **GitHub Issues**: 버그 신고 및 기능 요청
- **이메일**: sang.su0916@gmail.com
- **문서**: README.md 및 docs/ 폴더 참조

**🌟 전 세계 누구나 3분 만에 웹 크롤링 자동화를 시작할 수 있습니다!**

---
🤖 *Generated with Claude Code*  
*Co-Authored-By: Claude <noreply@anthropic.com>*"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 🎉 릴리스 v1.0.0 생성 성공!
    echo ========================================
    echo.
    echo 📦 릴리스 페이지: https://github.com/sang-su0916/web_crawling/releases/tag/v1.0.0
    echo.
    echo ✅ 이제 사용자들이 할 수 있는 것들:
    echo • Source code ZIP 다운로드
    echo • 안정된 v1.0.0 버전 사용  
    echo • GitHub에서 자동 업데이트 알림
    echo • 릴리스 노트로 변경사항 확인
    echo.
    
    echo 브라우저에서 릴리스를 확인하시겠습니까? (y/n)
    set /p view_release=선택: 
    if /i "%view_release%"=="y" (
        start https://github.com/sang-su0916/web_crawling/releases/tag/v1.0.0
    )
    
    echo.
    echo 🎊 축하합니다! 프로덕션 준비 완료된 오픈소스 프로젝트입니다!
) else (
    echo ❌ 릴리스 생성 실패
    echo GitHub 웹사이트에서 수동으로 릴리스를 생성해주세요.
    echo https://github.com/sang-su0916/web_crawling/releases/new
)

echo.
pause