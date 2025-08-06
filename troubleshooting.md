# 문제 해결 가이드

## 일반적인 문제들

### Python 관련 문제

**Q: "python is not recognized"**
- Python PATH 설정 확인
- 재설치 시 "Add Python to PATH" 체크

**Q: 패키지 설치 실패**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --only-binary :all:
```

### 웹 크롤링 문제

**Q: 사이트 접근 차단**
- 스케줄 간격 늘리기 (30분 이상)
- User-Agent 변경
- VPN 사용

**Q: JavaScript 사이트 크롤링 실패**
- `use_selenium: true` 설정
- Chrome 브라우저 설치 필요

### 성능 문제

**Q: 메모리 사용량 과다**
- 동시 처리 웹사이트 수 줄이기
- 스케줄 간격 늘리기

## 로그 확인

에러 발생 시 `scraping_automation.log` 파일 확인

## 지원 요청

문제 지속 시:
1. GitHub Issues에 버그 리포트
2. 오류 메시지와 로그 파일 첨부
3. 시스템 정보 포함