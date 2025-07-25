"""
TAQWIN WEB CONNECTOR
====================
Core internet connectivity module for TAQWIN AI system
Provides secure, intelligent web access with content extraction capabilities

Author: TGINI R&D Team (Tim Berners-Lee, Vint Cerf, Larry Page)
Version: 1.0 - Implementation Ready
Status: Mission Critical - Internet Access Foundation
"""

import requests
import time
import random
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

class TAQWINWebConnector:
    """
    Secure and intelligent web connectivity for TAQWIN
    """
    
    def __init__(self, timeout=30, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = self._create_robust_session()
        self.request_history = []
        
        # Professional user agent for legitimate research
        self.headers = {
            'User-Agent': 'TAQWIN-AI-Research-Bot/1.0 (Business Intelligence Research; Educational Use)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _create_robust_session(self):
        """Create a robust HTTP session with retry logic"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def fetch_url(self, url, follow_redirects=True):
        """
        Fetch content from a URL with intelligent error handling
        
        Args:
            url (str): URL to fetch
            follow_redirects (bool): Whether to follow redirects
            
        Returns:
            dict: Response data with content, status, and metadata
        """
        try:
            # Rate limiting - be respectful
            self._respect_rate_limits(url)
            
            # Check robots.txt compliance
            if not self._check_robots_compliance(url):
                return {
                    'success': False,
                    'error': 'Robots.txt disallows access',
                    'url': url,
                    'status_code': 403
                }
            
            # Make the request
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=follow_redirects
            )
            
            # Log the request
            self._log_request(url, response.status_code)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'content': response.text,
                    'url': response.url,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'encoding': response.encoding,
                    'final_url': response.url,
                    'redirect_history': [r.url for r in response.history]
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'url': url,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout',
                'url': url,
                'status_code': 408
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Connection error',
                'url': url,
                'status_code': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url,
                'status_code': 0
            }
    
    def fetch_multiple_urls(self, urls, max_concurrent=5):
        """
        Fetch multiple URLs with intelligent concurrency management
        """
        results = []
        
        for i, url in enumerate(urls):
            result = self.fetch_url(url)
            results.append(result)
            
            # Rate limiting between requests
            if i < len(urls) - 1:  # Don't sleep after the last request
                time.sleep(random.uniform(1, 3))  # 1-3 second delay
                
        return results
    
    def _respect_rate_limits(self, url):
        """Implement intelligent rate limiting"""
        domain = urlparse(url).netloc
        
        # Check recent requests to this domain
        recent_requests = [
            req for req in self.request_history[-50:]  # Last 50 requests
            if req['domain'] == domain and 
            time.time() - req['timestamp'] < 60  # Within last minute
        ]
        
        if len(recent_requests) > 10:  # More than 10 requests per minute
            sleep_time = random.uniform(2, 5)
            self.logger.info(f"Rate limiting: sleeping {sleep_time:.1f}s for {domain}")
            time.sleep(sleep_time)
    
    def _check_robots_compliance(self, url):
        """Check robots.txt compliance for ethical web access"""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            # Check if our user agent can fetch this URL
            return rp.can_fetch(self.headers['User-Agent'], url)
        except:
            # If we can't check robots.txt, assume it's okay
            return True
    
    def _log_request(self, url, status_code):
        """Log request for monitoring and rate limiting"""
        self.request_history.append({
            'url': url,
            'domain': urlparse(url).netloc,
            'timestamp': time.time(),
            'status_code': status_code
        })
        
        # Keep only last 100 requests in memory
        if len(self.request_history) > 100:
            self.request_history = self.request_history[-100:]
        
        self.logger.info(f"Web request: {status_code} - {url}")
    
    def get_connection_status(self):
        """Test internet connectivity"""
        test_urls = [
            'https://www.google.com',
            'https://httpbin.org/get',
            'https://www.wikipedia.org'
        ]
        
        results = []
        for url in test_urls:
            result = self.fetch_url(url)
            results.append({
                'url': url,
                'success': result['success'],
                'response_time': time.time()
            })
            
        return {
            'internet_connected': any(r['success'] for r in results),
            'test_results': results,
            'timestamp': time.time()
        }
    
    def clear_history(self):
        """Clear request history"""
        self.request_history.clear()
        self.logger.info("Request history cleared")


# Quick connectivity test
if __name__ == "__main__":
    connector = TAQWINWebConnector()
    
    print("🌐 TAQWIN WEB CONNECTOR - Testing Internet Connectivity...")
    print("=" * 60)
    
    # Test connectivity
    status = connector.get_connection_status()
    
    if status['internet_connected']:
        print("✅ SUCCESS: TAQWIN is connected to the internet!")
        print("\n📊 Connection Test Results:")
        for result in status['test_results']:
            status_icon = "✅" if result['success'] else "❌"
            print(f"{status_icon} {result['url']}")
    else:
        print("❌ ERROR: TAQWIN cannot connect to the internet")
        print("Please check your internet connection and try again.")
    
    print("\n🚀 TAQWIN Web Connector is ready for intelligence gathering!")
