#!/usr/bin/env python3
"""
TAQWIN COMPETITOR INTELLIGENCE SCANNER
Live Raw Data Collection for Organic Skincare Market
"""

from taqwin_web_intelligence import TAQWINWebIntelligence
import json
import time
from datetime import datetime

def scan_competitors_raw_data():
    """Scan competitors for raw intelligence data"""
    
    # Initialize TAQWIN Web Intelligence
    taqwin = TAQWINWebIntelligence()
    
    # Complete competitor list for organic skincare market
    competitors = [
        'Mamaearth',
        'Khadi Natural', 
        'Biotique',
        'Himalaya Herbals',
        'Forest Essentials',
        'Kama Ayurveda',
        'Plum Goodness',
        'The Body Shop India',
        'Lotus Herbals',
        'Jovees',
        'WOW Skin Science',
        'Mcaffeine',
        'Nykaa Naturals',
        'Organic Harvest'
    ]
    
    print('🕵️ TAQWIN COMPETITIVE INTELLIGENCE SCAN INITIATED')
    print('=' * 60)
    
    intelligence_reports = {
        'scan_timestamp': datetime.now().isoformat(),
        'total_competitors': len(competitors),
        'market_focus': 'Organic Skincare India',
        'intelligence_data': {}
    }
    
    for i, competitor in enumerate(competitors[:8], 1):  # First 8 competitors
        print(f'\n🎯 [{i}/8] SCANNING: {competitor}')
        print('-' * 40)
        
        # Strategic intelligence queries
        queries = [
            f'{competitor} organic skincare products customer feedback',
            f'{competitor} pricing strategy multani mitti face pack',
            f'{competitor} social media complaints organic products',
            f'{competitor} market share organic skincare India 2025'
        ]
        
        competitor_data = {
            'name': competitor,
            'scan_time': datetime.now().isoformat(),
            'raw_intelligence': [],
            'strategic_summary': {
                'total_searches': len(queries),
                'successful_searches': 0,
                'intelligence_value': 'CALCULATING'
            }
        }
        
        for query_idx, query in enumerate(queries, 1):
            print(f'  🔍 Search {query_idx}: {query[:50]}...')
            
            try:
                result = taqwin.search_web(query)
                if result and result.get('status') == 'SUCCESS':
                    competitor_data['raw_intelligence'].append({
                        'query': query,
                        'timestamp': result.get('timestamp'),
                        'abstract': result.get('abstract', ''),
                        'abstract_source': result.get('abstract_source', ''),
                        'abstract_url': result.get('abstract_url', ''),
                        'related_topics': result.get('related_topics', []),
                        'strategic_classification': 'HIGH' if any(keyword in query.lower() for keyword in ['customer', 'pricing', 'complaints']) else 'MEDIUM',
                        'intelligence_type': 'COMPETITIVE_ANALYSIS'
                    })
                    competitor_data['strategic_summary']['successful_searches'] += 1
                    print(f'    ✅ SUCCESS: Data extracted')
                else:
                    print(f'    ⚠️ LIMITED: No significant data')
                    
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f'    ❌ ERROR: {str(e)}')
        
        # Calculate intelligence value
        success_rate = competitor_data['strategic_summary']['successful_searches'] / len(queries)
        if success_rate >= 0.75:
            competitor_data['strategic_summary']['intelligence_value'] = 'HIGH'
        elif success_rate >= 0.5:
            competitor_data['strategic_summary']['intelligence_value'] = 'MEDIUM'
        else:
            competitor_data['strategic_summary']['intelligence_value'] = 'LOW'
        
        intelligence_reports['intelligence_data'][competitor] = competitor_data
        print(f'✅ {competitor}: {competitor_data["strategic_summary"]["successful_searches"]}/{len(queries)} searches successful')
    
    # Save raw intelligence data
    filename = f'taqwin_competitor_raw_intelligence_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(intelligence_reports, f, indent=2, ensure_ascii=False)
    
    print(f'\n🌟 COMPETITIVE INTELLIGENCE SCAN COMPLETE')
    print(f'📊 Raw intelligence data saved to: {filename}')
    
    # Display summary
    total_searches = sum(len(data['raw_intelligence']) for data in intelligence_reports['intelligence_data'].values())
    print(f'📈 INTELLIGENCE SUMMARY:')
    print(f'   Competitors Scanned: {len(intelligence_reports["intelligence_data"])}')
    print(f'   Total Raw Intelligence Gathered: {total_searches}')
    print(f'   Market Coverage: Organic Skincare India')
    
    return intelligence_reports

if __name__ == "__main__":
    scan_competitors_raw_data()
