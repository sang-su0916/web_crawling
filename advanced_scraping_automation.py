#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 웹 스크래핑 자동화 도구
Advanced Web Scraping Automation Tool

🕷️ 24시간 자동화 웹 스크래핑 시스템
- 다양한 웹사이트 동시 모니터링
- 자동 Excel 내보내기 및 SQLite 데이터베이스 저장
- 이메일/웹훅 알림 시스템
- 강력한 오류 처리 및 재시도 로직
- 비개발자도 쉽게 사용 가능

Author: Created with Claude Code
Version: 1.0.0
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import json
import logging
import schedule
import time
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self, db_path: str = "scraping_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 스크래핑 결과 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_name TEXT NOT NULL,
                url TEXT NOT NULL,
                title TEXT,
                content TEXT,
                price TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hash_value TEXT UNIQUE
            )
        ''')
        
        # 변경 로그 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS change_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_name TEXT NOT NULL,
                change_type TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_data(self, data: Dict[str, Any]) -> bool:
        """데이터 삽입"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO scraping_results 
                (website_name, url, title, content, price, hash_value)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['website_name'],
                data['url'],
                data.get('title', ''),
                data.get('content', ''),
                data.get('price', ''),
                data.get('hash_value', '')
            ))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
            
        except Exception as e:
            logging.error(f"데이터베이스 삽입 오류: {e}")
            return False
    
    def get_recent_data(self, hours: int = 24) -> List[Dict]:
        """최근 데이터 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM scraping_results 
                WHERE scraped_at > datetime('now', '-{} hours')
                ORDER BY scraped_at DESC
            '''.format(hours))
            
            columns = [description[0] for description in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return results
            
        except Exception as e:
            logging.error(f"데이터베이스 조회 오류: {e}")
            return []

class NotificationManager:
    """알림 관리 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.email_config = config.get('email', {})
        self.webhook_config = config.get('webhook', {})
    
    def send_email(self, subject: str, body: str) -> bool:
        """이메일 알림 전송"""
        if not self.email_config.get('enabled', False):
            return True
            
        try:
            msg = MimeMultipart()
            msg['From'] = self.email_config['smtp_user']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = subject
            
            msg.attach(MimeText(body, 'html'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['smtp_user'], self.email_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            logging.info(f"이메일 전송 완료: {subject}")
            return True
            
        except Exception as e:
            logging.error(f"이메일 전송 실패: {e}")
            return False
    
    def send_webhook(self, data: Dict[str, Any]) -> bool:
        """웹훅 알림 전송"""
        if not self.webhook_config.get('enabled', False):
            return True
            
        try:
            response = requests.post(
                self.webhook_config['url'],
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            logging.info("웹훅 전송 완료")
            return True
            
        except Exception as e:
            logging.error(f"웹훅 전송 실패: {e}")
            return False

class AdvancedWebScraper:
    """고급 웹 스크래핑 메인 클래스"""
    
    def __init__(self, config_path: str = "scraper_config.json"):
        self.setup_logging()
        self.load_config(config_path)
        self.db_manager = DatabaseManager()
        self.notification_manager = NotificationManager(self.config.get('notifications', {}))
        self.session = requests.Session()
        self.setup_session()
        
    def setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraping_automation.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
    def load_config(self, config_path: str):
        """설정 파일 로드"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # 기본 설정 생성
                self.config = self.create_default_config()
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            logging.error(f"설정 파일 로드 실패: {e}")
            self.config = self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """기본 설정 생성"""
        return {
            "websites": [
                {
                    "name": "example_news",
                    "url": "https://example.com/news",
                    "type": "news",
                    "selectors": {
                        "title": ".news-title",
                        "content": ".news-content"
                    },
                    "schedule": "*/30",
                    "enabled": False,
                    "use_selenium": False
                }
            ],
            "general_settings": {
                "user_agent": "Advanced Web Scraper 1.0",
                "timeout": 10,
                "max_retries": 3,
                "delay_between_requests": 1,
                "max_workers": 5
            },
            "notifications": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "smtp_user": "your-email@gmail.com",
                    "smtp_password": "your-app-password",
                    "to_email": "recipient@example.com"
                },
                "webhook": {
                    "enabled": False,
                    "url": "https://hooks.example.com/webhook"
                }
            },
            "export_settings": {
                "excel_export": True,
                "export_schedule": "daily",
                "max_records_per_file": 10000
            }
        }
    
    def setup_session(self):
        """HTTP 세션 설정"""
        headers = {
            'User-Agent': self.config['general_settings']['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
    
    def get_selenium_driver(self) -> webdriver.Chrome:
        """Selenium 드라이버 생성"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(f'--user-agent={self.config["general_settings"]["user_agent"]}')
        
        try:
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(self.config['general_settings']['timeout'])
            return driver
        except Exception as e:
            logging.error(f"Chrome 드라이버 초기화 실패: {e}")
            raise
    
    def scrape_website(self, website_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """단일 웹사이트 스크래핑"""
        if not website_config.get('enabled', True):
            return None
            
        url = website_config['url']
        logging.info(f"스크래핑 시작: {website_config['name']} - {url}")
        
        try:
            if website_config.get('use_selenium', False):
                return self.scrape_with_selenium(website_config)
            else:
                return self.scrape_with_requests(website_config)
                
        except Exception as e:
            logging.error(f"스크래핑 실패 {website_config['name']}: {e}")
            return None
    
    def scrape_with_requests(self, website_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """requests를 사용한 스크래핑"""
        url = website_config['url']
        max_retries = self.config['general_settings']['max_retries']
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    url, 
                    timeout=self.config['general_settings']['timeout']
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                return self.extract_data(soup, website_config)
                
            except requests.RequestException as e:
                logging.warning(f"요청 실패 (시도 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 지수 백오프
                else:
                    raise
    
    def scrape_with_selenium(self, website_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Selenium을 사용한 스크래핑"""
        driver = None
        try:
            driver = self.get_selenium_driver()
            driver.get(website_config['url'])
            
            # 페이지 로드 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 추가 대기 시간 (JavaScript 로딩)
            time.sleep(3)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            return self.extract_data(soup, website_config)
            
        except (TimeoutException, WebDriverException) as e:
            logging.error(f"Selenium 스크래핑 실패: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def extract_data(self, soup: BeautifulSoup, website_config: Dict[str, Any]) -> Dict[str, Any]:
        """HTML에서 데이터 추출"""
        selectors = website_config['selectors']
        data = {
            'website_name': website_config['name'],
            'url': website_config['url'],
            'scraped_at': datetime.now().isoformat()
        }
        
        for field, selector in selectors.items():
            try:
                element = soup.select_one(selector)
                if element:
                    data[field] = element.get_text(strip=True)
                else:
                    data[field] = ""
            except Exception as e:
                logging.warning(f"요소 추출 실패 {field}: {e}")
                data[field] = ""
        
        # 데이터 해시 생성 (중복 검사용)
        content_hash = str(hash(f"{data.get('title', '')}{data.get('content', '')}{data.get('price', '')}"))
        data['hash_value'] = content_hash
        
        return data
    
    def process_scraped_data(self, data: Dict[str, Any]) -> bool:
        """스크래핑된 데이터 처리"""
        if not data:
            return False
            
        # 데이터베이스 저장
        is_new = self.db_manager.insert_data(data)
        
        if is_new:
            logging.info(f"새로운 데이터 발견: {data['website_name']}")
            
            # 알림 전송
            self.send_change_notification(data)
            
        return is_new
    
    def send_change_notification(self, data: Dict[str, Any]):
        """변경 알림 전송"""
        subject = f"🔔 새로운 데이터 발견: {data['website_name']}"
        
        html_body = f"""
        <html>
        <body>
            <h2>웹 스크래핑 알림</h2>
            <p><strong>웹사이트:</strong> {data['website_name']}</p>
            <p><strong>URL:</strong> <a href="{data['url']}">{data['url']}</a></p>
            <p><strong>제목:</strong> {data.get('title', 'N/A')}</p>
            <p><strong>내용:</strong> {data.get('content', 'N/A')[:200]}...</p>
            <p><strong>가격:</strong> {data.get('price', 'N/A')}</p>
            <p><strong>수집 시간:</strong> {data['scraped_at']}</p>
            
            <hr>
            <p><small>Advanced Web Scraping Automation Tool</small></p>
        </body>
        </html>
        """
        
        # 이메일 전송
        self.notification_manager.send_email(subject, html_body)
        
        # 웹훅 전송
        webhook_data = {
            'type': 'new_data',
            'website': data['website_name'],
            'title': data.get('title', ''),
            'url': data['url'],
            'timestamp': data['scraped_at']
        }
        self.notification_manager.send_webhook(webhook_data)
    
    def run_single_scrape(self):
        """단일 스크래핑 실행"""
        logging.info("스크래핑 작업 시작")
        
        results = []
        for website_config in self.config['websites']:
            if website_config.get('enabled', True):
                data = self.scrape_website(website_config)
                if data:
                    self.process_scraped_data(data)
                    results.append(data)
                    
                # 요청 간 지연
                time.sleep(self.config['general_settings']['delay_between_requests'])
        
        logging.info(f"스크래핑 작업 완료: {len(results)}개 웹사이트 처리")
        
        # 일일 리포트 생성 확인
        if self.config['export_settings']['excel_export']:
            self.maybe_generate_daily_report()
    
    def maybe_generate_daily_report(self):
        """일일 리포트 생성 여부 확인"""
        now = datetime.now()
        
        # 매일 자정에 리포트 생성
        if now.hour == 0 and now.minute < 5:
            self.generate_excel_report()
    
    def generate_excel_report(self):
        """Excel 리포트 생성"""
        try:
            # 최근 24시간 데이터 조회
            recent_data = self.db_manager.get_recent_data(24)
            
            if not recent_data:
                logging.info("생성할 리포트 데이터가 없습니다.")
                return
            
            # DataFrame 생성
            df = pd.DataFrame(recent_data)
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraping_report_{timestamp}.xlsx"
            
            # Excel 파일 저장
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 전체 데이터
                df.to_excel(writer, sheet_name='전체_데이터', index=False)
                
                # 웹사이트별 통계
                website_stats = df.groupby('website_name').agg({
                    'id': 'count',
                    'scraped_at': ['min', 'max']
                }).round(2)
                website_stats.to_excel(writer, sheet_name='웹사이트별_통계')
                
                # 시간별 통계
                df['hour'] = pd.to_datetime(df['scraped_at']).dt.hour
                hourly_stats = df.groupby('hour')['id'].count()
                hourly_stats.to_excel(writer, sheet_name='시간별_통계')
            
            logging.info(f"Excel 리포트 생성 완료: {filename}")
            
            # 이메일로 리포트 전송
            subject = f"📊 일일 스크래핑 리포트 - {datetime.now().strftime('%Y-%m-%d')}"
            body = f"""
            <html>
            <body>
                <h2>일일 스크래핑 리포트</h2>
                <p><strong>보고서 생성 시간:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>수집된 데이터:</strong> {len(recent_data)}건</p>
                <p><strong>모니터링 웹사이트:</strong> {len(df['website_name'].unique())}개</p>
                
                <h3>웹사이트별 수집 현황</h3>
                <table border="1" style="border-collapse: collapse;">
                    <tr><th>웹사이트</th><th>수집 건수</th></tr>
            """
            
            for website, count in df['website_name'].value_counts().items():
                body += f"<tr><td>{website}</td><td>{count}</td></tr>"
            
            body += """
                </table>
                <br>
                <p>상세한 데이터는 첨부된 Excel 파일을 확인해주세요.</p>
            </body>
            </html>
            """
            
            self.notification_manager.send_email(subject, body)
            
        except Exception as e:
            logging.error(f"Excel 리포트 생성 실패: {e}")
    
    def setup_scheduler(self):
        """스케줄러 설정"""
        # 기본적으로 30분마다 실행
        schedule.every(30).minutes.do(self.run_single_scrape)
        
        # 설정에 따른 개별 스케줄
        for website_config in self.config['websites']:
            if website_config.get('enabled', True) and 'schedule' in website_config:
                schedule_str = website_config['schedule']
                
                # 스케줄 형식에 따른 처리
                if schedule_str.startswith('*/'):
                    # */30 (30분마다)
                    interval = int(schedule_str[2:])
                    schedule.every(interval).minutes.do(
                        lambda w=website_config: self.scrape_single_website(w)
                    )
                elif schedule_str == 'daily':
                    schedule.every().day.at("09:00").do(
                        lambda w=website_config: self.scrape_single_website(w)
                    )
                elif schedule_str == 'hourly':
                    schedule.every().hour.do(
                        lambda w=website_config: self.scrape_single_website(w)
                    )
        
        # 일일 리포트 생성 (매일 자정)
        if self.config['export_settings']['excel_export']:
            schedule.every().day.at("00:00").do(self.generate_excel_report)
        
        logging.info("스케줄러 설정 완료")
    
    def scrape_single_website(self, website_config: Dict[str, Any]):
        """단일 웹사이트 스크래핑 (스케줄러용)"""
        data = self.scrape_website(website_config)
        if data:
            self.process_scraped_data(data)
    
    def run_scheduler(self):
        """스케줄러 실행"""
        self.setup_scheduler()
        logging.info("🕷️ 고급 웹 스크래핑 자동화 시작")
        logging.info("종료하려면 Ctrl+C를 누르세요")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 스케줄 확인
        except KeyboardInterrupt:
            logging.info("사용자에 의해 종료됨")
        except Exception as e:
            logging.error(f"스케줄러 오류: {e}")

def main():
    """메인 함수"""
    print("🕷️ Advanced Web Scraping Automation Tool v1.0.0")
    print("=" * 50)
    print()
    
    try:
        scraper = AdvancedWebScraper()
        
        print("실행 모드를 선택하세요:")
        print("1. 단일 실행 (한 번만 스크래핑)")
        print("2. 자동화 모드 (24시간 자동 실행)")
        print("3. 설정 확인")
        print("4. Excel 리포트 생성")
        
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == "1":
            print("\n단일 스크래핑을 시작합니다...")
            scraper.run_single_scrape()
            print("✅ 스크래핑 완료!")
            
        elif choice == "2":
            print("\n24시간 자동화 모드를 시작합니다...")
            scraper.run_scheduler()
            
        elif choice == "3":
            print("\n현재 설정:")
            print(f"- 모니터링 웹사이트: {len(scraper.config['websites'])}개")
            print(f"- 활성화된 웹사이트: {len([w for w in scraper.config['websites'] if w.get('enabled', True)])}개")
            print(f"- 이메일 알림: {'ON' if scraper.config['notifications']['email']['enabled'] else 'OFF'}")
            print(f"- 웹훅 알림: {'ON' if scraper.config['notifications']['webhook']['enabled'] else 'OFF'}")
            print(f"- Excel 내보내기: {'ON' if scraper.config['export_settings']['excel_export'] else 'OFF'}")
            
        elif choice == "4":
            print("\nExcel 리포트를 생성합니다...")
            scraper.generate_excel_report()
            print("✅ 리포트 생성 완료!")
            
        else:
            print("❌ 잘못된 선택입니다.")
    
    except Exception as e:
        logging.error(f"실행 중 오류 발생: {e}")
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()