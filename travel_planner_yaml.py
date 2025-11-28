#!/usr/bin/env python3
"""
CrewAI CLI-based Travel Planner Crew
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


class YAMLTravelPlannerCrew:
    def __init__(self, config_dir="travel_planner_crew"):
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
            if agent_name in ['itinerary_planner', 'budget_advisor']:
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

    def create_tasks_from_yaml(self, agents, region, trip_type):
        """Create tasks from YAML configuration."""
        tasks_config = self.load_config('tasks.yaml')
        tasks = []
        task_objects = {}

        for task_name, config in tasks_config.items():
            # Replace placeholders in description
            description = config['description'].replace('{region}', region)
            description = description.replace('{trip_type}', trip_type)

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

    def run(self, region, trip_type):
        """Execute the travel planner crew workflow."""
        print(f"🌍 Starting YAML-based Travel Planner Crew")
        print(f"📍 Region: {region}")
        print(f"🎯 Trip Type: {trip_type}")
        print("=" * 60)

        # Create agents and tasks from YAML
        agents = self.create_agents_from_yaml()
        tasks = self.create_tasks_from_yaml(agents, region, trip_type)

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
        print("🎉 YAML-based Travel Planner Crew workflow completed!")
        print("📋 Check 'trip_plan.txt' for your complete travel plan and budget")

        return result


def main():
    """Main function to run the YAML-based Travel Planner Crew."""
    print("Welcome to the YAML-based Travel Planner Crew! ✈️🌍")
    print("=" * 60)

    # Get user input for region/destination
    region = input("\n🌍 Enter your preferred region/destination (e.g., 'Europe', 'Japan', 'Southeast Asia'):\n> ")

    if not region.strip():
        print("❌ No region provided. Please try again.")
        return

    # Get user input for trip type
    print("\n🎯 Trip Type Options:")
    print("1. Budget-friendly")
    print("2. Luxury")
    print("3. Adventure")
    print("4. Cultural")
    print("5. Other (specify)")

    trip_choice = input("\nSelect trip type (1-5) or enter custom type:\n> ")

    # Map choices to trip types
    trip_types = {
        '1': 'budget-friendly',
        '2': 'luxury',
        '3': 'adventure',
        '4': 'cultural'
    }

    if trip_choice in trip_types:
        trip_type = trip_types[trip_choice]
    elif trip_choice == '5':
        trip_type = input("Enter your custom trip type:\n> ").strip()
    else:
        trip_type = trip_choice.strip()

    if not trip_type:
        print("❌ No trip type provided. Please try again.")
        return

    # Initialize and run the crew
    try:
        travel_planner = YAMLTravelPlannerCrew()
        result = travel_planner.run(region, trip_type)
        print(f"\n✅ Final Result:\n{result}")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("Please check your YAML configuration files and try again.")


if __name__ == "__main__":
    main()
