#!/usr/bin/env python3
"""
Assignment 2: Travel Planner Crew
A CrewAI implementation for travel planning workflow.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileWriterTool
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "groq/llama3-8b-8192"


class TravelPlannerCrew:
    def __init__(self):
        self.file_writer = FileWriterTool()

    def create_agents(self) -> Dict[str, Agent]:
        """Create and return all agents for the travel planner crew."""

        # Destination Expert Agent
        destination_expert = Agent(
            role='Destination Expert',
            goal='Suggest top destinations based on user preferences and travel type',
            backstory="""You are a seasoned travel expert with extensive knowledge of destinations
            worldwide. You have traveled to over 100 countries and have deep insights into what
            makes each destination special. You excel at matching travelers with perfect destinations
            based on their preferences, budget, and travel style.""",
            verbose=True,
            allow_delegation=False
        )

        # Itinerary Planner Agent
        itinerary_planner = Agent(
            role='Itinerary Planner',
            goal='Create detailed day-by-day travel plans with activities, food, and cultural experiences',
            backstory="""You are a professional travel planner with 15 years of experience creating
            memorable travel experiences. You have expertise in local cultures, must-see attractions,
            hidden gems, authentic food experiences, and optimal travel logistics. You create
            well-balanced itineraries that maximize the travel experience.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.file_writer]
        )

        # Budget Advisor Agent
        budget_advisor = Agent(
            role='Budget Advisor',
            goal='Provide accurate cost estimates and budget breakdowns for travel plans',
            backstory="""You are a financial advisor specializing in travel budgeting. You have
            access to current pricing information for accommodations, transportation, food, and
            activities worldwide. You help travelers understand the true cost of their trips and
            provide practical budget optimization strategies.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.file_writer]
        )

        return {
            'destination_expert': destination_expert,
            'itinerary_planner': itinerary_planner,
            'budget_advisor': budget_advisor
        }

    def create_tasks(self, agents: Dict[str, Agent], region: str, trip_type: str) -> list:
        """Create and return all tasks for the travel planning workflow."""

        # Task 1: Destination Selection
        destination_task = Task(
            description=f"""
            Based on the user's preferences:
            - Preferred region/destination: "{region}"
            - Type of trip: "{trip_type}"

            Suggest 3-5 top destinations that match these criteria. For each destination, provide:
            1. Brief description and why it fits the criteria
            2. Best time to visit
            3. Key highlights and attractions
            4. Suitability for the specified trip type
            5. Any special considerations

            Focus on destinations that offer the best value and experience for the specified trip type.
            """,
            agent=agents['destination_expert'],
            expected_output="List of 3-5 recommended destinations with detailed explanations for each"
        )

        # Task 2: Itinerary Planning
        itinerary_task = Task(
            description="""
            Create a comprehensive 5-day travel itinerary for the recommended destination(s).

            Include for each day:
            1. Morning, afternoon, and evening activities
            2. Recommended restaurants and local food experiences
            3. Cultural experiences and must-see attractions
            4. Transportation between locations
            5. Estimated time for each activity
            6. Alternative options for different weather conditions

            Ensure the itinerary balances planned activities with free time and matches the trip type.
            """,
            agent=agents['itinerary_planner'],
            expected_output="Detailed 5-day itinerary with activities, dining, and cultural experiences",
            context=[destination_task]
        )

        # Task 3: Budget Planning
        budget_task = Task(
            description="""
            Create a comprehensive budget breakdown for the travel plan.

            Provide detailed cost estimates for:
            1. Accommodation (per night and total)
            2. Transportation (flights, local transport)
            3. Food and dining (breakfast, lunch, dinner, snacks)
            4. Activities and attractions (entry fees, tours)
            5. Shopping and miscellaneous expenses
            6. Emergency fund recommendation

            Include:
            - Daily budget breakdown
            - Total trip cost estimate
            - Money-saving tips specific to the destination
            - Payment methods and currency information

            Save the complete travel plan and budget to 'trip_plan.txt'.
            """,
            agent=agents['budget_advisor'],
            expected_output="Complete budget breakdown with cost estimates and money-saving tips saved to trip_plan.txt",
            context=[destination_task, itinerary_task]
        )

        return [destination_task, itinerary_task, budget_task]

    def run(self, region: str, trip_type: str):
        """Execute the travel planner crew workflow."""
        print(f"🌍 Starting Travel Planner Crew")
        print(f"📍 Region: {region}")
        print(f"🎯 Trip Type: {trip_type}")
        print("=" * 60)

        # Create agents and tasks
        agents = self.create_agents()
        tasks = self.create_tasks(agents, region, trip_type)

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
        print("🎉 Travel Planner Crew workflow completed!")
        print("📋 Check 'trip_plan.txt' for your complete travel plan and budget")

        return result


def main():
    """Main function to run the Travel Planner Crew."""
    print("Welcome to the Travel Planner Crew! ✈️🌍")
    print("=" * 50)

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
        travel_planner = TravelPlannerCrew()
        result = travel_planner.run(region, trip_type)
        print(f"\n✅ Final Result:\n{result}")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
