#!/usr/bin/env python3
"""
TAQWIN SEARCH ENGINE - MULTI-SOURCE WEB SEARCH INTELLIGENCE
Implementation Date: 2025-07-24T22:55:32Z
Created by: TGINI Project Team (Larry Page + Sergey Brin)

This module provides TAQWIN with intelligent web search capabilities across multiple engines.
"""

import json
import time
from datetime import datetime
import logging
from urllib.parse import quote_plus, urljoin
import re
from taqwin_web_connector import TAQWINWebConnector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - TAQWIN SearchEngine - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('D:/Ethereal Glow/taqwin_search.log'),
        logging.StreamHandler()
    ]
)

class TAQWINSearchEngine:
    """
    TAQWIN Multi-Source Search Intelligence Engine
    Aggregates and ranks results from multiple search engines for strategic intelligence
    """
    
    def __init__(self):
        self.web_connector = TAQWINWebConnector()
        
        # Search engine endpoints (free APIs)
        self.search_engines = {
            'duckduckgo_instant': 'https://api.duckduckgo.com/',
            'wikipedia': 'https://en.wikipedia.org/api/rest_v1/page/summary/',
            'arxiv': 'http://export.arxiv.org/api/query'
        }
        
        # Search statistics
        self.total_searches = 0
        self.successful_searches = 0
        self.results_found = 0
        
        logging.info("TAQWIN Search Engine Initialized")
        logging.info("Multi-source search protocols activated")
        
    def multi_source_search(self, query, max_results=10):
        """Search across multiple engines and aggregate results"""
        self.total_searches += 1
        all_results = []
        
        try:
            # DuckDuckGo Instant Answer API (Free)
            ddg_results = self.search_duckduckgo_instant(query, max_results)
            if ddg_results:
                all_results.extend(ddg_results)
            
            # Wikipedia Search (Free)
            wiki_results = self.search_wikipedia(query, max_results)
            if wiki_results:
                all_results.extend(wiki_results)
            
            # arXiv Academic Papers (Free)
            arxiv_results = self.search_arxiv(query, max_results // 2)
            if arxiv_results:
                all_results.extend(arxiv_results)
            
            # Deduplicate and rank results
            unique_results = self.deduplicate_and_rank(all_results)
            
            if unique_results:
                self.successful_searches += 1
                self.results_found += len(unique_results)
                logging.info(f"Search completed: {len(unique_results)} results for '{query}'")
            
            return unique_results[:max_results]
            
        except Exception as e:
            logging.error(f"Multi-source search failed for '{query}': {e}")
            return []
    
    def search_duckduckgo_instant(self, query, max_results=5):
        """Search using DuckDuckGo Instant Answer API (Free)"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.web_connector.secure_request(url, params=params)
            if not response or response.status_code != 200:
                return []
            
            data = response.json()
            results = []
            
            # Process Instant Answer
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', 'DuckDuckGo Result'),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', ''),
                    'source': 'DuckDuckGo',
                    'relevance_score': 0.9
                })
            
            # Process Related Topics
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('Text', '')[:100] + '...',
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo Related',
                        'relevance_score': 0.7
                    })
            
            logging.info(f"DuckDuckGo search: {len(results)} results")
            return results
            
        except Exception as e:
            logging.error(f"DuckDuckGo search failed: {e}")
            return []
    
    def search_wikipedia(self, query, max_results=3):
        """Search Wikipedia for relevant articles"""
        try:
            # First, search for the page
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
            
            response = self.web_connector.secure_request(search_url)
            if not response or response.status_code != 200:
                return []
            
            data = response.json()
            
            if data.get('type') == 'standard':
                result = {
                    'title': data.get('title', ''),
                    'snippet': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'source': 'Wikipedia',
                    'relevance_score': 0.8
                }
                
                logging.info(f"Wikipedia search: 1 result")
                return [result]
            
            return []
            
        except Exception as e:
            logging.error(f"Wikipedia search failed: {e}")
            return []
    
    def search_arxiv(self, query, max_results=2):
        """Search arXiv for academic papers"""
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results
            }
            
            response = self.web_connector.secure_request(url, params=params)
            if not response or response.status_code != 200:
                return []
            
            # Parse XML response (simplified parsing)
            content = response.text
            results = []
            
            # Extract entries (basic regex parsing)
            entries = re.findall(r'<entry>.*?</entry>', content, re.DOTALL)
            
            for entry in entries[:max_results]:
                title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                link_match = re.search(r'<id>(.*?)</id>', entry)
                
                if title_match and summary_match:
                    results.append({
                        'title': title_match.group(1).strip(),
                        'snippet': summary_match.group(1).strip()[:300] + '...',
                        'url': link_match.group(1).strip() if link_match else '',
                        'source': 'arXiv',
                        'relevance_score': 0.85
                    })
            
            logging.info(f"arXiv search: {len(results)} results")
            return results
            
        except Exception as e:
            logging.error(f"arXiv search failed: {e}")
            return []
    
    def deduplicate_and_rank(self, results):
        """Remove duplicates and rank results by relevance"""
        try:
            # Remove duplicates based on URL and title similarity
            unique_results = []
            seen_urls = set()
            seen_titles = set()
            
            for result in results:
                url = result.get('url', '').lower()
                title = result.get('title', '').lower()
                
                # Skip if we've seen this URL or very similar title
                if url and url in seen_urls:
                    continue
                if title and any(self.similarity(title, seen_title) > 0.8 for seen_title in seen_titles):
                    continue
                
                seen_urls.add(url)
                seen_titles.add(title)
                unique_results.append(result)
            
            # Sort by relevance score (descending)
            unique_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            return unique_results
            
        except Exception as e:
            logging.error(f"Deduplication failed: {e}")
            return results
    
    def similarity(self, text1, text2):
        """Calculate simple text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if len(words1) == 0 and len(words2) == 0:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def strategic_search(self, query, business_context=""):
        """Enhanced search with business intelligence focus"""
        try:
            # Enhance query with business context
            enhanced_query = f"{query} {business_context}".strip()
            
            # Perform multi-source search
            results = self.multi_source_search(enhanced_query)
            
            # Add strategic intelligence metadata
            for result in results:
                result['search_timestamp'] = datetime.now().isoformat()
                result['business_context'] = business_context
                result['strategic_relevance'] = self.assess_strategic_relevance(result, query)
            
            return results
            
        except Exception as e:
            logging.error(f"Strategic search failed: {e}")
            return []
    
    def assess_strategic_relevance(self, result, original_query):
        """Assess strategic business relevance of search result"""
        try:
            strategic_keywords = [
                'market', 'business', 'strategy', 'competition', 'revenue',
                'growth', 'customer', 'industry', 'trend', 'opportunity',
                'analysis', 'research', 'innovation', 'technology'
            ]
            
            text_content = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
            
            # Count strategic keyword matches
            strategic_score = sum(1 for keyword in strategic_keywords if keyword in text_content)
            
            # Normalize score (0-1)
            max_possible_score = len(strategic_keywords)
            normalized_score = min(strategic_score / max_possible_score, 1.0)
            
            return round(normalized_score, 2)
            
        except Exception as e:
            logging.error(f"Strategic relevance assessment failed: {e}")
            return 0.5
    
    def get_search_stats(self):
        """Get search engine performance statistics"""
        success_rate = (self.successful_searches / self.total_searches * 100) if self.total_searches > 0 else 0
        avg_results = (self.results_found / self.successful_searches) if self.successful_searches > 0 else 0
        
        return {
            'total_searches': self.total_searches,
            'successful_searches': self.successful_searches,
            'success_rate': round(success_rate, 2),
            'total_results_found': self.results_found,
            'average_results_per_search': round(avg_results, 1)
        }

def test_search_engine():
    """Test function to verify search engine functionality"""
    print("Testing TAQWIN Search Engine...")
    
    search_engine = TAQWINSearchEngine()
    
    # Test basic search
    print("Testing basic search functionality...")
    results = search_engine.multi_source_search("artificial intelligence", max_results=5)
    
    if results:
        print(f"Search successful: {len(results)} results found")
        print("Sample results:")
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. {result.get('title', 'No title')}")
            print(f"     Source: {result.get('source', 'Unknown')}")
            print(f"     URL: {result.get('url', 'No URL')}")
            print()
    else:
        print("Search failed: No results found")
    
    # Test strategic search
    print("Testing strategic search...")
    strategic_results = search_engine.strategic_search("skincare market trends", "business intelligence")
    
    if strategic_results:
        print(f"Strategic search successful: {len(strategic_results)} results")
        for result in strategic_results[:2]:
            print(f"  Strategic relevance: {result.get('strategic_relevance', 0)}")
    
    # Display statistics
    stats = search_engine.get_search_stats()
    print("\nSearch Engine Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return len(results) > 0

if __name__ == "__main__":
    print("TAQWIN Search Engine - Direct Test Mode")
    test_search_engine()
