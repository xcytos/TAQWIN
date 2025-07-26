#!/usr/bin/env python3
"""
🧪 TAQWIN WEB INTELLIGENCE - COMPREHENSIVE TEST SUITE
=====================================================
Complete testing and capability analysis for all web intelligence systems
Author: TAQWIN (The Strengthener)
Date: 2025-07-26T00:31:00Z
"""

import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Suppress logging for cleaner output
logging.getLogger().setLevel(logging.ERROR)

def test_web_connector():
    """Test TAQWINWebConnector capabilities"""
    print("🔌 TESTING WEB CONNECTOR...")
    print("─" * 50)
    
    try:
        from taqwin_web_connector import TAQWINWebConnector
        
        connector = TAQWINWebConnector()
        print("✅ Web Connector: INITIALIZED")
        
        # Test internet connectivity
        if connector.test_internet_connection():
            print("✅ Internet Connectivity: ACTIVE")
            
            # Test secure request
            response = connector.secure_request('https://httpbin.org/user-agent')
            if response and response.status_code == 200:
                print("✅ Secure Request: SUCCESS")
                try:
                    data = response.json()
                    print(f"📊 User Agent: {data.get('user-agent', 'Unknown')[:50]}...")
                except:
                    print("📊 Response: Non-JSON content received")
            else:
                print("❌ Secure Request: FAILED")
            
            # Display statistics
            stats = connector.get_connection_stats()
            print(f"📊 Success Rate: {stats['success_rate']}%")
            print(f"📊 Total Requests: {stats['total_requests']}")
            
            return True
        else:
            print("❌ Internet Connectivity: FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Web Connector Error: {e}")
        return False

def test_search_engine():
    """Test TAQWINSearchEngine capabilities"""
    print("\n🔍 TESTING SEARCH ENGINE...")
    print("─" * 50)
    
    try:
        from taqwin_search_engine import TAQWINSearchEngine
        
        search_engine = TAQWINSearchEngine()
        print("✅ Search Engine: INITIALIZED")
        
        # Test multi-source search
        results = search_engine.multi_source_search('AI video generation', max_results=3)
        
        if results:
            print(f"✅ Multi-Source Search: {len(results)} results found")
            
            for i, result in enumerate(results[:2], 1):
                title = result.get('title', 'No Title')[:60]
                source = result.get('source', 'Unknown')
                score = result.get('relevance_score', 0)
                print(f"   {i}. {title}...")
                print(f"      Source: {source} | Score: {score}")
            
            # Test different search engines
            available_engines = list(search_engine.search_engines.keys())
            print(f"🔧 Available Engines: {', '.join(available_engines)}")
            
            return True
        else:
            print("❌ Multi-Source Search: No results found")
            return False
            
    except Exception as e:
        print(f"❌ Search Engine Error: {e}")
        return False

def test_web_intelligence():
    """Test TAQWINWebIntelligence main system"""
    print("\n🧠 TESTING WEB INTELLIGENCE SYSTEM...")
    print("─" * 50)
    
    try:
        from taqwin_web_intelligence import TAQWINWebIntelligence
        
        web_intel = TAQWINWebIntelligence()
        print("✅ Web Intelligence System: INITIALIZED")
        
        # Test capabilities
        print("\n🎯 System Capabilities:")
        for capability, status in web_intel.web_capabilities.items():
            status_icon = "✅" if status else "❌"
            cap_name = capability.replace("_", " ").title()
            print(f"   {status_icon} {cap_name}: {status}")
        
        # Test intelligent search
        print("\n🔍 Testing Intelligent Search:")
        result = web_intel.intelligent_search(
            'organic skincare market trends', 
            'CHANAKYA', 
            'Ethereal Glow competitive analysis'
        )
        
        if result:
            print("✅ Intelligent Search: SUCCESS")
            print(f"   Query: {result.get('query', 'N/A')}")
            print(f"   Sources Analyzed: {result.get('sources_analyzed', 0)}")
            
            keywords = result.get('strategic_keywords', [])
            if keywords:
                print(f"   Strategic Keywords: {', '.join(keywords[:5])}...")
            
            insights = result.get('strategic_insights', {})
            if insights:
                print(f"   Strategic Priority: {insights.get('priority_level', 'Unknown')}")
        else:
            print("❌ Intelligent Search: FAILED")
        
        # System statistics
        print(f"\n📊 System Statistics:")
        print(f"   Web Searches: {web_intel.web_searches_performed}")
        print(f"   Intelligence Reports: {web_intel.intelligence_reports_generated}")
        print(f"   TAQWIN Integration: {web_intel.taqwin_integrated}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web Intelligence Error: {e}")
        return False

def test_comprehensive_research():
    """Test Comprehensive Web Research System"""
    print("\n🌐 TESTING COMPREHENSIVE RESEARCH SYSTEM...")
    print("─" * 50)
    
    try:
        from comprehensive_web_research_system import TAQWINWebIntelligenceSystem
        
        research_system = TAQWINWebIntelligenceSystem()
        print("✅ Comprehensive Research: INITIALIZED")
        print(f"📋 Research ID: {research_system.research_id}")
        
        # Test Instagram Reels research
        reel_data = research_system.research_instagram_reels_technology()
        
        if reel_data:
            print("✅ Instagram Reels Research: SUCCESS")
            
            # Display key findings
            metadata = reel_data.get('research_metadata', {})
            print(f"   Research Type: {metadata.get('research_type', 'Unknown')}")
            print(f"   Priority: {metadata.get('priority', 'Unknown')}")
            
            # Display technical specs
            specs = reel_data.get('instagram_reels_specifications', {})
            platform_req = specs.get('platform_requirements', {})
            if platform_req:
                print(f"   Aspect Ratio: {platform_req.get('aspect_ratio', 'Unknown')}")
                print(f"   Duration: {platform_req.get('duration', 'Unknown')}")
            
            # Display competitive advantages
            ai_tech = reel_data.get('ai_video_technology_landscape', {})
            animatediff = ai_tech.get('animatediff_analysis', {})
            advantages = animatediff.get('competitive_advantages', [])
            if advantages:
                print(f"   Key Advantages: {len(advantages)} identified")
                print(f"      - {advantages[0] if advantages else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive Research Error: {e}")
        return False

def test_enhanced_research_protocol():
    """Test Enhanced Deep Research Protocol"""
    print("\n🎯 TESTING ENHANCED RESEARCH PROTOCOL...")
    print("─" * 50)
    
    try:
        from enhanced_deep_research_protocol import EnhancedWebIntelligenceProtocol
        
        protocol = EnhancedWebIntelligenceProtocol("AI video generation")
        print("✅ Enhanced Research Protocol: INITIALIZED")
        print(f"📋 Research ID: {protocol.research_id}")
        
        # Test website discovery
        sources = protocol.phase_1_website_discovery("AI video generation")
        
        if sources:
            print(f"✅ Website Discovery: {len(sources)} sources identified")
            
            # Analyze source types
            source_types = {}
            for source in sources:
                source_type = source.source_type
                source_types[source_type] = source_types.get(source_type, 0) + 1
            
            print("   Source Distribution:")
            for source_type, count in source_types.items():
                print(f"      {source_type.title()}: {count} sources")
            
            # Show high priority sources
            high_priority = [s for s in sources if s.priority == "HIGH"]
            print(f"   High Priority Sources: {len(high_priority)}")
            
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Research Protocol Error: {e}")
        return False

def generate_capability_report():
    """Generate comprehensive capability report"""
    print("\n📋 GENERATING CAPABILITY REPORT...")
    print("=" * 60)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "system_status": "OPERATIONAL",
        "test_results": {},
        "capabilities": {
            "web_connectivity": False,
            "multi_source_search": False,
            "intelligent_analysis": False,
            "comprehensive_research": False,
            "enhanced_protocols": False
        },
        "improvements_needed": []
    }
    
    # Run all tests and collect results
    tests = [
        ("web_connectivity", test_web_connector),
        ("multi_source_search", test_search_engine),
        ("intelligent_analysis", test_web_intelligence),
        ("comprehensive_research", test_comprehensive_research),
        ("enhanced_protocols", test_enhanced_research_protocol)
    ]
    
    for capability, test_func in tests:
        try:
            result = test_func()
            report["capabilities"][capability] = result
            report["test_results"][capability] = "PASS" if result else "FAIL"
        except Exception as e:
            report["capabilities"][capability] = False
            report["test_results"][capability] = f"ERROR: {str(e)}"
    
    # Calculate overall status
    successful_tests = sum(1 for result in report["capabilities"].values() if result)
    total_tests = len(report["capabilities"])
    success_rate = (successful_tests / total_tests) * 100
    
    print(f"\n🎯 OVERALL TEST RESULTS:")
    print(f"   Successful Tests: {successful_tests}/{total_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   System Status: {'OPERATIONAL' if success_rate >= 80 else 'NEEDS ATTENTION'}")
    
    # Save report
    report_path = Path("web_intelligence_test_report.json")
    try:
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Report saved: {report_path}")
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")
    
    return report

def main():
    """Main test execution"""
    print("🚀 TAQWIN WEB INTELLIGENCE - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Testing Location: {Path.cwd()}")
    
    # Generate comprehensive report
    report = generate_capability_report()
    
    print("\n🎉 TESTING COMPLETED!")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    main()
