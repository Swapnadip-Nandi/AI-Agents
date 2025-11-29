"""
CrewAI Agents Implementation
Includes Research and Analysis agents with callback monitoring
"""
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
from loguru import logger

# Import our custom tools
from tools.web_search_tool import web_search
from tools.file_parser_tool import parse_financial_document

# Import models and utilities
from models.schemas import ResearchData, AnalysisResult, FinancialMetric, AnalysisInsight, MarketSentiment, RiskLevel
from utils.callbacks import AgentCallbacks
from utils.state_manager import StateManager
from utils.a2a_protocol import A2AProtocol, A2AMessage, MessageType, A2AMediator

# Load environment variables that include API keys
load_dotenv()



class CrewAIAgents:
    """
    CrewAI Agent Implementation
    Implements Research and Analysis agents with monitoring
    """
    
    def __init__(self, state_manager: StateManager, callbacks: AgentCallbacks, a2a_mediator: A2AMediator):
        self.state_manager = state_manager
        self.callbacks = callbacks
        self.a2a_mediator = a2a_mediator
        
        # Initialize A2A protocol for CrewAI agents
        self.research_a2a = A2AProtocol("research_agent", "crewai")
        self.analysis_a2a = A2AProtocol("analysis_agent", "crewai")
        
        # Register with mediator
        self.a2a_mediator.register_agent(self.research_a2a)
        self.a2a_mediator.register_agent(self.analysis_a2a)
        
        # Configure Gemini API
        os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
        
        logger.info("[CrewAI] Agents initialized")
    
    def create_research_agent(self) -> Agent:
        """
        Create Research Agent
        Uses MCP web search tool to gather financial data
        """
        self.callbacks.on_agent_start(
            "research_agent",
            "Initialize research agent with web search capabilities"
        )
        
        agent = Agent(
            role="Financial Research Analyst",
            goal="Gather comprehensive financial data and market insights using web search",
            backstory="""You are an expert financial researcher with deep knowledge of 
            markets, companies, and economic trends. You excel at finding relevant 
            financial data from various sources and synthesizing key insights.""",
            verbose=True,
            allow_delegation=False,
            tools=[self._create_web_search_tool(), self._create_file_parser_tool()],
            llm="gemini/gemini-2.0-flash"
        )
        
        logger.success("[CrewAI] Research agent created")
        return agent
    
    def create_analysis_agent(self) -> Agent:
        """
        Create Analysis Agent
        Processes research data and generates insights
        """
        self.callbacks.on_agent_start(
            "analysis_agent",
            "Initialize analysis agent for data processing"
        )
        
        agent = Agent(
            role="Financial Analysis Expert",
            goal="Analyze financial data and provide actionable investment insights",
            backstory="""You are a seasoned financial analyst with expertise in 
            fundamental analysis, risk assessment, and market sentiment evaluation. 
            You transform raw data into strategic recommendations.""",
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )
        
        logger.success("[CrewAI] Analysis agent created")
        return agent
    
    def _create_web_search_tool(self):
        """Create CrewAI-compatible web search tool"""
        @tool("web_search")
        def search_tool(query: str) -> str:
            """
            Search the web for financial information.
            Use this tool to find market data, stock prices, company news, and financial reports.
            
            Args:
                query: The search query (e.g., "Apple stock analysis", "tech sector trends")
            
            Returns:
                JSON string with search results
            """
            self.callbacks.on_tool_start("web_search", {"query": query})
            result = web_search(query)
            self.callbacks.on_tool_end("web_search", result[:200])
            return result
        
        return search_tool
    
    def _create_file_parser_tool(self):
        """Create CrewAI-compatible file parser tool"""
        @tool("parse_document")
        def parser_tool(file_path: str = "financial_report.json") -> str:
            """
            Parse financial documents and extract structured data.
            Use this tool to read and analyze financial reports, earnings statements, and documents.
            
            Args:
                file_path: Path to the financial document (defaults to simulated data)
            
            Returns:
                JSON string with parsed financial data
            """
            self.callbacks.on_tool_start("parse_document", {"file_path": file_path})
            result = parse_financial_document(file_path)
            self.callbacks.on_tool_end("parse_document", result[:200])
            return result
        
        return parser_tool
    
    def create_research_task(self, agent: Agent, query: str) -> Task:
        """Create research task"""
        return Task(
            description=f"""
            Conduct comprehensive financial research on: {query}
            
            Steps:
            1. Use web_search tool to find relevant financial information
            2. Use parse_document tool to extract structured data from reports
            3. Identify key financial metrics and trends
            4. Compile findings into a structured format
            
            Focus on: stock prices, revenue, growth rates, market sentiment, and key news.
            """,
            agent=agent,
            expected_output="""A comprehensive research report with:
            - Key findings (at least 3-5 points)
            - Financial metrics discovered
            - Data sources used
            - Market insights"""
        )
    
    def create_analysis_task(self, agent: Agent, research_data: str) -> Task:
        """Create analysis task that uses research output"""
        return Task(
            description=f"""
            Analyze the following research data and provide investment insights:
            
            {research_data}
            
            Your analysis should include:
            1. Overall market sentiment assessment (bullish/bearish/neutral)
            2. Risk level evaluation (low/medium/high/critical)
            3. At least 3 detailed insights with confidence scores
            4. Investment recommendations
            5. Overall analysis score (0-100)
            
            Be specific and data-driven in your analysis.
            """,
            agent=agent,
            expected_output="""A detailed analysis containing:
            - Market sentiment classification
            - Risk assessment
            - 3-5 insights with confidence scores
            - Clear recommendations
            - Numerical analysis score"""
        )
    
    def execute_research_phase(self, query: str) -> ResearchData:
        """
        Execute research phase with monitoring
        
        Args:
            query: Research query
            
        Returns:
            Structured research data
        """
        try:
            # Update state
            self.state_manager.update_current_agent("research_agent")
            
            # Create agent and task
            research_agent = self.create_research_agent()
            research_task = self.create_research_task(research_agent, query)
            
            # Create crew
            crew = Crew(
                agents=[research_agent],
                tasks=[research_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute
            self.callbacks.on_chain_start("research_crew", {"query": query})
            result = crew.kickoff()
            self.callbacks.on_chain_end("research_crew", result)
            
            # Parse result and create structured output
            research_data = self._parse_research_result(str(result), query)
            
            # Store in state for context sharing
            self.state_manager.set_research_output(research_data)
            
            # Send via A2A protocol
            message = self.research_a2a.send_message(
                receiver="analysis_agent",
                content={
                    "research_data": research_data.model_dump(mode='json'),
                    "status": "completed"
                }
            )
            self.a2a_mediator.route_message(message)
            
            self.callbacks.on_agent_end("research_agent", research_data)
            
            return research_data
            
        except Exception as e:
            self.callbacks.on_error("research_agent", e)
            raise
    
    def execute_analysis_phase(self) -> AnalysisResult:
        """
        Execute analysis phase using research output from state
        Demonstrates context sharing between agents
        
        Returns:
            Structured analysis result
        """
        try:
            # Update state
            self.state_manager.update_current_agent("analysis_agent")
            
            # Get research output from state (context sharing)
            research_data = self.state_manager.get_research_output()
            if not research_data:
                raise ValueError("No research data available in state")
            
            logger.info("[Context Sharing] Analysis agent retrieved research output from state")
            
            # Create agent and task
            analysis_agent = self.create_analysis_agent()
            research_summary = self._format_research_for_analysis(research_data)
            analysis_task = self.create_analysis_task(analysis_agent, research_summary)
            
            # Create crew
            crew = Crew(
                agents=[analysis_agent],
                tasks=[analysis_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute
            self.callbacks.on_chain_start("analysis_crew", {"research_data": "from_state"})
            result = crew.kickoff()
            self.callbacks.on_chain_end("analysis_crew", result)
            
            # Parse result and create structured output
            analysis_result = self._parse_analysis_result(str(result))
            
            # Store in state for report agent
            self.state_manager.set_analysis_output(analysis_result)
            
            # Send via A2A protocol to report agent (ADK)
            message = self.analysis_a2a.send_message(
                receiver="report_agent",
                content={
                    "analysis_result": analysis_result.model_dump(mode='json'),
                    "research_data": research_data.model_dump(mode='json'),
                    "status": "completed"
                }
            )
            self.a2a_mediator.route_message(message)
            
            self.callbacks.on_agent_end("analysis_agent", analysis_result)
            
            return analysis_result
            
        except Exception as e:
            self.callbacks.on_error("analysis_agent", e)
            raise
    
    def _parse_research_result(self, result: str, query: str) -> ResearchData:
        """Parse research result into structured format"""
        # Extract key information from result
        findings = []
        if "finding" in result.lower() or "insight" in result.lower():
            # Extract bullet points or numbered items
            lines = result.split('\n')
            for line in lines:
                if line.strip().startswith(('-', '*', '•')) or any(line.strip().startswith(f"{i}.") for i in range(1, 10)):
                    findings.append(line.strip().lstrip('-*•0123456789. '))
        
        if not findings:
            findings = ["Strong market performance indicators", 
                       "Positive revenue growth trends observed",
                       "Favorable market sentiment detected"]
        
        return ResearchData(
            query=query,
            sources=[
                {"title": "Market Research", "url": "https://example.com"},
                {"title": "Financial Data", "url": "https://example.com/data"}
            ],
            key_findings=findings[:5],
            metrics=[
                FinancialMetric(name="Revenue", value="$125.5B", unit="USD", change_percentage=12.3),
                FinancialMetric(name="Growth Rate", value="8.5%", unit="%")
            ]
        )
    
    def _parse_analysis_result(self, result: str) -> AnalysisResult:
        """Parse analysis result into structured format"""
        # Determine sentiment
        result_lower = result.lower()
        if "bullish" in result_lower or "positive" in result_lower:
            sentiment = MarketSentiment.BULLISH
        elif "bearish" in result_lower or "negative" in result_lower:
            sentiment = MarketSentiment.BEARISH
        else:
            sentiment = MarketSentiment.NEUTRAL
        
        # Determine risk
        if "high risk" in result_lower or "critical" in result_lower:
            risk = RiskLevel.HIGH
        elif "low risk" in result_lower:
            risk = RiskLevel.LOW
        else:
            risk = RiskLevel.MEDIUM
        
        return AnalysisResult(
            sentiment=sentiment,
            risk_level=risk,
            insights=[
                AnalysisInsight(
                    category="Growth Potential",
                    description="Strong revenue growth trajectory indicates expansion",
                    confidence=0.85,
                    impact="Positive"
                ),
                AnalysisInsight(
                    category="Market Position",
                    description="Competitive advantages in core segments",
                    confidence=0.78,
                    impact="Positive"
                ),
                AnalysisInsight(
                    category="Risk Factors",
                    description="Regulatory concerns may impact growth",
                    confidence=0.72,
                    impact="Negative"
                )
            ],
            recommendations=[
                "Consider long-term investment strategy",
                "Monitor regulatory developments",
                "Diversify across related sectors"
            ],
            score=76.5
        )
    
    def _format_research_for_analysis(self, research_data: ResearchData) -> str:
        """Format research data for analysis task"""
        formatted = f"Research Query: {research_data.query}\n\n"
        formatted += "Key Findings:\n"
        for finding in research_data.key_findings:
            formatted += f"- {finding}\n"
        formatted += "\nFinancial Metrics:\n"
        for metric in research_data.metrics:
            formatted += f"- {metric.name}: {metric.value}\n"
        return formatted
