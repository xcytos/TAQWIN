#!/usr/bin/env python3
"""
TAQWIN WEB CONNECTOR - INTERNET ACCESS FRAMEWORK
Implementation Date: 2025-07-24T22:55:32Z
Created by: TGINI Project Team (Tim Berners-Lee + Vint Cerf)

This module provides TAQWIN with secure internet connectivity and web request capabilities.
"""

import requests
import json
import time
from datetime import datetime
import sqlite3
import logging
from urllib.parse import urljoin, urlparse
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - TAQWIN WebConnector - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('D:/Ethereal Glow/taqwin_web_access.log'),
        logging.StreamHandler()
    ]
)

class TAQWINWebConnector:
    """
    TAQWIN Internet Access Framework
    Provides secure, rate-limited web connectivity for strategic intelligence gathering
    """
    
    def __init__(self):
        self.session = requests.Session()
        
        # Sophisticated User Agent rotation for web anonymity
        self.user_agents = [
            'TAQWIN-AI-Brain/1.0 (Business Intelligence System)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Rate limiting to be respectful to web servers
        self.rate_limiter = {}
        self.default_delay = 1  # 1 second between requests
        
        # Connection status tracking
        self.connection_active = False
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        logging.info("[GLOBAL] TAQWIN Web Connector Initialized")
        logging.info("[SECURE] Secure request protocols activated")
        logging.info("[POWER] Rate limiting system operational")
        
    def test_internet_connection(self):
        """Test basic internet connectivity"""
        test_urls = [
            'https://httpbin.org/status/200',
            'https://www.google.com',
            'https://duckduckgo.com'
        ]
        
        for url in test_urls:
            try:
                response = self.secure_request(url, timeout=10)
                if response and response.status_code == 200:
                    self.connection_active = True
                    logging.info(f"[CHECK] Internet connectivity confirmed via {url}")
                    return True
            except Exception as e:
                logging.warning(f"⚠️ Connection test failed for {url}: {e}")
                continue
                
        self.connection_active = False
        logging.error("❌ Internet connectivity test failed")
        return False
        
    def secure_request(self, url, params=None, timeout=30, method='GET', data=None):
        """Make secure web request with comprehensive error handling"""
        try:
            # Rate limiting
            domain = urlparse(url).netloc
            current_time = time.time()
            
            if domain in self.rate_limiter:
                time_since_last = current_time - self.rate_limiter[domain]
                if time_since_last < self.default_delay:
                    sleep_time = self.default_delay - time_since_last
                    time.sleep(sleep_time)
            
            self.rate_limiter[domain] = current_time
            
            # Rotate User Agent for each request
            self.session.headers.update({
                'User-Agent': random.choice(self.user_agents)
            })
            
            # Make request based on method
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=data, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Update statistics
            self.total_requests += 1
            
            if response.status_code == 200:
                self.successful_requests += 1
                logging.info(f"[SUCCESS] Successful request to {domain}")
                return response
            else:
                self.failed_requests += 1
                logging.warning(f"[WARNING] Request returned status {response.status_code} for {url}")
                return response
                
        except requests.exceptions.Timeout:
            self.failed_requests += 1
            logging.error(f"⏰ Request timeout for {url}")
            return None
        except requests.exceptions.ConnectionError:
            self.failed_requests += 1
            logging.error(f"🔌 Connection error for {url}")
            return None
        except Exception as e:
            self.failed_requests += 1
            logging.error(f"❌ Request failed for {url}: {e}")
            return None
    
    def get_connection_stats(self):
        """Get connection performance statistics"""
        success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        
        stats = {
            'connection_active': self.connection_active,
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': round(success_rate, 2),
            'domains_accessed': len(self.rate_limiter)
        }
        
        return stats
    
    def safe_download(self, url, max_size_mb=10):
        """Safely download content with size limits"""
        try:
            response = self.secure_request(url, timeout=30)
            if not response:
                return None
                
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                if size_mb > max_size_mb:
                    logging.warning(f"⚠️ Content too large ({size_mb:.2f}MB) for {url}")
                    return None
            
            return response.content
            
        except Exception as e:
            logging.error(f"❌ Download failed for {url}: {e}")
            return None

def test_web_connector():
    """Test function to verify web connector functionality"""
    print("🧪 Testing TAQWIN Web Connector...")
    
    connector = TAQWINWebConnector()
    
    # Test internet connectivity
    print("🔌 Testing internet connection...")
    if connector.test_internet_connection():
        print("✅ Internet connection: ACTIVE")
    else:
        print("❌ Internet connection: FAILED")
        return False
    
    # Test basic web request
    print("🌐 Testing web request...")
    response = connector.secure_request('https://httpbin.org/json')
    if response and response.status_code == 200:
        print("✅ Web request: SUCCESS")
        try:
            data = response.json()
            print(f"📊 Sample response data: {data}")
        except:
            print("📊 Response received (non-JSON)")
    else:
        print("❌ Web request: FAILED")
    
    # Display connection statistics
    stats = connector.get_connection_stats()
    print("\n📊 Connection Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    return True

if __name__ == "__main__":
    print("🚀 TAQWIN Web Connector - Direct Test Mode")
    test_web_connector()
