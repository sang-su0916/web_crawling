# 설치 가이드

## 시스템 요구사항

- Python 3.7 이상
- Windows 10/11, macOS, Linux
- 4GB RAM 이상
- 500MB 저장공간

## Windows 설치

### 방법 1: 원클릭 설치 (권장)
1. `완전자동설치.bat` 더블클릭
2. 화면 지시에 따라 진행
3. `run_scraper.bat` 실행

### 방법 2: 수동 설치
```cmd
python -m pip install -r requirements.txt
python advanced_scraping_automation.py
```

## macOS/Linux 설치

```bash
chmod +x quick_start.sh
./quick_start.sh
```

## 문제 해결

### Python 설치 오류
- Windows: Microsoft Store에서 "Python" 검색
- macOS: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

### 패키지 설치 실패
```bash
pip install --upgrade pip
pip install -r requirements.txt --only-binary :all:
```