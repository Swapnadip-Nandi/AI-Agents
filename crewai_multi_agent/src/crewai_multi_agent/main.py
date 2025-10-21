#!/usr/bin/env python
import sys
import warnings
import time
from datetime import datetime

from crewai_multi_agent.crew import CrewaiMultiAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the E-commerce Product Launch Campaign crew with retry logic.
    """
    # Example: Smart Home Device Campaign
    inputs = {
        'product_name': 'SmartHub Pro 360',
        'product_category': 'Smart Home Devices',
        'current_date': datetime.now().strftime("%B %d, %Y")
    }
    
    print("=" * 80)
    print("AMAZON PRODUCT LAUNCH CAMPAIGN - MULTI-AGENT SYSTEM")
    print("=" * 80)
    print(f"\nProduct: {inputs['product_name']}")
    print(f"Category: {inputs['product_category']}")
    print(f"Campaign Date: {inputs['current_date']}")
    print("\nInitializing 6-Agent Workflow:")
    print("  1. Lead Planner - Campaign Strategy")
    print("  2. Market Researcher - Market Intelligence")
    print("  3. SEO Specialist - Keyword Optimization")
    print("  4. Copywriter - Content Creation")
    print("  5. Social Media Marketer - Social Campaign")
    print("  6. Critic/Validator - Quality Assurance")
    print("\n" + "=" * 80 + "\n")

    max_retries = 3
    retry_delay = 20  # ✓ Increased from 10 to 20 seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                # Add extra delay before retries to let API recover
                wait_time = retry_delay * attempt  # Exponential backoff: 20s, 40s, 60s
                print(f"⏳ Waiting {wait_time} seconds before retry attempt {attempt}...")
                time.sleep(wait_time)
            
            print(f"🚀 Starting crew execution (Attempt {attempt}/{max_retries})...")
            result = CrewaiMultiAgent().crew().kickoff(inputs=inputs)
            
            print("\n" + "=" * 80)
            print("✅ CAMPAIGN GENERATION COMPLETE!")
            print("=" * 80)
            print("\nOutputs generated:")
            print("  ✓ campaign_validation_report.md")
            print("  ✓ amazon_campaign_final_report.md")
            print("\nCheck the files above for complete campaign materials.")
            print("=" * 80 + "\n")
            
            return result
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Execution interrupted by user.")
            sys.exit(0)
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Error on attempt {attempt}: {error_msg}")
            
            # Check if it's a rate limit or overload error
            if "503" in error_msg or "overloaded" in error_msg.lower() or "rate limit" in error_msg.lower():
                if attempt < max_retries:
                    wait_time = retry_delay * attempt  # Exponential backoff
                    print(f"⏳ API overloaded. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"\n❌ Max retries reached. API is consistently overloaded.")
                    print("💡 Suggestions:")
                    print("  1. Wait 5-10 minutes and try again")
                    print("  2. Use a different model in .env (e.g., gemini-1.5-pro-latest)")
                    print("  3. Check your API quota at https://console.cloud.google.com")
                    raise
            else:
                # For other errors, print and raise immediately
                print(f"\n❌ Fatal error: {e}")
                raise

    print("\n❌ All retry attempts failed.")
    sys.exit(1)



def run_kitchen_appliance():
    """
    Run campaign for Kitchen Appliance category.
    """
    inputs = {
        'product_name': 'UltraClean Robot Vacuum X5',
        'product_category': 'Kitchen & Home Appliances',
        'current_date': datetime.now().strftime("%B %d, %Y")
    }
    
    print(f"\nLaunching campaign for: {inputs['product_name']}")
    print(f"Category: {inputs['product_category']}\n")

    try:
        result = CrewaiMultiAgent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run_electronics():
    """
    Run campaign for Electronics category.
    """
    inputs = {
        'product_name': 'SoundWave Pro Wireless Headphones',
        'product_category': 'Electronics & Accessories',
        'current_date': datetime.now().strftime("%B %d, %Y")
    }
    
    print(f"\nLaunching campaign for: {inputs['product_name']}")
    print(f"Category: {inputs['product_category']}\n")

    try:
        result = CrewaiMultiAgent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'product_name': 'SmartHub Pro 360',
        'product_category': 'Smart Home Devices',
        'current_date': datetime.now().strftime("%B %d, %Y")
    }
    
    try:
        CrewaiMultiAgent().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiMultiAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'product_name': 'SmartHub Pro 360',
        'product_category': 'Smart Home Devices',
        'current_date': datetime.now().strftime("%B %d, %Y")
    }

    try:
        CrewaiMultiAgent().crew().test(
            n_iterations=int(sys.argv[1]), 
            eval_llm=sys.argv[2], 
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Extract product info from trigger or use defaults
    inputs = {
        "crewai_trigger_payload": trigger_payload,
        'product_name': trigger_payload.get('product_name', 'SmartHub Pro 360'),
        'product_category': trigger_payload.get('product_category', 'Smart Home Devices'),
        'current_date': datetime.now().strftime("%B %d, %Y")
    }

    try:
        result = CrewaiMultiAgent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


if __name__ == "__main__":
    """
    Run the default campaign when executing the script directly.
    """
    run()

