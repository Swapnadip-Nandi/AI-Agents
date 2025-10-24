"""
Enhanced Main Workflow Entry Point
Uses session-based architecture with async logging and campaign learning
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from workflows.enhanced_campaign_workflow import EnhancedCampaignWorkflow
from shared.session_manager import SessionManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_sample_product() -> dict:
    """Create sample product information."""
    return {
        "name": "Premium Stainless Steel Water Bottle",
        "category": "Kitchen & Dining",
        "description": "A high-quality, insulated water bottle for everyday use",
        "features": [
            "Double-wall vacuum insulation keeps drinks cold for 24 hours",
            "Made from food-grade 18/8 stainless steel",
            "Leak-proof cap with carry handle",
            "BPA-free and dishwasher safe",
            "Available in 6 stylish colors"
        ],
        "benefits": [
            "Stay hydrated throughout the day",
            "Reduce plastic waste with reusable bottle",
            "Keep beverages at perfect temperature",
            "Durable construction for years of use",
            "Easy to clean and maintain"
        ],
        "target_price": "$29.99",
        "cost": "$8.50",
        "target_audience": "Health-conscious individuals, fitness enthusiasts, outdoor adventurers",
        "brand": "HydraMax",
        "unique_features": [
            "Patent-pending temperature lock technology",
            "Ergonomic grip design",
            "Compatible with standard cup holders"
        ],
        "keywords": ["water bottle", "insulated", "stainless steel", "reusable", "eco-friendly"]
    }


def main():
    """Main execution function."""
    
    print("\n" + "="*80)
    print("🚀 ENHANCED ADK MULTI-AGENT SYSTEM")
    print("Powered by Google Agent Development Kit (ADK)")
    print("="*80)
    print("\n✨ New Features:")
    print("   • Session-based execution with unique IDs")
    print("   • Async time-series logging")
    print("   • Long-term memory with campaign learning")
    print("   • Real-time progress tracking")
    print("   • Automatic cleanup after 7 days")
    print("="*80 + "\n")
    
    # Check environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not found - running in demo mode")
        print("   To use real Gemini API, create .env file with your API key\n")
    else:
        print("✅ Gemini API key detected\n")
    
    try:
        # Create product information
        print("📦 Preparing product information...")
        product_info = create_sample_product()
        print(f"   Product: {product_info['name']}")
        print(f"   Category: {product_info['category']}")
        print(f"   Target Price: {product_info['target_price']}\n")
        
        # Initialize session manager
        print("🔧 Initializing session manager...")
        session_manager = SessionManager(
            storage_root="./storage",
            retention_days=7,
            auto_cleanup=True
        )
        
        # Get session statistics
        stats = session_manager.get_session_stats()
        print(f"   Total Sessions: {stats['total_sessions']}")
        print(f"   Completed: {stats['completed']}")
        print(f"   Average Quality Score: {stats['avg_quality_score']:.1f}%\n")
        
        # Initialize enhanced workflow
        print("🚀 Initializing enhanced campaign workflow...\n")
        workflow = EnhancedCampaignWorkflow(
            storage_root="./storage",
            session_manager=session_manager
        )
        
        # Execute workflow
        print("="*80)
        print("EXECUTING CAMPAIGN WORKFLOW")
        print("="*80 + "\n")
        
        results = workflow.execute(product_info)
        
        # Display comprehensive results
        print("\n" + "="*80)
        print("📊 CAMPAIGN RESULTS SUMMARY")
        print("="*80)
        
        session_id = results['session_id']
        campaign_data = results['campaign_results']
        validation = campaign_data['validation_report']
        outputs = results['outputs']
        
        print(f"\n🆔 Session ID: {session_id}")
        print(f"\n📈 Performance Metrics:")
        print(f"   Overall Quality Score: {validation.get('overall_score', 'N/A')}/100")
        print(f"   Campaign Status: {validation.get('status', 'Unknown')}")
        print(f"   Approval Status: {'✅ APPROVED' if validation.get('approval') else '⚠️  NEEDS REVISION'}")
        print(f"   Workflow Duration: {results['workflow_duration']:.2f} seconds")
        
        print(f"\n📁 Generated Outputs:")
        print(f"   JSON Report: {outputs.get('json', 'N/A')}")
        print(f"   Markdown Report: {outputs.get('markdown', 'N/A')}")
        
        # Display listing summary
        listing = campaign_data.get('amazon_listing', {})
        if listing:
            print(f"\n📝 Amazon Listing:")
            print(f"   Title: {listing.get('title', 'N/A')[:60]}...")
            print(f"   Bullet Points: {len(listing.get('bullet_points', []))} items")
            print(f"   Description Length: {len(listing.get('description', ''))} characters")
        
        # Display social campaigns
        social = campaign_data.get('social_campaigns', {})
        if social:
            platforms = [
                key.replace('_campaign', '').replace('_', ' ').title()
                for key in social.keys()
                if key.endswith('_campaign')
            ]
            print(f"\n📱 Social Media Platforms: {', '.join(platforms)}")
        
        # Display learning info
        if campaign_data.get('learning_suggestions'):
            print(f"\n💡 Campaign Learning: Used similar campaign as reference")
        
        # Display memory statistics
        mem_stats = results.get('memory_stats', {})
        print(f"\n🧠 Memory Statistics:")
        print(f"   Short-term entries: {mem_stats.get('short_term_entries', 0)}")
        print(f"   Long-term entries: {mem_stats.get('longterm_entries', 0)}")
        print(f"   Campaign templates: {mem_stats.get('campaign_templates', 0)}")
        print(f"   Cache size: {mem_stats.get('cache_size', 0)}")
        
        # Display execution metrics
        metrics = results.get('metrics', {})
        print(f"\n⚡ Execution Metrics:")
        print(f"   Agents executed: {metrics.get('agents_executed', 0)}")
        print(f"   Tools called: {metrics.get('tools_called', 0)}")
        print(f"   Memory operations: {metrics.get('memory_operations', 0)}")
        print(f"   Errors: {metrics.get('errors', 0)}")
        
        # Display recommendations
        recommendations = validation.get('recommendations', [])
        if recommendations:
            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec}")
        
        print("\n" + "="*80)
        
        if validation.get('approval'):
            print("✅ CAMPAIGN APPROVED - READY FOR DEPLOYMENT!")
        else:
            print("⚠️  CAMPAIGN NEEDS REVISIONS - REVIEW RECOMMENDATIONS")
        
        print("="*80)
        
        # Next steps
        print("\n📋 Next Steps:")
        print(f"   1. Review results in: ./storage/sessions/{session_id}/results/")
        print(f"   2. Check logs in: ./storage/sessions/{session_id}/logs/")
        print(f"   3. View session manifest: ./storage/sessions/{session_id}/session_manifest.json")
        
        if validation.get('approval'):
            print("   4. Deploy Amazon listing with provided content")
            print("   5. Launch social media campaigns")
            print("   6. Monitor performance metrics")
        else:
            print("   4. Address highlighted issues")
            print("   5. Re-run workflow with improvements")
        
        print("\n🌐 Web Interface:")
        print("   Run 'python adk_web.py' to access the web dashboard")
        print("   View real-time logs and session management\n")
        
        print("✨ Campaign workflow completed successfully!\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
        return 1
    
    except Exception as e:
        print(f"\n\n❌ Workflow failed with error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
