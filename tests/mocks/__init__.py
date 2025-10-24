"""
Mock data and responses for testing

Provides mock API responses and test data for unit tests.
"""

# Mock product data
MOCK_PRODUCT = {
    "name": "Premium Water Bottle",
    "category": "Kitchen & Dining",
    "description": "A high-quality insulated water bottle",
    "features": [
        "Double-wall insulation",
        "Stainless steel construction",
        "Leak-proof design"
    ],
    "benefits": [
        "Keeps drinks cold for 24 hours",
        "Durable and long-lasting",
        "Easy to clean"
    ],
    "target_price": "$29.99",
    "cost": "$8.50"
}

# Mock market research data
MOCK_MARKET_ANALYSIS = {
    "market_size": "$500M+",
    "growth_rate": "15% YoY",
    "trends": [
        "Eco-friendly products",
        "Health consciousness",
        "Sustainability focus"
    ],
    "opportunities": [
        "Premium segment underserved",
        "Growing demand for reusable items"
    ]
}

# Mock keyword data
MOCK_KEYWORDS = {
    "primary_keywords": [
        {"keyword": "water bottle", "search_volume": "50000", "competition": "high"},
        {"keyword": "insulated bottle", "search_volume": "30000", "competition": "medium"}
    ],
    "secondary_keywords": [
        {"keyword": "stainless steel bottle", "search_volume": "20000", "competition": "medium"}
    ]
}

# Mock listing content
MOCK_LISTING = {
    "title": "Premium Insulated Water Bottle - Stainless Steel, 24oz",
    "bullet_points": [
        "KEEPS DRINKS COLD: Double-wall insulation keeps beverages cold for 24 hours",
        "DURABLE CONSTRUCTION: Made from premium 18/8 stainless steel",
        "LEAK-PROOF DESIGN: Secure cap prevents spills and leaks",
        "ECO-FRIENDLY: Reusable design reduces plastic waste",
        "EASY CLEANING: Dishwasher safe for convenient maintenance"
    ],
    "description": "Premium insulated water bottle designed for active lifestyles..."
}

# Mock API responses
MOCK_WEB_SEARCH_RESULTS = [
    {
        "title": "Best Water Bottles 2025",
        "url": "https://example.com/review",
        "snippet": "Top rated water bottles for fitness enthusiasts..."
    }
]

MOCK_COMPLIANCE_RESULT = {
    "compliant": True,
    "score": 95,
    "violations": [],
    "warnings": []
}

MOCK_VALIDATION_REPORT = {
    "overall_score": 85,
    "status": "Good",
    "approval": True,
    "recommendations": []
}
