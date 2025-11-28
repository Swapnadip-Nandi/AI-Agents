#!/usr/bin/env python3
"""
CrewAI CLI-based Code Assistant Crew
Uses YAML configuration files for agents and tasks.
"""

import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileWriterTool

# Load environment variables
load_dotenv()

# Configure API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "groq/llama3-8b-8192"


class YAMLCodeAssistantCrew:
    def __init__(self, config_dir="code_assistant_crew"):
        self.config_dir = config_dir
        self.file_writer = FileWriterTool()

    def load_config(self, filename):
        """Load YAML configuration file."""
        filepath = os.path.join(self.config_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def create_agents_from_yaml(self):
        """Create agents from YAML configuration."""
        agents_config = self.load_config('agents.yaml')
        agents = {}

        for agent_name, config in agents_config.items():
            tools = []
            if agent_name in ['coder', 'reviewer']:
                tools = [self.file_writer]

            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                verbose=True,
                allow_delegation=False,
                tools=tools
            )
            agents[agent_name] = agent

        return agents

    def create_tasks_from_yaml(self, agents, user_query):
        """Create tasks from YAML configuration."""
        tasks_config = self.load_config('tasks.yaml')
        tasks = []
        task_objects = {}

        for task_name, config in tasks_config.items():
            # Replace placeholder in description
            description = config['description'].replace('{user_query}', user_query)

            # Get context tasks if specified
            context = []
            if 'context' in config:
                for context_task_name in config['context']:
                    if context_task_name in task_objects:
                        context.append(task_objects[context_task_name])

            task = Task(
                description=description,
                expected_output=config['expected_output'],
                agent=agents[config['agent']],
                context=context
            )

            tasks.append(task)
            task_objects[task_name] = task

        return tasks

    def run(self, user_query):
        """Execute the code assistant crew workflow."""
        print(f"🚀 Starting YAML-based Code Assistant Crew for query: '{user_query}'")
        print("=" * 60)

        # Create agents and tasks from YAML
        agents = self.create_agents_from_yaml()
        tasks = self.create_tasks_from_yaml(agents, user_query)

        # Create and configure crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        # Execute the crew
        result = crew.kickoff()

        print("\n" + "=" * 60)
        print("🎉 YAML-based Code Assistant Crew workflow completed!")
        print("📁 Check 'solution.py' for the generated code")
        print("📝 Check 'review.txt' for the code review feedback")

        return result


def main():
    """Main function to run the YAML-based Code Assistant Crew."""
    print("Welcome to the YAML-based Code Assistant Crew! 👨‍💻")
    print("=" * 60)

    # Get user input
    user_query = input("\n🤔 Please describe the programming problem you need help with:\n> ")

    if not user_query.strip():
        print("❌ No query provided. Please try again.")
        return

    # Initialize and run the crew
    try:
        crew_assistant = YAMLCodeAssistantCrew()
        result = crew_assistant.run(user_query)
        print(f"\n✅ Final Result:\n{result}")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("Please check your YAML configuration files and try again.")


if __name__ == "__main__":
    main()
