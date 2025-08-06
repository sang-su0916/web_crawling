# 🕷️ Web Scraping Automation Tool

**자동화된 웹 크롤링 프로그램 - 프로그래밍 지식 없이도 사용 가능!**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/sang-su0916/web_crawling)

## 📋 주요 기능

- 🌐 **다양한 웹사이트 자동 크롤링** (뉴스, 주식, 쇼핑, 부동산 등)
- ⏰ **24시간 자동 스케줄링** (매일/매시간/매분 설정 가능)
- 📊 **Excel 파일 자동 저장** (데이터 분석 및 그래프 생성 가능)
- 🔄 **데이터 변경 감지 및 알림** (이메일/웹훅 지원)
- 💾 **SQLite 데이터베이스 저장** (과거 데이터 관리)
- 🛡️ **안정적인 에러 처리** (재시도 로직 및 로깅)
- 🎨 **사용자 친화적 인터페이스** (비개발자도 쉽게 사용)

## 📸 스크린샷

### 메인 프로그램 실행 화면
```
🕷️ 고급 웹 스크래핑 자동화 시스템
============================================================
1. 지금 바로 전체 스크래핑 실행
2. 특정 타겟만 스크래핑
3. 자동 스케줄링 시작
4. 리포트 생성
5. 샘플 설정 파일 생성
6. 데이터베이스 초기화
============================================================
선택하세요 (1-6): 
```

### Excel 결과 파일 예시
| 시간 | KOSPI | 변동률 | 뉴스 헤드라인 | USD 환율 |
|------|-------|--------|---------------|----------|
| 2024-01-15 09:00 | 2,547.10 | +0.8% | 증시 상승 전망 | 1,342.5 |
| 2024-01-15 10:00 | 2,548.30 | +0.85% | 경제 지표 개선 | 1,341.2 |

## 🚀 빠른 시작 (3분 완료!)

### Windows 사용자 (권장)

1. **저장소 다운로드**
   ```bash
   git clone https://github.com/sang-su0916/web_crawling.git
   cd web_crawling
   ```
   
   또는 [ZIP 파일 다운로드](https://github.com/sang-su0916/web_crawling/archive/refs/heads/main.zip)

2. **원클릭 설치**
   ```
   완전자동설치.bat 더블클릭
   ```

3. **프로그램 실행**
   ```
   run_scraper.bat 더블클릭
   ```

4. **첫 사용 설정**
   - 메뉴에서 `5` 선택 (설정 파일 생성)
   - 메뉴에서 `1` 선택 (테스트 실행)

### macOS/Linux 사용자

1. **저장소 다운로드**
   ```bash
   git clone https://github.com/sang-su0916/web_crawling.git
   cd web_crawling
   ```

2. **패키지 설치**
   ```bash
   chmod +x quick_start.sh
   ./quick_start.sh
   ```

3. **프로그램 실행**
   ```bash
   python3 advanced_scraping_automation.py
   ```

## 📦 시스템 요구사항

- **Python**: 3.7 이상
- **운영체제**: Windows 10/11, macOS, Ubuntu/Debian Linux
- **메모리**: 최소 4GB RAM
- **저장공간**: 최소 500MB
- **인터넷**: 패키지 설치 및 웹 크롤링을 위해 필요

## 📚 사용 가이드

### 기본 사용법

1. **설정 파일 생성** (처음에 한 번만)
   ```
   프로그램 실행 → 5번 선택
   ```

2. **테스트 실행**
   ```
   프로그램 실행 → 1번 선택
   ```

3. **결과 확인**
   - `scraping_results_날짜_시간.xlsx` 파일 생성
   - Excel로 열어서 수집된 데이터 확인

### 자동 스케줄링 설정

```json
{
  "name": "네이버_뉴스",
  "url": "https://news.naver.com",
  "type": "news",
  "schedule": "*/30",
  "enabled": true
}
```

**스케줄 설정 예시:**
- `"09:00"`: 매일 오전 9시
- `"*/30"`: 30분마다
- `"*/60"`: 1시간마다

### 지원하는 웹사이트 유형

- 📰 **뉴스 사이트**: 네이버뉴스, 다음뉴스, 구글뉴스
- 📈 **금융 정보**: 네이버증권, 코스피/코스닥, 환율, 암호화폐
- 🛍️ **쇼핑몰**: 쿠팡, G마켓, 11번가, 옥션
- 🏠 **부동산**: 직방, 다방, 네이버부동산
- 🌤️ **날씨**: 네이버날씨, 기상청
- 🎮 **엔터테인먼트**: 스팀, 멜론차트, 영화순위
- 💼 **취업정보**: 사람인, 잡코리아, 원티드

## 🎯 실전 활용 예시

### 1. 부동산 시세 모니터링
```json
{
  "name": "강남구_아파트시세",
  "url": "https://부동산사이트.com/강남구",
  "type": "real_estate",
  "schedule": "09:00",
  "enabled": true
}
```
→ **매일 아침 9시 자동 확인 → Excel 그래프로 추세 분석**

### 2. 쇼핑 할인 알림
```json
{
  "name": "쿠팡_아이폰가격",
  "url": "https://coupang.com/products/아이폰",
  "type": "shopping",
  "schedule": "*/60",
  "enabled": true
}
```
→ **1시간마다 가격 확인 → 할인시 즉시 알림**

### 3. 주식 투자 참고자료
```json
{
  "name": "삼성전자_주가",
  "url": "https://finance.naver.com/item/main.nhn?code=005930",
  "type": "stock",
  "schedule": "15:30",
  "enabled": true
}
```
→ **매일 장 마감 후 확인 → 투자 판단 자료 수집**

## 🛠️ 고급 설정

### 알림 설정 (이메일)
```json
"notifications": {
  "email_enabled": true,
  "email_from": "sender@gmail.com",
  "email_to": "receiver@gmail.com",
  "email_password": "앱비밀번호"
}
```

### 알림 설정 (Slack/Discord)
```json
"notifications": {
  "webhook_enabled": true,
  "webhook_url": "https://hooks.slack.com/services/..."
}
```

### Selenium 사용 (JavaScript 사이트)
```json
{
  "use_selenium": true,
  "selenium_headless": true
}
```

## 📁 파일 구조

```
web_crawling/
├── advanced_scraping_automation.py  # 메인 프로그램
├── requirements.txt                  # Python 패키지 의존성
├── 완전자동설치.bat                   # Windows 원클릭 설치
├── run_scraper.bat                   # Windows 실행 파일
├── quick_start.sh                    # macOS/Linux 설치 스크립트
├── 빠른시작가이드.txt                  # 사용법 요약
├── README_공유용.txt                  # 비개발자용 설명서
├── docs/                            # 문서화
│   ├── installation-guide.md       # 상세 설치 가이드
│   ├── examples.md                  # 실전 예제 모음
│   └── troubleshooting.md          # 문제 해결 가이드
└── examples/                        # 설정 파일 예시
    ├── news_config.json            # 뉴스 사이트 설정
    ├── shopping_config.json        # 쇼핑몰 설정
    └── finance_config.json         # 금융 사이트 설정
```

## 🔧 문제 해결

### 일반적인 문제들

**Q: Python이 설치되지 않았다고 나와요**
```bash
# Windows
완전자동설치.bat 실행 → Python 자동 설치 안내

# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip
```

**Q: 패키지 설치가 실패해요**
```bash
pip install --upgrade pip
pip install -r requirements.txt --only-binary :all:
```

**Q: 웹사이트가 차단되는 것 같아요**
- 스케줄 간격을 30분 이상으로 설정
- User-Agent 변경
- VPN 사용 고려

더 자세한 문제 해결은 [troubleshooting.md](docs/troubleshooting.md) 참조

## 📊 성능 및 한계

### 성능
- **동시 처리**: 최대 5개 사이트 병렬 처리
- **메모리 사용량**: 평균 50-100MB
- **속도**: 사이트당 평균 2-5초

### 한계
- JavaScript 헤비 사이트: Selenium 필요 (느림)
- 로그인 필요 사이트: 수동 설정 필요
- IP 차단: 과도한 요청시 발생 가능

## 🤝 기여하기

### 버그 리포트
- [Issues](https://github.com/sang-su0916/web_crawling/issues)에서 버그 신고
- 오류 메시지와 스크린샷 포함 필수

### 기능 요청
- 새로운 웹사이트 지원 요청
- 기능 개선 제안
- Pull Request 환영

### 개발 환경 설정
```bash
git clone https://github.com/sang-su0916/web_crawling.git
cd web_crawling
pip install -r requirements.txt
python advanced_scraping_automation.py
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## ⚖️ 법적 고지

- 이 도구는 **교육 및 개인적 용도**로만 사용하세요
- **상업적 사용 금지**
- 웹사이트의 `robots.txt` 정책을 준수하세요
- 과도한 요청으로 서버에 부담을 주지 마세요
- **사용자가 모든 법적 책임을 집니다**

## 🎯 로드맵

### v2.0 (계획)
- [ ] GUI 인터페이스 추가
- [ ] Docker 컨테이너 지원
- [ ] 클라우드 배포 지원 (AWS, Google Cloud)
- [ ] 머신러닝 기반 데이터 분석
- [ ] 모바일 앱 연동

### v1.5 (진행중)
- [ ] 더 많은 웹사이트 템플릿
- [ ] 성능 최적화
- [ ] 에러 핸들링 개선
- [ ] 사용자 인터페이스 개선

## 📞 지원

### 문의 및 지원
- **GitHub Issues**: [버그 신고 / 기능 요청](https://github.com/sang-su0916/web_crawling/issues)
- **이메일**: sang.su0916@gmail.com
- **위키**: [상세 문서](https://github.com/sang-su0916/web_crawling/wiki)

### 커뮤니티
- **Discussions**: [Q&A 및 아이디어 공유](https://github.com/sang-su0916/web_crawling/discussions)
- **한국어 지원**: 네이버 카페 "파이썬 자동화" 검색

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sang-su0916/web_crawling&type=Date)](https://star-history.com/#sang-su0916/web_crawling&Date)

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**

**Made with ❤️ by [sang-su0916](https://github.com/sang-su0916)**