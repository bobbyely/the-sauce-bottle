# The Sauce Bottle - Google AI & MCP Development Roadmap
*Agentic AI-Driven Political Fact-Checking Platform*

## Executive Summary
This roadmap spans 15-20 months with 5-10 hours/week commitment, building an AI-powered fact-checking platform using Google's AI ecosystem and Model Context Protocol (MCP) servers. Total estimated effort: 320-450 hours across 7 phases.

---

## Refined Technology Stack

### Core AI Infrastructure
- **Primary AI**: Google Gemini Pro/Ultra via Google AI SDK
- **Agent Framework**: Google Agent-to-Agent (A2A) communication
- **Context Servers**: Custom MCP servers for specialized tasks
- **Vector Search**: Google Vertex AI Vector Search
- **Knowledge Management**: Google Cloud Knowledge Graph
- **Web Automation**: Playwright + Google AI guidance
- **Backend**: FastAPI with Google AI SDK integration
- **Frontend**: Vue.js with Google AI JavaScript SDK
- **Database**: PostgreSQL + Google Cloud SQL
- **Deployment**: Google Cloud Platform (GCP)

### MCP Server Architecture
```python
# Custom MCP Servers for specialized tasks
servers = {
    "political-scraper": "mcp://political-content-scraper",
    "fact-checker": "mcp://australian-politics-facts", 
    "evidence-gatherer": "mcp://multi-source-research",
    "report-generator": "mcp://publication-writer"
}
```

---

## Phase 1: Google AI Foundation & MCP Setup (Weeks 1-10, 50-75 hours)

### Learning Objectives
- Master Google AI SDK and Gemini API
- Understand MCP server development and deployment
- Set up Google A2A agent communication
- Implement Google Vertex AI Vector Search

### Technical Deliverables
**Week 1-3: Google AI Infrastructure**
```python
# Core Google AI integration
import google.generativeai as genai
from google.cloud import aiplatform
from google.ai import generativelanguage as glm

class GoogleAIAgent:
    def __init__(self, model_name="gemini-pro"):
        genai.configure(api_key=os.getenv('GOOGLE_AI_API_KEY'))
        self.model = genai.GenerativeModel(model_name)
        self.vector_search = aiplatform.MatchingEngineIndex()
    
    async def classify_political_content(self, text: str) -> dict:
        prompt = f"""
        Analyze this political content and classify:
        Content: {text}
        
        Return JSON with: politician, party, topic, claim_type, factual_claims
        """
        response = await self.model.generate_content_async(prompt)
        return json.loads(response.text)
```

**Week 4-6: MCP Server Development**
```python
# Custom MCP Server for Political Content
from mcp import Server, Tool
import asyncio

class PoliticalScrapingMCP(Server):
    def __init__(self):
        super().__init__("political-scraper")
        self.register_tools()
    
    def register_tools(self):
        @self.tool("scrape_abc_news")
        async def scrape_abc_news(query: str) -> dict:
            """Scrape ABC News for political content"""
            # Google AI guided scraping logic
            pass
        
        @self.tool("extract_quotes")  
        async def extract_quotes(article: str) -> list:
            """Extract political quotes using Gemini"""
            # AI-powered quote extraction
            pass

# Deploy MCP server
server = PoliticalScrapingMCP()
await server.serve("localhost:8001")
```

**Week 7-8: Google A2A Agent Communication**
```python
# Agent-to-Agent communication setup
from google.ai.agents import Agent, AgentCommunication

class FactCheckingAgentNetwork:
    def __init__(self):
        self.scraper_agent = Agent("content-scraper")
        self.analyzer_agent = Agent("fact-analyzer") 
        self.reporter_agent = Agent("report-generator")
        
        # Set up A2A communication channels
        self.setup_agent_communication()
    
    def setup_agent_communication(self):
        # Scraper -> Analyzer pipeline
        self.scraper_agent.subscribe_to(
            "new_content", 
            self.analyzer_agent.analyze_content
        )
        
        # Analyzer -> Reporter pipeline  
        self.analyzer_agent.subscribe_to(
            "fact_check_complete",
            self.reporter_agent.generate_report
        )
```

**Week 9-10: Vector Search & Knowledge Base**
- Google Vertex AI Vector Search deployment
- Political statement embeddings using Gemini
- Semantic similarity search for historical statements
- Basic RAG implementation with Google AI

### Success Criteria
- ✅ Google AI SDK successfully classifies political content (80%+ accuracy)
- ✅ MCP servers handle specialized tasks reliably
- ✅ A2A agents communicate and coordinate effectively
- ✅ Vector search returns relevant historical statements

### Learning Resources
- **Google AI SDK**: Official documentation and samples
- **MCP Protocol**: Anthropic's MCP specification and examples
- **Google A2A**: Google AI agent communication guides
- **Vertex AI**: Google Cloud AI/ML platform tutorials

---

## Phase 2: Intelligent Web Scraping with MCP Servers (Weeks 11-18, 70-90 hours)

### Learning Objectives
- Advanced MCP server patterns for web scraping
- Google AI guided web navigation
- Multi-agent coordination using A2A
- Adaptive scraping with Gemini intelligence

### Technical Deliverables
**Week 11-13: Advanced Scraping MCP Server**
```python
# Sophisticated scraping MCP server
class IntelligentScrapingMCP(Server):
    def __init__(self):
        super().__init__("intelligent-scraper")
        self.gemini = genai.GenerativeModel("gemini-pro")
        self.playwright = PlaywrightBrowser()
    
    @self.tool("analyze_page_structure")
    async def analyze_page_structure(self, url: str) -> dict:
        """Use Gemini to understand page layout"""
        screenshot = await self.playwright.screenshot(url)
        
        prompt = f"""
        Analyze this news website screenshot and identify:
        1. Article content selectors 
        2. Navigation patterns
        3. Anti-bot measures
        4. Content update mechanisms
        
        Return JSON with CSS selectors and scraping strategy.
        """
        
        response = await self.gemini.generate_content([
            prompt,
            {"mime_type": "image/png", "data": screenshot}
        ])
        return json.loads(response.text)
    
    @self.tool("adaptive_scrape")
    async def adaptive_scrape(self, site_config: dict) -> list:
        """Self-healing scraper that adapts to changes"""
        try:
            return await self.standard_scrape(site_config)
        except ScrapingError:
            # Ask Gemini to analyze what changed
            new_strategy = await self.analyze_page_structure(site_config['url'])
            return await self.scrape_with_new_strategy(new_strategy)
```

**Week 14-15: Multi-Source MCP Orchestration**
```python
# Orchestrator for multiple MCP servers
class ScrapingOrchestrator:
    def __init__(self):
        self.mcp_clients = {
            'abc': MCPClient("mcp://abc-news-scraper"),
            'guardian': MCPClient("mcp://guardian-au-scraper"), 
            'smh': MCPClient("mcp://smh-scraper"),
            'parliament': MCPClient("mcp://parliament-scraper")
        }
        
    async def coordinate_scraping(self, targets: list) -> dict:
        """Coordinate multiple MCP servers via A2A"""
        tasks = []
        for target in targets:
            client = self.mcp_clients[target['source']]
            task = client.call_tool("scrape_content", target['params'])
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return await self.deduplicate_and_merge(results)
```

**Week 16-18: Content Understanding MCP Server**
```python
class ContentAnalysisMCP(Server):
    def __init__(self):
        super().__init__("content-analyzer")
        self.gemini = genai.GenerativeModel("gemini-pro")
    
    @self.tool("extract_political_claims")
    async def extract_political_claims(self, article: str) -> list:
        """Extract factual claims from political articles"""
        prompt = f"""
        Analyze this political article and extract:
        1. Direct quotes from politicians
        2. Factual claims that can be verified
        3. Policy positions stated
        4. Statistical claims
        
        Article: {article}
        
        Return structured JSON with attribution and context.
        """
        
        response = await self.gemini.generate_content(prompt)
        return self.parse_claims_response(response.text)
    
    @self.tool("assess_claim_verifiability") 
    async def assess_claim_verifiability(self, claim: str) -> dict:
        """Determine if a claim can be fact-checked"""
        prompt = f"""
        Assess this political claim for fact-checking feasibility:
        Claim: "{claim}"
        
        Evaluate:
        1. Is it a factual claim or opinion?
        2. What evidence would be needed?
        3. What sources should be consulted?
        4. Confidence level for verification
        
        Return JSON assessment.
        """
        response = await self.gemini.generate_content(prompt)
        return json.loads(response.text)
```

### Success Criteria
- ✅ Autonomous scraping of 5+ Australian news sources
- ✅ 200+ political statements collected daily
- ✅ 90%+ accuracy in quote attribution via Gemini
- ✅ Self-healing scrapers adapt to site changes automatically

---

## Phase 3: Advanced Fact-Checking with Google A2A (Weeks 19-28, 90-120 hours)

### Learning Objectives
- Multi-step reasoning with Gemini Pro/Ultra
- Complex agent workflows using A2A
- Evidence synthesis and verification
- Advanced prompt engineering for fact-checking

### Technical Deliverables
**Week 19-21: Research Agent MCP Server**
```python
class ResearchAgentMCP(Server):
    def __init__(self):
        super().__init__("research-agent")
        self.gemini = genai.GenerativeModel("gemini-ultra")
        self.vector_search = VertexAIVectorSearch()
    
    @self.tool("create_research_plan")
    async def create_research_plan(self, claim: str) -> dict:
        """Generate comprehensive research strategy"""
        prompt = f"""
        Create a research plan to fact-check this claim:
        "{claim}"
        
        Consider:
        1. What specific facts need verification?
        2. What are the most authoritative sources?
        3. What historical context is relevant?
        4. What counter-evidence should be sought?
        5. What methodology should be used?
        
        Return detailed JSON research plan.
        """
        
        response = await self.gemini.generate_content(prompt)
        return json.loads(response.text)
    
    @self.tool("execute_research_step")
    async def execute_research_step(self, step: dict) -> dict:
        """Execute individual research step"""
        if step['type'] == 'database_search':
            return await self.search_internal_database(step['query'])
        elif step['type'] == 'web_search':
            return await self.search_web_sources(step['query'])
        elif step['type'] == 'document_analysis':
            return await self.analyze_documents(step['documents'])
        # Additional research step types...
```

**Week 22-24: Fact-Checking Agent Network**
```python
# Complex A2A agent network for fact-checking
class FactCheckingNetwork:
    def __init__(self):
        # Specialized agents
        self.research_agent = Agent("research-specialist")
        self.analysis_agent = Agent("claim-analyzer") 
        self.verification_agent = Agent("evidence-verifier")
        self.synthesis_agent = Agent("report-synthesizer")
        
        self.setup_a2a_workflows()
    
    def setup_a2a_workflows(self):
        # Research workflow
        self.research_agent.on_message("new_claim", self.start_research)
        self.research_agent.on_complete("research_plan", 
                                       self.analysis_agent.analyze_evidence)
        
        # Analysis workflow  
        self.analysis_agent.on_complete("evidence_analysis",
                                       self.verification_agent.verify_sources)
        
        # Synthesis workflow
        self.verification_agent.on_complete("verification_complete",
                                           self.synthesis_agent.create_report)
    
    async def start_research(self, claim_data: dict):
        """Initiate fact-checking process"""
        # Call research MCP server
        research_plan = await self.mcp_client.call_tool(
            "create_research_plan", 
            {"claim": claim_data['text']}
        )
        
        # Execute research steps
        evidence = []
        for step in research_plan['steps']:
            result = await self.mcp_client.call_tool(
                "execute_research_step", 
                step
            )
            evidence.append(result)
        
        # Send to analysis agent
        await self.analysis_agent.send_message("analyze_evidence", {
            "claim": claim_data,
            "evidence": evidence
        })
```

**Week 25-26: Evidence Synthesis MCP Server**
```python
class EvidenceSynthesisMCP(Server):
    def __init__(self):
        super().__init__("evidence-synthesizer")
        self.gemini = genai.GenerativeModel("gemini-ultra")
    
    @self.tool("synthesize_evidence")
    async def synthesize_evidence(self, evidence_package: dict) -> dict:
        """Synthesize evidence into coherent fact-check"""
        prompt = f"""
        Synthesize this evidence into a fact-check report:
        
        Claim: {evidence_package['claim']}
        Evidence: {json.dumps(evidence_package['evidence'], indent=2)}
        
        Provide:
        1. Verdict (True/False/Partly True/Unsubstantiated)
        2. Confidence level (0-100%)
        3. Key supporting evidence
        4. Key contradicting evidence  
        5. Important context/nuance
        6. Sources and methodology
        
        Write for general public readability.
        """
        
        response = await self.gemini.generate_content(prompt)
        return self.parse_fact_check_response(response.text)
    
    @self.tool("assess_confidence")
    async def assess_confidence(self, synthesis: dict) -> float:
        """Calculate confidence score for fact-check"""
        factors = {
            'source_quality': self.assess_source_quality(synthesis['sources']),
            'evidence_strength': self.assess_evidence_strength(synthesis['evidence']),
            'consensus_level': self.assess_consensus(synthesis['evidence']),
            'claim_specificity': self.assess_claim_specificity(synthesis['claim'])
        }
        
        # Use Gemini to weight factors contextually
        prompt = f"""
        Calculate confidence score (0-100) for this fact-check:
        Factors: {json.dumps(factors)}
        
        Consider Australian political context and source reliability.
        Return just the numeric score.
        """
        
        response = await self.gemini.generate_content(prompt)
        return float(response.text.strip())
```

**Week 27-28: Human-AI Collaboration Interface**
- Google AI powered review suggestions
- Confidence-based routing to human reviewers
- Interactive evidence exploration
- Continuous learning from human feedback

### Success Criteria
- ✅ Automated fact-checking with 85%+ accuracy
- ✅ Evidence gathering from 10+ sources per claim via MCP
- ✅ Clear confidence scoring with Gemini assessment
- ✅ Human reviewers process 3x more content with AI assistance

---

## Phase 4: Intelligent User Experience with Google AI (Weeks 29-36, 70-90 hours)

### Learning Objectives
- Google AI JavaScript SDK integration
- Conversational interfaces with Gemini
- Real-time AI explanations
- Personalized content delivery

### Technical Deliverables
**Week 29-31: Conversational Interface**
```javascript
// Vue.js component with Google AI SDK
import { GoogleGenerativeAI } from "@google/generative-ai";

export default {
  name: 'AIFactChecker',
  data() {
    return {
      genAI: null,
      conversation: [],
      currentQuery: ''
    }
  },
  
  async mounted() {
    this.genAI = new GoogleGenerativeAI(process.env.VUE_APP_GOOGLE_AI_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-pro" });
  },
  
  methods: {
    async askFactCheck(query) {
      const prompt = `
        User is asking about Australian politics: "${query}"
        
        Search our fact-checking database and provide:
        1. Direct answer if we have fact-checks on this topic
        2. Related fact-checks that might be relevant  
        3. Suggest specific politicians or claims to investigate
        4. If no data exists, explain what we'd need to fact-check this
        
        Be conversational and helpful.
      `;
      
      const result = await this.model.generateContent(prompt);
      return result.response.text();
    },
    
    async explainFactCheck(factCheckId) {
      // Get fact-check data via API
      const factCheck = await this.$api.getFactCheck(factCheckId);
      
      const prompt = `
        Explain this fact-check in simple terms:
        ${JSON.stringify(factCheck)}
        
        User context: ${this.userProfile.comprehension_level}
        
        Provide clear explanation of:
        1. What was claimed
        2. What we found
        3. Why we reached this conclusion
        4. What sources we used
      `;
      
      const result = await this.model.generateContent(prompt);
      return result.response.text();
    }
  }
}
```

**Week 32-33: Personalization MCP Server**
```python
class PersonalizationMCP(Server):
    def __init__(self):
        super().__init__("personalization-engine")
        self.gemini = genai.GenerativeModel("gemini-pro")
    
    @self.tool("create_daily_briefing")
    async def create_daily_briefing(self, user_profile: dict) -> dict:
        """Generate personalized political briefing"""
        # Get recent statements and fact-checks
        recent_content = await self.get_recent_content()
        
        prompt = f"""
        Create personalized daily briefing for user:
        Profile: {json.dumps(user_profile)}
        Recent Content: {json.dumps(recent_content)}
        
        Prioritize based on:
        1. User's followed politicians  
        2. User's topic interests
        3. User's reading level
        4. Breaking developments
        
        Format as engaging newsletter with clear sections.
        """
        
        response = await self.gemini.generate_content(prompt)
        return self.format_briefing(response.text)
    
    @self.tool("explain_for_user")
    async def explain_for_user(self, content: str, user_level: str) -> str:
        """Tailor explanations to user sophistication"""
        prompt = f"""
        Explain this political content for {user_level} audience:
        {content}
        
        Adjust:
        - Vocabulary complexity
        - Background context provided
        - Detail level
        - Use of political jargon
        
        Keep engaging and informative.
        """
        
        response = await self.gemini.generate_content(prompt)
        return response.text
```

**Week 34-36: Advanced UX Features**
- AI-generated content summaries with Gemini
- Intelligent search with query expansion
- Real-time explanation of AI reasoning
- Interactive evidence exploration interface

### Success Criteria
- ✅ Natural language queries work 95% of the time
- ✅ Users engage 3x longer with personalized content
- ✅ AI explanations rated "helpful" by 80%+ users
- ✅ Complex topics explained appropriately for user level

---

## Phase 5: Content Generation & Advanced Analysis (Weeks 37-44, 80-100 hours)

### Learning Objectives
- Advanced content generation with Gemini Ultra
- Multi-modal analysis capabilities
- Automated report generation
- Predictive political analysis

### Technical Deliverables
**Week 37-39: Report Generation MCP Server**
```python
class ReportGenerationMCP(Server):
    def __init__(self):
        super().__init__("report-generator")
        self.gemini_ultra = genai.GenerativeModel("gemini-ultra")
    
    @self.tool("generate_politician_report")
    async def generate_politician_report(self, politician: str, timeframe: str) -> dict:
        """Generate comprehensive politician analysis"""
        # Gather all statements and fact-checks
        data = await self.gather_politician_data(politician, timeframe)
        
        prompt = f"""
        Generate comprehensive analysis report for {politician}:
        
        Data: {json.dumps(data)}
        Timeframe: {timeframe}
        
        Include:
        1. Executive Summary
        2. Statement Accuracy Analysis
        3. Topic Consistency Review  
        4. Contradiction Highlights
        5. Trend Analysis
        6. Comparison to Party Positions
        7. Public Accountability Metrics
        
        Write in professional journalism style suitable for publication.
        Include data visualizations suggestions.
        Cite all sources properly.
        """
        
        response = await self.gemini_ultra.generate_content(prompt)
        return self.format_report(response.text, data)
    
    @self.tool("create_trend_analysis")
    async def create_trend_analysis(self, topic: str, period: str) -> dict:
        """Analyze political trends and patterns"""
        trend_data = await self.gather_trend_data(topic, period)
        
        prompt = f"""
        Analyze political trends for topic: {topic}
        Period: {period}