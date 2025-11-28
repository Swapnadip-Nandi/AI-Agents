#!/usr/bin/env python3
"""
Assignment 1: Code Assistant Crew (Alternative Version)
A CrewAI implementation without external file writing tools.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "groq/llama3-8b-8192"


def save_to_file(filename: str, content: str):
    """Simple file writing function."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Content saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to {filename}: {e}")


class CodeAssistantCrew:
    def __init__(self):
        pass

    def create_agents(self) -> Dict[str, Agent]:
        """Create and return all agents for the code assistant crew."""

        # Problem Setter Agent
        problem_setter = Agent(
            role='Problem Setter',
            goal='Take user queries and reformulate them into clear, well-defined programming problem statements',
            backstory="""You are an experienced software architect and problem analyst.
            Your expertise lies in understanding vague programming requests and converting them
            into clear, actionable problem statements with specific requirements, constraints,
            and expected outcomes.""",
            verbose=True,
            allow_delegation=False
        )

        # Coder Agent
        coder = Agent(
            role='Python Developer',
            goal='Generate clean, efficient, and well-documented Python code solutions',
            backstory="""You are a senior Python developer with extensive experience in
            algorithm implementation, data structures, and software development best practices.
            You write clean, readable code with proper documentation and follow PEP 8 standards.""",
            verbose=True,
            allow_delegation=False
        )

        # Reviewer Agent
        reviewer = Agent(
            role='Code Reviewer',
            goal='Review code for correctness, readability, optimization, and provide constructive feedback',
            backstory="""You are a senior software engineer and code review specialist.
            You have a keen eye for code quality, performance optimization, security issues,
            and maintainability. You provide detailed, actionable feedback to improve code quality.""",
            verbose=True,
            allow_delegation=False
        )

        return {
            'problem_setter': problem_setter,
            'coder': coder,
            'reviewer': reviewer
        }

    def create_tasks(self, agents: Dict[str, Agent], user_query: str) -> list:
        """Create and return all tasks for the code assistant workflow."""

        # Task 1: Problem Definition
        problem_definition_task = Task(
            description=f"""
            Analyze the user query: "{user_query}"

            Create a comprehensive problem statement that includes:
            1. Clear problem description
            2. Input/output specifications
            3. Constraints and requirements
            4. Expected behavior
            5. Any edge cases to consider

            Make the problem statement specific and actionable for a developer to implement.
            """,
            agent=agents['problem_setter'],
            expected_output="A detailed problem statement with clear requirements and specifications"
        )

        # Task 2: Code Implementation
        code_implementation_task = Task(
            description="""
            Based on the problem statement from the Problem Setter, implement a complete Python solution.

            Requirements:
            1. Write clean, readable Python code
            2. Include proper documentation and comments
            3. Follow PEP 8 coding standards
            4. Include error handling where appropriate
            5. Add example usage/test cases

            Provide the complete code solution with all necessary imports and proper structure.
            The code should be production-ready and well-structured.
            """,
            agent=agents['coder'],
            expected_output="Complete Python code solution with documentation and examples",
            context=[problem_definition_task]
        )

        # Task 3: Code Review
        code_review_task = Task(
            description="""
            Review the generated Python code and provide comprehensive feedback.

            Evaluate the code for:
            1. Correctness and functionality
            2. Code readability and style
            3. Performance and optimization opportunities
            4. Error handling and edge cases
            5. Documentation quality
            6. Best practices adherence

            Provide specific recommendations for improvement and rate the overall code quality.
            Give detailed feedback with examples of improvements.
            """,
            agent=agents['reviewer'],
            expected_output="Detailed code review with specific feedback and recommendations",
            context=[problem_definition_task, code_implementation_task]
        )

        return [problem_definition_task, code_implementation_task, code_review_task]

    def run(self, user_query: str):
        """Execute the code assistant crew workflow."""
        print(f"🚀 Starting Code Assistant Crew for query: '{user_query}'")
        print("=" * 60)

        # Create agents and tasks
        agents = self.create_agents()
        tasks = self.create_tasks(agents, user_query)

        # Create and configure crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        # Execute the crew
        result = crew.kickoff()

        # Save results to files
        if len(tasks) >= 2:
            # Save code solution
            code_result = tasks[1].output if hasattr(tasks[1], 'output') else str(result)
            save_to_file('solution.py', code_result)

        if len(tasks) >= 3:
            # Save review feedback
            review_result = tasks[2].output if hasattr(tasks[2], 'output') else "Review completed"
            save_to_file('review.txt', review_result)

        print("\n" + "=" * 60)
        print("🎉 Code Assistant Crew workflow completed!")
        print("📁 Check 'solution.py' for the generated code")
        print("📝 Check 'review.txt' for the code review feedback")

        return result


def main():
    """Main function to run the Code Assistant Crew."""
    print("Welcome to the Code Assistant Crew! 👨‍💻")
    print("=" * 50)

    # Get user input
    user_query = input("\n🤔 Please describe the programming problem you need help with:\n> ")

    if not user_query.strip():
        print("❌ No query provided. Please try again.")
        return

    # Initialize and run the crew
    try:
        crew_assistant = CodeAssistantCrew()
        result = crew_assistant.run(user_query)
        print(f"\n✅ Final Result:\n{result}")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
