
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Mycrew1():
    """Automated Research & Writing Flow Crews"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # AGENTS
    @agent
    def searcher_agent(self) -> Agent:
        return Agent(config=self.agents_config['searcher_agent'], verbose=True)

    @agent
    def validator_agent(self) -> Agent:
        return Agent(config=self.agents_config['validator_agent'], verbose=True)

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(config=self.agents_config['summarizer_agent'], verbose=True)

    @agent
    def insight_extractor_agent(self) -> Agent:
        return Agent(config=self.agents_config['insight_extractor_agent'], verbose=True)

    @agent
    def outline_creator_agent(self) -> Agent:
        return Agent(config=self.agents_config['outline_creator_agent'], verbose=True)

    @agent
    def writer_agent(self) -> Agent:
        return Agent(config=self.agents_config['writer_agent'], verbose=True)

    @agent
    def proofreader_agent(self) -> Agent:
        return Agent(config=self.agents_config['proofreader_agent'], verbose=True)

    # TASKS
    @task
    def search_papers(self) -> Task:
        return Task(config=self.tasks_config['search_papers'])

    @task
    def validate_papers(self) -> Task:
        return Task(config=self.tasks_config['validate_papers'])

    @task
    def summarize_papers(self) -> Task:
        return Task(config=self.tasks_config['summarize_papers'])

    @task
    def extract_insights(self) -> Task:
        return Task(config=self.tasks_config['extract_insights'])

    @task
    def create_outline(self) -> Task:
        return Task(config=self.tasks_config['create_outline'])

    @task
    def write_draft(self) -> Task:
        return Task(config=self.tasks_config['write_draft'])

    @task
    def proofread_article(self) -> Task:
        return Task(config=self.tasks_config['proofread_article'])

    # CREWS
    @crew
    def research_crew(self) -> Crew:
        return Crew(
            agents=[self.searcher_agent(), self.validator_agent()],
            tasks=[self.search_papers(), self.validate_papers()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def analysis_crew(self) -> Crew:
        return Crew(
            agents=[self.summarizer_agent(), self.insight_extractor_agent()],
            tasks=[self.summarize_papers(), self.extract_insights()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def writing_crew(self) -> Crew:
        return Crew(
            agents=[self.outline_creator_agent(), self.writer_agent(), self.proofreader_agent()],
            tasks=[self.create_outline(), self.write_draft(), self.proofread_article()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def full_flow(self) -> Crew:
        """Full Automated Research & Writing Flow"""
        return Crew(
            agents=[
                self.searcher_agent(), self.validator_agent(),
                self.summarizer_agent(), self.insight_extractor_agent(),
                self.outline_creator_agent(), self.writer_agent(), self.proofreader_agent()
            ],
            tasks=[
                self.search_papers(), self.validate_papers(),
                self.summarize_papers(), self.extract_insights(),
                self.create_outline(), self.write_draft(), self.proofread_article()
            ],
            process=Process.sequential,
            verbose=True,
        )
