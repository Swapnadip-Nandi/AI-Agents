"""
Amazon Campaign Multi-Agent System - Main Entry Point

This is the main orchestrator that uses the CampaignWorkflow to execute
the complete Amazon campaign creation process.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from shared.logger import Logger
from shared.memory_manager import MemoryManager
from workflows.campaign_workflow import CampaignWorkflow


def create_sample_product() -> Dict[str, Any]:
    """
    Create sample product information for demonstration.
    
    Returns:
        Sample product data
    """
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
        ]
    }


def main():
    """Main execution function."""
    
    # Initialize logger
    logger = Logger()
    
    logger.info("=" * 80)
    logger.info("AMAZON CAMPAIGN MULTI-AGENT SYSTEM")
    logger.info("Powered by Google Agent Development Kit (ADK)")
    logger.info("=" * 80)
    
    # Check environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_API_KEY not found - running in demo mode")
        logger.info("To use real Gemini API, create .env file with your API key")
    else:
        logger.success("Gemini API key detected")
    
    try:
        # Create product information
        logger.info("\nPreparing product information...")
        product_info = create_sample_product()
        logger.info(f"Product: {product_info['name']}")
        logger.info(f"Category: {product_info['category']}")
        logger.info(f"Target Price: {product_info['target_price']}")
        
        # Initialize memory manager
        logger.info("\nInitializing memory system...")
        memory_manager = MemoryManager()
        
        # Initialize campaign workflow
        logger.info("Initializing campaign workflow...")
        campaign_workflow = CampaignWorkflow(
            memory_manager=memory_manager,
            logger=logger
        )
        
        # Execute workflow
        logger.info("\nExecuting campaign workflow...\n")
        results = campaign_workflow.execute(product_info)
        
        # Display results summary
        logger.info("\n" + "=" * 80)
        logger.info("CAMPAIGN RESULTS SUMMARY")
        logger.info("=" * 80)
        
        campaign_data = results.get("campaign_results", {})
        validation = campaign_data.get("validation_report", {})
        outputs = results.get("outputs", {})
        
        logger.info(f"\n📊 Quality Score: {validation.get('overall_score', 'N/A')}/100")
        logger.info(f"📈 Status: {validation.get('status', 'Unknown')}")
        logger.info(f"✅ Approved: {'YES' if validation.get('approval') else 'NO'}")
        logger.info(f"⏱️  Duration: {results.get('workflow_duration', 0):.2f} seconds")
        
        logger.info(f"\n📁 Outputs Generated:")
        logger.info(f"   JSON: {outputs.get('json', 'N/A')}")
        logger.info(f"   Markdown: {outputs.get('markdown', 'N/A')}")
        
        # Display listing summary
        listing = campaign_data.get("amazon_listing", {})
        if listing:
            logger.info(f"\n📝 Amazon Listing:")
            logger.info(f"   Title Length: {len(listing.get('title', ''))} chars")
            logger.info(f"   Bullet Points: {len(listing.get('bullet_points', []))} items")
            logger.info(f"   Description Length: {len(listing.get('description', ''))} chars")
        
        # Display social campaigns summary
        social = campaign_data.get("social_campaigns", {})
        if social:
            platforms = [
                key.replace('_campaign', '').title()
                for key in social.keys()
                if key.endswith('_campaign')
            ]
            logger.info(f"\n📱 Social Media Platforms: {', '.join(platforms)}")
        
        # Display recommendations if any
        recommendations = validation.get("recommendations", [])
        if recommendations:
            logger.info(f"\n💡 Recommendations ({len(recommendations)}):")
            for i, rec in enumerate(recommendations[:5], 1):
                logger.info(f"   {i}. {rec}")
            if len(recommendations) > 5:
                logger.info(f"   ... and {len(recommendations) - 5} more")
        
        logger.info("\n" + "=" * 80)
        
        if validation.get("approval"):
            logger.success("✅ CAMPAIGN APPROVED - READY FOR DEPLOYMENT!")
        else:
            logger.warning("⚠️  CAMPAIGN NEEDS REVISIONS - REVIEW RECOMMENDATIONS")
        
        logger.info("=" * 80)
        
        # Next steps
        logger.info("\n📋 Next Steps:")
        if validation.get("approval"):
            logger.info("   1. Review the generated outputs in ./storage/results/")
            logger.info("   2. Deploy Amazon listing with provided content")
            logger.info("   3. Launch social media campaigns")
            logger.info("   4. Monitor performance metrics")
        else:
            logger.info("   1. Review validation report in outputs")
            logger.info("   2. Address highlighted issues")
            logger.info("   3. Re-run workflow with improvements")
        
        logger.info("\n✨ Campaign workflow completed successfully!\n")
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\n\nWorkflow interrupted by user")
        return 1
    
    except Exception as e:
        logger.error(f"\n\n❌ Workflow failed with error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
