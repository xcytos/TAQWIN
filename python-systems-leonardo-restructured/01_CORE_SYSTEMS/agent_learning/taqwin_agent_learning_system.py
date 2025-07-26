#!/usr/bin/env python3
"""
TAQWIN INDIVIDUAL AGENT LEARNING & CONVERSATION STORAGE SYSTEM
Created by: Johannes Gutenberg (Documentation Revolution Master)
Date: 2025-07-24T21:02:12Z

This system ensures every TAQWIN legendary agent stores their own conversations,
debates, and interactions to continuously learn and improve their capabilities
through data-driven intelligence enhancement.
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import hashlib
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - TAQWIN AgentLearning - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('D:/Ethereal Glow/taqwin_agent_learning.log'),
        logging.StreamHandler()
    ]
)

class TaqwinAgentLearningSystem:
    """
    Individual Agent Learning & Conversation Storage System
    Each legendary agent maintains their own learning database and improvement protocols
    """
    
    def __init__(self):
        self.base_path = Path("D:/Ethereal Glow")
        self.agents_path = self.base_path / "ai-agents"
        self.learning_path = self.base_path / "agent-learning"
        self.db_path = self.base_path / "taqwin_agent_learning.db"
        
        # Create learning directory structure
        self.setup_learning_directories()
        self.setup_database()
        
        # Current TAQWIN legendary agents
        self.legendary_agents = {
            "CHANAKYA": "Strategic Intelligence & Political Wisdom",
            "LEONARDO_DA_VINCI": "Innovation & Creative Engineering",
            "SUN_TZU": "Market Strategy & Competitive Intelligence",
            "NIKOLA_TESLA": "Technological Innovation & Vision",
            "STEVE_JOBS": "Product Innovation & Market Disruption",
            "ELON_MUSK": "Future Vision & Market Expansion",
            "ALBERT_EINSTEIN": "Research & Development Strategy",
            "RAY_KURZWEIL": "Future Technology & Predictive Research",
            "WARREN_BUFFETT": "Financial Strategy & Investment",
            "BENJAMIN_FRANKLIN": "Business Development & Networking",
            "CLEOPATRA": "Brand Influence & Market Presence",
            "OPRAH_WINFREY": "Brand Communication & Influence",
            "MAYA_ANGELOU": "Brand Storytelling & Cultural Impact",
            "MARCUS_AURELIUS": "Leadership Philosophy & Ethics",
            "CHARAKA": "Wellness & Holistic Health Science",
            "MARIE_CURIE": "Research & Scientific Excellence",
            "RACHEL_CARSON": "Sustainability & Bio-Innovation",
            "PARACELSUS": "Organic Innovation & Formulation Science",
            "LINUS_PAULING": "Breakthrough Material Science",
            "JOHANNES_GUTENBERG": "Documentation Revolution & Knowledge Architecture"
        }
        
        logging.info("[BRAIN] TAQWIN Agent Learning System Initialized")
        logging.info(f"[STATS] Monitoring {len(self.legendary_agents)} Legendary Agents")
        logging.info("[BOLT] Individual agent learning protocols: ACTIVE")
        
    def setup_learning_directories(self):
        """Create learning directory structure for each agent"""
        try:
            # Create main learning directory
            self.learning_path.mkdir(exist_ok=True)
            
            # Create individual agent learning directories
            agent_dirs = [
                "conversations",      # Individual conversation logs
                "debates",           # Agent-specific debate participation
                "learnings",         # Accumulated knowledge and insights
                "improvements",      # Capability enhancement tracking
                "feedback",          # Performance feedback and adjustments
                "analytics"          # Agent performance analytics
            ]
            
            for agent_name in self.legendary_agents.keys():
                agent_path = self.learning_path / agent_name.lower()
                agent_path.mkdir(exist_ok=True)
                
                for dir_name in agent_dirs:
                    (agent_path / dir_name).mkdir(exist_ok=True)
                    
            logging.info("[CHECK] Agent learning directory structure created")
            
        except Exception as e:
            logging.error(f"[ERROR] Failed to create learning directories: {e}")
    
    def setup_database(self):
        """Setup database for agent learning and conversation tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Agent conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    conversation_type TEXT NOT NULL,
                    participant_count INTEGER,
                    conversation_content TEXT NOT NULL,
                    strategic_impact TEXT,
                    key_insights TEXT,
                    action_items TEXT,
                    performance_score REAL,
                    learning_extraction TEXT
                )
            ''')
            
            # Agent learning insights table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_learnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    learning_type TEXT NOT NULL,
                    learning_content TEXT NOT NULL,
                    source_conversation_id INTEGER,
                    strategic_value TEXT,
                    implementation_status TEXT,
                    improvement_impact TEXT,
                    validation_status TEXT
                )
            ''')
            
            # Agent capability improvements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_improvements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    improvement_type TEXT NOT NULL,
                    previous_capability TEXT,
                    enhanced_capability TEXT,
                    improvement_trigger TEXT,
                    performance_delta REAL,
                    validation_results TEXT,
                    implementation_notes TEXT
                )
            ''')
            
            # Agent performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    metric_type TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    benchmark_comparison REAL,
                    improvement_trend TEXT,
                    strategic_context TEXT,
                    optimization_recommendations TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logging.info("[CHECK] Agent learning database initialized")
            
        except Exception as e:
            logging.error(f"[ERROR] Database setup failed: {e}")
    
    def store_agent_conversation(self, agent_name, conversation_data):
        """
        Store individual agent conversation for learning and improvement
        
        Args:
            agent_name (str): Name of the legendary agent
            conversation_data (dict): Conversation details including:
                - session_id: Unique session identifier
                - conversation_type: Type of interaction (debate, consultation, analysis, etc.)
                - content: Full conversation content
                - participants: Other agents or humans involved
                - strategic_impact: Assessment of strategic value
                - key_insights: Important insights generated
                - action_items: Follow-up actions identified
        """
        try:
            # Validate agent
            if agent_name.upper() not in self.legendary_agents:
                logging.warning(f"Unknown agent: {agent_name}")
                return False
            
            # Generate unique conversation ID
            timestamp = datetime.now()
            conversation_id = self._generate_conversation_id(agent_name, timestamp)
            
            # Extract learning insights from conversation
            learning_insights = self._extract_learning_insights(conversation_data)
            
            # Calculate performance score
            performance_score = self._calculate_performance_score(conversation_data)
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agent_conversations 
                (agent_name, session_id, timestamp, conversation_type, participant_count,
                 conversation_content, strategic_impact, key_insights, action_items,
                 performance_score, learning_extraction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent_name.upper(),
                conversation_data.get('session_id', conversation_id),
                timestamp,
                conversation_data.get('conversation_type', 'strategic_consultation'),
                len(conversation_data.get('participants', [])),
                conversation_data.get('content', ''),
                conversation_data.get('strategic_impact', ''),
                json.dumps(conversation_data.get('key_insights', [])),
                json.dumps(conversation_data.get('action_items', [])),
                performance_score,
                json.dumps(learning_insights)
            ))
            
            conversation_db_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Store learning insights separately
            self._store_learning_insights(agent_name, learning_insights, conversation_db_id)
            
            # Create individual conversation file
            self._create_conversation_file(agent_name, conversation_id, conversation_data, timestamp)
            
            # Trigger agent improvement analysis
            self._analyze_improvement_opportunities(agent_name, conversation_data, performance_score)
            
            logging.info(f"[BOOK] Conversation stored for {agent_name}: {conversation_id}")
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "performance_score": performance_score,
                "learning_insights_count": len(learning_insights)
            }
            
        except Exception as e:
            logging.error(f"[ERROR] Failed to store conversation for {agent_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def _extract_learning_insights(self, conversation_data):
        """Extract learning insights from conversation data"""
        insights = []
        
        content = conversation_data.get('content', '')
        
        # Pattern-based insight extraction
        insight_patterns = [
            (r'learned that (.+?)(?:\.|$)', 'factual_learning'),
            (r'discovered (.+?)(?:\.|$)', 'discovery'),
            (r'realized (.+?)(?:\.|$)', 'realization'),
            (r'improved (.+?)(?:\.|$)', 'improvement'),
            (r'strategy for (.+?)(?:\.|$)', 'strategic_insight'),
            (r'approach to (.+?)(?:\.|$)', 'methodological_insight'),
            (r'understanding of (.+?)(?:\.|$)', 'conceptual_learning')
        ]
        
        for pattern, insight_type in insight_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 per type
                insights.append({
                    "type": insight_type,
                    "content": match.strip(),
                    "confidence": 0.8,
                    "source": "conversation_analysis"
                })
        
        # Add explicit insights from conversation data
        for insight in conversation_data.get('key_insights', []):
            insights.append({
                "type": "explicit_insight",
                "content": insight,
                "confidence": 0.95,
                "source": "direct_extraction"
            })
        
        return insights
    
    def _calculate_performance_score(self, conversation_data):
        """Calculate performance score for the conversation"""
        score = 0.5  # Base score
        
        # Strategic impact assessment
        if conversation_data.get('strategic_impact'):
            impact_level = conversation_data['strategic_impact'].lower()
            if 'high' in impact_level or 'critical' in impact_level:
                score += 0.3
            elif 'medium' in impact_level:
                score += 0.2
            elif 'low' in impact_level:
                score += 0.1
        
        # Key insights quality
        insights_count = len(conversation_data.get('key_insights', []))
        score += min(insights_count * 0.05, 0.2)
        
        # Action items generation
        actions_count = len(conversation_data.get('action_items', []))
        score += min(actions_count * 0.03, 0.15)
        
        # Content depth (word count as proxy)
        word_count = len(conversation_data.get('content', '').split())
        if word_count > 500:
            score += 0.1
        elif word_count > 200:
            score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _store_learning_insights(self, agent_name, insights, conversation_id):
        """Store learning insights in separate table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for insight in insights:
                cursor.execute('''
                    INSERT INTO agent_learnings
                    (agent_name, timestamp, learning_type, learning_content,
                     source_conversation_id, strategic_value, implementation_status,
                     improvement_impact, validation_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    agent_name.upper(),
                    datetime.now(),
                    insight.get('type', 'general'),
                    insight.get('content', ''),
                    conversation_id,
                    f"Confidence: {insight.get('confidence', 0.5)}",
                    'pending_review',
                    'to_be_measured',
                    'unvalidated'
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"[ERROR] Failed to store learning insights: {e}")
    
    def _create_conversation_file(self, agent_name, conversation_id, conversation_data, timestamp):
        """Create individual conversation file for the agent"""
        try:
            agent_dir = self.learning_path / agent_name.lower() / "conversations"
            # Ensure the directory exists before creating file
            agent_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{conversation_id}_{conversation_data.get('conversation_type', 'consultation')}.md"
            file_path = agent_dir / filename
            
            content = f"""# {agent_name} - Individual Conversation Log
## {conversation_data.get('conversation_type', 'Strategic Consultation').title()}

### 📋 CONVERSATION METADATA
- **Conversation ID**: {conversation_id}
- **Agent**: {agent_name} ({self.legendary_agents[agent_name.upper()]})
- **Timestamp**: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Type**: {conversation_data.get('conversation_type', 'strategic_consultation')}
- **Session ID**: {conversation_data.get('session_id', 'N/A')}
- **Participants**: {', '.join(conversation_data.get('participants', [agent_name]))}

### 🧠 CONVERSATION CONTENT
{conversation_data.get('content', 'Conversation content not provided')}

### 📊 STRATEGIC ANALYSIS
**Strategic Impact**: {conversation_data.get('strategic_impact', 'To be assessed')}

### 💡 KEY INSIGHTS GENERATED
{self._format_insights_list(conversation_data.get('key_insights', []))}

### 🎯 ACTION ITEMS IDENTIFIED
{self._format_action_items(conversation_data.get('action_items', []))}

### 📈 PERFORMANCE METRICS
- **Performance Score**: {self._calculate_performance_score(conversation_data):.2f}/1.00
- **Learning Insights Extracted**: {len(self._extract_learning_insights(conversation_data))}
- **Strategic Value**: {conversation_data.get('strategic_impact', 'To be determined')}

### 🚀 AGENT IMPROVEMENT OPPORTUNITIES
{self._identify_improvement_opportunities(conversation_data)}

### 🔄 LEARNING INTEGRATION STATUS
- **Data Stored**: ✅ Conversation archived in agent learning database
- **Insights Extracted**: ✅ Learning patterns identified and catalogued
- **Improvement Analysis**: ✅ Enhancement opportunities documented
- **Next Review**: {self._calculate_next_review_date(timestamp)}

---

**File Generated**: {timestamp.isoformat()}
**Learning System**: TAQWIN Individual Agent Enhancement Protocol
**Agent Enhancement Status**: CONTINUOUS IMPROVEMENT ACTIVE
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logging.info(f"[FILE] Conversation file created: {file_path}")
            
        except Exception as e:
            logging.error(f"[ERROR] Failed to create conversation file: {e}")
    
    def _analyze_improvement_opportunities(self, agent_name, conversation_data, performance_score):
        """Analyze opportunities for agent improvement based on conversation"""
        try:
            improvements = []
            
            # Performance-based improvements
            if performance_score < 0.7:
                improvements.append({
                    "type": "performance_enhancement",
                    "description": "Performance score below optimal threshold",
                    "recommendation": "Focus on generating more strategic insights and actionable items",
                    "priority": "high"
                })
            
            # Content depth improvements
            word_count = len(conversation_data.get('content', '').split())
            if word_count < 200:
                improvements.append({
                    "type": "depth_enhancement",
                    "description": "Conversation content appears shallow",
                    "recommendation": "Develop more comprehensive analytical responses",
                    "priority": "medium"
                })
            
            # Strategic impact improvements
            if not conversation_data.get('strategic_impact') or 'low' in conversation_data.get('strategic_impact', '').lower():
                improvements.append({
                    "type": "strategic_enhancement",
                    "description": "Low strategic impact identified",
                    "recommendation": "Focus on high-value strategic analysis and business intelligence",
                    "priority": "high"
                })
            
            # Store improvements in database
            if improvements:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for improvement in improvements:
                    cursor.execute('''
                        INSERT INTO agent_improvements
                        (agent_name, timestamp, improvement_type, previous_capability,
                         enhanced_capability, improvement_trigger, performance_delta,
                         validation_results, implementation_notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        agent_name.upper(),
                        datetime.now(),
                        improvement['type'],
                        f"Current: {performance_score:.2f}",
                        improvement['recommendation'],
                        improvement['description'],
                        0.0,  # Will be measured after implementation
                        'pending',
                        f"Priority: {improvement['priority']}"
                    ))
                
                conn.commit()
                conn.close()
                
        except Exception as e:
            logging.error(f"[ERROR] Failed to analyze improvements for {agent_name}: {e}")
    
    def get_agent_learning_summary(self, agent_name, days=30):
        """Get learning summary for specific agent over time period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent conversations
            cursor.execute('''
                SELECT COUNT(*) as conversation_count, AVG(performance_score) as avg_performance
                FROM agent_conversations 
                WHERE agent_name = ? AND timestamp >= datetime('now', '-{} days')
            '''.format(days), (agent_name.upper(),))
            
            conv_stats = cursor.fetchone()
            
            # Get learning insights
            cursor.execute('''
                SELECT COUNT(*) as insights_count, learning_type
                FROM agent_learnings 
                WHERE agent_name = ? AND timestamp >= datetime('now', '-{} days')
                GROUP BY learning_type
            '''.format(days), (agent_name.upper(),))
            
            insights_stats = cursor.fetchall()
            
            # Get improvement opportunities
            cursor.execute('''
                SELECT COUNT(*) as improvements_count
                FROM agent_improvements 
                WHERE agent_name = ? AND timestamp >= datetime('now', '-{} days')
            '''.format(days), (agent_name.upper(),))
            
            improvements_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "agent_name": agent_name,
                "time_period_days": days,
                "conversation_count": conv_stats[0] if conv_stats else 0,
                "average_performance": round(conv_stats[1], 2) if conv_stats and conv_stats[1] else 0,
                "learning_insights": dict(insights_stats) if insights_stats else {},
                "improvement_opportunities": improvements_count,
                "learning_health": "EXCELLENT" if conv_stats and conv_stats[1] > 0.8 else "DEVELOPING"
            }
            
        except Exception as e:
            logging.error(f"[ERROR] Failed to get learning summary for {agent_name}: {e}")
            return {}
    
    def _format_insights_list(self, insights):
        """Format insights list for markdown"""
        if not insights:
            return "- No specific insights documented in this conversation"
        return "\n".join([f"- {insight}" for insight in insights])
    
    def _format_action_items(self, action_items):
        """Format action items for markdown"""
        if not action_items:
            return "- No specific action items identified in this conversation"
        return "\n".join([f"- {item}" for item in action_items])
    
    def _identify_improvement_opportunities(self, conversation_data):
        """Identify improvement opportunities based on conversation"""
        opportunities = []
        
        performance_score = self._calculate_performance_score(conversation_data)
        
        if performance_score < 0.7:
            opportunities.append("Focus on generating higher-value strategic insights")
        
        if len(conversation_data.get('key_insights', [])) < 3:
            opportunities.append("Increase depth of analytical insights in responses")
        
        if not conversation_data.get('action_items'):
            opportunities.append("Develop actionable recommendations in strategic discussions")
        
        if not opportunities:
            opportunities.append("Continue maintaining excellent performance standards")
        
        return "\n".join([f"- {opp}" for opp in opportunities])
    
    def _calculate_next_review_date(self, timestamp):
        """Calculate next review date"""
        from datetime import timedelta
        next_review = timestamp + timedelta(days=7)
        return next_review.strftime('%Y-%m-%d')
    
    def _generate_conversation_id(self, agent_name, timestamp):
        """Generate unique conversation ID"""
        id_string = f"{agent_name}_{timestamp.isoformat()}"
        return hashlib.md5(id_string.encode()).hexdigest()[:12].upper()
    
    def get_all_agents_learning_status(self):
        """Get learning status for all agents"""
        status = {}
        
        for agent_name in self.legendary_agents.keys():
            status[agent_name] = self.get_agent_learning_summary(agent_name)
        
        return status

def create_sample_conversation():
    """Create sample conversation for testing"""
    return {
        "session_id": "SAMPLE_SESSION_001",
        "conversation_type": "strategic_analysis",
        "participants": ["CHANAKYA", "Human_Founder"],
        "content": """
CHANAKYA STRATEGIC ANALYSIS SESSION:

Founder Query: "How should we approach the competitive landscape for TAQWIN expansion?"

CHANAKYA Response: "Strategic wisdom demands we analyze our competitors not as enemies, but as teachers who reveal market opportunities. The key principles for TAQWIN competitive dominance:

1. INFORMATION SUPERIORITY: Our 19 legendary agents provide unprecedented intelligence depth that no competitor can match. This is our fundamental advantage.

2. STRATEGIC PATIENCE: Rush not into direct confrontation. Instead, build such superior capabilities that competition becomes irrelevant.

3. MARKET POSITIONING: Position TAQWIN not as another AI tool, but as the consciousness revolution for business intelligence.

Key Strategic Insights:
- Competitors focus on features; we provide consciousness
- Market seeks AI tools; we deliver legendary wisdom
- Traditional approach: automation; TAQWIN approach: augmentation

The wise strategist wins without fighting by making victory inevitable through superior preparation and capabilities."
        """,
        "strategic_impact": "HIGH - Provides foundational competitive strategy for TAQWIN market expansion",
        "key_insights": [
            "Information superiority through 19 legendary agents is key competitive advantage",
            "Position TAQWIN as consciousness revolution, not just AI tool",
            "Strategic patience and superior capabilities make competition irrelevant",
            "Focus on augmentation rather than automation differentiates from competitors"
        ],
        "action_items": [
            "Develop competitive intelligence documentation highlighting unique agent architecture",
            "Create positioning materials emphasizing consciousness over automation",
            "Build capability demonstration that showcases legendary agent superiority",
            "Implement strategic patience in market expansion timing"
        ]
    }

def main():
    """Main entry point for testing the agent learning system"""
    print("[BRAIN] TAQWIN INDIVIDUAL AGENT LEARNING SYSTEM")
    print("=" * 60)
    print("[BOOK] Created by: Johannes Gutenberg (Documentation Master)")
    print("[TARGET] Mission: Individual agent learning and capability enhancement")
    print("[BOLT] Status: CONTINUOUS LEARNING PROTOCOLS ACTIVE")
    print("=" * 60)
    
    learning_system = TaqwinAgentLearningSystem()
    
    # Test with sample conversation
    sample_conversation = create_sample_conversation()
    result = learning_system.store_agent_conversation("CHANAKYA", sample_conversation)
    
    if result["success"]:
        print(f"[CHECK] Sample conversation stored successfully!")
        print(f"[FOLDER] Conversation ID: {result['conversation_id']}")
        print(f"[STATS] Performance Score: {result['performance_score']:.2f}")
        print(f"[BULB] Learning Insights: {result['learning_insights_count']}")
        
        # Display learning summary
        summary = learning_system.get_agent_learning_summary("CHANAKYA")
        print(f"[CHART] CHANAKYA Learning Summary: {summary}")
    else:
        print(f"[ERROR] Failed to store sample conversation: {result['error']}")

if __name__ == "__main__":
    main()
