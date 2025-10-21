from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_multi_agent.tools.custom_tool import WebSearchTool, SEOKeywordTool, DataAnalysisTool
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewaiMultiAgent():
    """CrewaiMultiAgent crew for E-commerce Product Launch Campaign"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # Initialize LLM from environment variables with fallback
    model = os.getenv('MODEL', 'gemini/gemini-2.5-flash')
    fallback_model = os.getenv('FALLBACK_MODEL', 'gemini/gemini-2.0-flash')
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key:
        try:
            # Primary LLM with optimized settings to reduce API calls
            llm = LLM(
                model=model,
                api_key=api_key,
                temperature=0.3,  # Lower temperature for more consistent outputs
                max_tokens=2048   # Reduced token limit to speed up responses
            )
            print(f"✓ Primary LLM initialized: {model}")
        except Exception as e:
            print(f"⚠ Primary model failed, using fallback: {fallback_model}")
            llm = LLM(
                model=fallback_model,
                api_key=api_key,
                temperature=0.3,
                max_tokens=2048
            )
    else:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # Initialize custom tools
    web_search_tool = WebSearchTool()
    seo_keyword_tool = SEOKeywordTool()
    data_analysis_tool = DataAnalysisTool()
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
    @agent
    def lead_planner(self) -> Agent:
        """
        Lead Planner Agent - Orchestrates campaign strategy and coordination
        DELEGATION DISABLED to prevent tool validation errors
        """
        return Agent(
            config=self.agents_config['lead_planner'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,  # ✓ DISABLED to prevent delegation tool errors
            max_iter=5,  # ✓ Reduced iterations
            max_retry_limit=2,  # ✓ Reduced retries
            llm=self.llm
        )

    @agent
    def market_researcher(self) -> Agent:
        """
        Market Researcher Agent - Conducts market analysis and competitor research
        Uses web search and data analysis tools
        """
        return Agent(
            config=self.agents_config['market_researcher'], # type: ignore[index]
            verbose=True,
            tools=[self.web_search_tool, self.data_analysis_tool],
            max_iter=5,  # ✓ Reduced to prevent excessive API calls
            max_retry_limit=2,
            allow_delegation=False,  # ✓ Disable delegation
            llm=self.llm
        )

    @agent
    def seo_specialist(self) -> Agent:
        """
        SEO Specialist Agent - Performs keyword research and optimization strategy
        Uses SEO keyword tool and web search
        """
        return Agent(
            config=self.agents_config['seo_specialist'], # type: ignore[index]
            verbose=True,
            tools=[self.seo_keyword_tool, self.web_search_tool],
            max_iter=5,  # ✓ Reduced iterations
            max_retry_limit=2,
            allow_delegation=False,  # ✓ Disable delegation
            llm=self.llm
        )

    @agent
    def copywriter(self) -> Agent:
        """
        Copywriter Agent - Creates compelling product copy and marketing content
        """
        return Agent(
            config=self.agents_config['copywriter'], # type: ignore[index]
            verbose=True,
            max_iter=5,  # ✓ Reduced iterations
            max_retry_limit=2,
            allow_delegation=False,  # ✓ Disable delegation
            llm=self.llm
        )

    @agent
    def social_media_marketer(self) -> Agent:
        """
        Social Media Marketer Agent - Develops social media campaigns and content
        """
        return Agent(
            config=self.agents_config['social_media_marketer'], # type: ignore[index]
            verbose=True,
            max_iter=5,  # ✓ Reduced iterations
            max_retry_limit=2,
            allow_delegation=False,  # ✓ Disable delegation
            llm=self.llm
        )

    @agent
    def critic_validator(self) -> Agent:
        """
        Critic/Validator Agent - Reviews and validates all campaign materials
        """
        return Agent(
            config=self.agents_config['critic_validator'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            max_iter=5,  # ✓ Reduced iterations
            max_retry_limit=2,
            llm=self.llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    
    @task
    def planning_task(self) -> Task:
        """
        Task 1: Campaign Planning and Strategy Development
        Lead Planner defines campaign objectives, personas, and strategy
        """
        return Task(
            config=self.tasks_config['planning_task'], # type: ignore[index]
        )

    @task
    def market_research_task(self) -> Task:
        """
        Task 2: Market Research and Competitive Analysis
        Market Researcher gathers intelligence using web search and data analysis
        Runs in parallel with SEO research
        """
        return Task(
            config=self.tasks_config['market_research_task'], # type: ignore[index]
        )

    @task
    def seo_research_task(self) -> Task:
        """
        Task 3: SEO Keyword Research and Strategy
        SEO Specialist identifies high-value keywords
        Runs in parallel with market research
        """
        return Task(
            config=self.tasks_config['seo_research_task'], # type: ignore[index]
        )

    @task
    def copywriting_task(self) -> Task:
        """
        Task 4: Copywriting and Content Creation
        Copywriter creates Amazon listing copy based on research and SEO insights
        Depends on: planning, market research, SEO research
        Runs in parallel with social media task
        """
        return Task(
            config=self.tasks_config['copywriting_task'], # type: ignore[index]
        )

    @task
    def social_media_task(self) -> Task:
        """
        Task 5: Social Media Campaign Development
        Social Media Marketer creates platform-specific content
        Depends on: planning, market research, SEO research
        Runs in parallel with copywriting task
        """
        return Task(
            config=self.tasks_config['social_media_task'], # type: ignore[index]
        )

    @task
    def validation_task(self) -> Task:
        """
        Task 6: Quality Assurance and Validation
        Critic/Validator reviews all materials for quality and compliance
        Depends on: all previous tasks
        """
        return Task(
            config=self.tasks_config['validation_task'], # type: ignore[index]
        )

    @task
    def final_campaign_report(self) -> Task:
        """
        Task 7: Final Campaign Report Compilation
        Lead Planner compiles all validated materials into final deliverable
        Depends on: all previous tasks
        """
        return Task(
            config=self.tasks_config['final_campaign_report'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiMultiAgent crew for E-commerce Campaign"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Sequential process with context sharing
            verbose=True,
            max_rpm=10,  # ✓ CRITICAL: Limit to 10 requests per minute to prevent API overload
            # Workflow explanation:
            # 1. Planning (sequential) - Lead Planner sets strategy
            # 2. Research Phase (parallel potential) - Market Research + SEO Research
            # 3. Content Creation (parallel potential) - Copywriting + Social Media
            # 4. Validation (sequential) - Critic reviews all
            # 5. Final Report (sequential) - Lead Planner compiles
            # Note: CrewAI's sequential process with context sharing allows 
            # tasks to access previous outputs, simulating coordination
        )

