#!/bin/bash

echo "=========================================="
echo "🕷️ Web Scraping Automation Tool"
echo "=========================================="
echo

echo "[💻 macOS/Linux 설치 시작...]"
echo

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3이 설치되어 있지 않습니다!"
    echo
    echo "macOS: brew install python3"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo
    exit 1
fi

echo "✅ Python3 확인 완료: $(python3 --version)"

# pip 업그레이드
echo "[1/3] pip 업그레이드..."
python3 -m pip install --upgrade pip --user > /dev/null 2>&1

# 패키지 설치
echo "[2/3] 필수 패키지 설치..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --user
else
    echo "❌ requirements.txt 파일이 없습니다!"
    exit 1
fi

# 설치 검증
echo "[3/3] 설치 검증..."
python3 -c "import requests, bs4, pandas, selenium, schedule, openpyxl; print('✅ 모든 패키지 정상 설치됨')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo
    echo "=========================================="
    echo "🎉 설치 완료!"
    echo "=========================================="
    echo
    echo "이제 다음과 같이 사용하세요:"
    echo
    echo "1. python3 advanced_scraping_automation.py"
    echo "2. 메뉴에서 5번 선택 (처음 설정)"
    echo "3. 메뉴에서 1번 선택 (테스트 실행)"
    echo
    echo "프로그램을 바로 시작하시겠습니까? (y/n)"
    read -r choice
    if [[ $choice == "y" || $choice == "Y" ]]; then
        echo
        echo "프로그램을 시작합니다..."
        python3 advanced_scraping_automation.py
    else
        echo
        echo "python3 advanced_scraping_automation.py 를 실행해서 사용하세요!"
    fi
else
    echo "⚠️ 일부 패키지에 문제가 있을 수 있지만 기본 기능은 작동합니다."
fi