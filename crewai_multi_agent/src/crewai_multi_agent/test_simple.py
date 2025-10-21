#!/usr/bin/env python
"""
Simple test to verify LLM connectivity and basic agent functionality
Run this before executing the full crew to ensure everything is configured correctly
"""

import os
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

def test_llm_connection():
    """Test basic LLM connectivity"""
    print("=" * 60)
    print("TESTING LLM CONNECTION")
    print("=" * 60)
    
    model = os.getenv('MODEL', 'gemini/gemini-2.0-flash-001')
    api_key = os.getenv('GEMINI_API_KEY')
    
    print(f"\nModel: {model}")
    print(f"API Key: {'*' * 20}{api_key[-10:] if api_key else 'NOT FOUND'}")
    
    if not api_key:
        print("\n❌ ERROR: GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        print("\n🔄 Initializing LLM...")
        llm = LLM(
            model=model,
            api_key=api_key,
            temperature=0.7,
            max_tokens=1000
        )
        
        print("✓ LLM initialized successfully")
        
        print("\n🔄 Testing simple completion...")
        response = llm.call(
            messages=[{"role": "user", "content": "Say 'Hello! LLM is working correctly.' in one short sentence."}]
        )
        
        print(f"✓ Response received: {response}")
        print("\n" + "=" * 60)
        print("✅ LLM CONNECTION TEST PASSED")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n" + "=" * 60)
        print("❌ LLM CONNECTION TEST FAILED")
        print("=" * 60)
        print("\n💡 Troubleshooting suggestions:")
        print("  1. Check your API key is correct in .env file")
        print("  2. Verify the model name is correct")
        print("  3. Check your Google Cloud quota at https://console.cloud.google.com")
        print("  4. Try switching to a different model (e.g., gemini/gemini-2.0-flash)")
        return False

if __name__ == "__main__":
    import sys
    success = test_llm_connection()
    sys.exit(0 if success else 1)
