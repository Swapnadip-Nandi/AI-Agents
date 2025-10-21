from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import json
import re
from datetime import datetime


class WebSearchInput(BaseModel):
    """Input schema for WebSearchTool."""
    query: str = Field(..., description="The search query to find information about products, competitors, or market trends.")
    max_results: int = Field(default=5, description="Maximum number of search results to return.")


class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = (
        "Searches the web for information about products, competitors, market trends, and customer reviews. "
        "Use this tool to gather real-time data about Amazon products, pricing, reviews, and competitive landscape. "
        "Returns relevant search results with titles, snippets, and URLs."
    )
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """
        Simulates web search results for e-commerce research.
        In production, this would integrate with DuckDuckGo API or SerpAPI.
        """
        try:
            # Simulated search results based on common e-commerce queries
            results = self._generate_mock_results(query, max_results)
            
            output = f"Search Results for: '{query}'\n"
            output += f"Found {len(results)} relevant results:\n\n"
            
            for idx, result in enumerate(results, 1):
                output += f"{idx}. **{result['title']}**\n"
                output += f"   {result['snippet']}\n"
                output += f"   Source: {result['url']}\n\n"
            
            return output
        except Exception as e:
            return f"Error performing web search: {str(e)}"

    def _generate_mock_results(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Generate mock search results based on query keywords."""
        query_lower = query.lower()
        
        # Smart home / Electronics queries
        if any(word in query_lower for word in ['smart', 'electronics', 'tech', 'gadget', 'device']):
            return [
                {
                    "title": "Top Smart Home Devices 2025 - Amazon Best Sellers",
                    "snippet": "Smart speakers, security cameras, and smart lights dominate the market. Echo Dot 5th Gen leads with 4.7★ rating and 50K+ reviews. Price range: $25-$199.",
                    "url": "amazon.com/best-sellers-smart-home"
                },
                {
                    "title": "Smart Home Market Trends Q4 2025",
                    "snippet": "Market grew 23% YoY. Key trends: AI integration, voice control, energy efficiency. Target demographics: millennials 25-40, tech enthusiasts, homeowners.",
                    "url": "marketresearch.com/smart-home-2025"
                },
                {
                    "title": "Consumer Reviews: Smart Home Devices",
                    "snippet": "Customers prioritize ease of setup (87%), compatibility (82%), and privacy features (76%). Average purchase decision time: 2-3 weeks of research.",
                    "url": "consumerreports.org/smart-home"
                },
                {
                    "title": "Competitor Analysis: Google vs Amazon Smart Devices",
                    "snippet": "Amazon holds 31% market share, Google 28%. Amazon strengths: ecosystem integration, Prime benefits. Pricing: Amazon devices 15-20% lower.",
                    "url": "techcrunch.com/smart-device-competition"
                },
                {
                    "title": "Top Keywords for Smart Home Products",
                    "snippet": "High-volume keywords: 'smart home' (246K/month), 'alexa compatible' (135K), 'voice control' (89K), 'home automation' (67K).",
                    "url": "semrush.com/keywords-smart-home"
                }
            ][:max_results]
        
        # Kitchen / Home appliances
        elif any(word in query_lower for word in ['kitchen', 'appliance', 'cook', 'home', 'vacuum', 'clean']):
            return [
                {
                    "title": "Best Kitchen Appliances 2025 - Amazon Reviews",
                    "snippet": "Air fryers, robot vacuums, and smart blenders top the charts. Robot vacuums: 4.6★ avg rating, $200-$800 price range. 35% growth in smart kitchen category.",
                    "url": "amazon.com/best-kitchen-appliances"
                },
                {
                    "title": "Home Appliance Buyer Personas",
                    "snippet": "Key segments: Busy families (40%), health-conscious cooks (30%), tech early adopters (20%). Age range: 28-55. Household income: $50K-$120K.",
                    "url": "nielsen.com/home-appliance-buyers"
                },
                {
                    "title": "Robot Vacuum Market Analysis 2025",
                    "snippet": "Market size: $4.2B. Popular features: LIDAR mapping (78% prefer), self-emptying (65%), app control (89%). Roborock and iRobot lead market.",
                    "url": "statista.com/robot-vacuum-market"
                },
                {
                    "title": "Customer Pain Points in Kitchen Shopping",
                    "snippet": "Top concerns: durability (91%), warranty (84%), ease of cleaning (79%), noise level (72%). Brand trust influences 68% of purchase decisions.",
                    "url": "consumerinsights.com/kitchen-purchases"
                },
                {
                    "title": "SEO Keywords: Kitchen & Home Products",
                    "snippet": "Top searches: 'air fryer' (368K/month), 'robot vacuum' (201K), 'instant pot' (165K), 'kitchen gadgets' (98K), 'smart appliances' (76K).",
                    "url": "ahrefs.com/kitchen-keywords"
                }
            ][:max_results]
        
        # General e-commerce / Amazon
        elif any(word in query_lower for word in ['amazon', 'ecommerce', 'online', 'shopping', 'product']):
            return [
                {
                    "title": "Amazon Product Launch Best Practices 2025",
                    "snippet": "Successful launches: strong imagery (95% impact), A+ content (73% conversion lift), sponsored ads (60% visibility boost). First 2 weeks critical.",
                    "url": "sellerstrategy.com/launch-guide"
                },
                {
                    "title": "E-commerce Marketing Trends 2025",
                    "snippet": "Video content increases conversion 80%. Social commerce grows 43% YoY. Instagram and TikTok top platforms for product discovery (ages 18-35).",
                    "url": "ecommercenews.com/trends-2025"
                },
                {
                    "title": "Amazon SEO: Ranking Factors 2025",
                    "snippet": "Key factors: keywords in title (weight: 35%), bullet points (20%), reviews count/rating (25%), sales velocity (20%). Backend keywords still matter.",
                    "url": "junglescout.com/amazon-seo"
                },
                {
                    "title": "Customer Review Analysis: Amazon Success Factors",
                    "snippet": "Products with 4.5+ stars convert 3x better. Review velocity (10+ reviews/month) boosts ranking. Respond to negative reviews within 24hrs.",
                    "url": "reviewtrackers.com/amazon-reviews"
                },
                {
                    "title": "Competitive Pricing Strategy on Amazon",
                    "snippet": "Dynamic pricing essential. Products priced 5-15% below competitors see 40% more clicks. Prime eligibility increases conversion 32%.",
                    "url": "repricer.com/pricing-strategy"
                }
            ][:max_results]
        
        # Default general results
        else:
            return [
                {
                    "title": f"Market Research: {query}",
                    "snippet": "Comprehensive market analysis showing growth trends, customer demographics, and competitive landscape for the queried product category.",
                    "url": "marketresearch.com/analysis"
                },
                {
                    "title": f"Customer Reviews and Ratings: {query}",
                    "snippet": "Aggregate customer feedback shows high demand for quality, value, and reliability. Average rating expectations: 4.3+ stars for success.",
                    "url": "reviews.com/customer-feedback"
                },
                {
                    "title": f"Competitive Analysis: {query}",
                    "snippet": "Top competitors identified with pricing strategies, market positioning, and unique selling propositions analyzed for strategic insights.",
                    "url": "competitive-intel.com/report"
                }
            ][:max_results]


class SEOKeywordInput(BaseModel):
    """Input schema for SEOKeywordTool."""
    product_category: str = Field(..., description="The product category or niche to find SEO keywords for.")
    focus_keywords: str = Field(default="", description="Optional primary keywords to expand upon.")


class SEOKeywordTool(BaseTool):
    name: str = "SEO Keyword Research Tool"
    description: str = (
        "Analyzes and generates high-value SEO keywords for e-commerce products. "
        "Provides keyword search volume, competition level, and long-tail keyword suggestions. "
        "Use this to optimize product listings, titles, and marketing copy for better discoverability."
    )
    args_schema: Type[BaseModel] = SEOKeywordInput

    def _run(self, product_category: str, focus_keywords: str = "") -> str:
        """
        Generates SEO keyword recommendations.
        In production, this would integrate with Google Keyword Planner, Ahrefs, or SEMrush API.
        """
        try:
            keywords = self._generate_keywords(product_category, focus_keywords)
            
            output = f"SEO Keyword Analysis for: '{product_category}'\n"
            if focus_keywords:
                output += f"Focus Keywords: {focus_keywords}\n"
            output += "=" * 70 + "\n\n"
            
            output += "## Primary Keywords (High Volume, Medium Competition)\n"
            for kw in keywords['primary']:
                output += f"- **{kw['keyword']}** | Search Volume: {kw['volume']}/month | Competition: {kw['competition']}\n"
            
            output += "\n## Long-Tail Keywords (Medium Volume, Low Competition)\n"
            for kw in keywords['long_tail']:
                output += f"- **{kw['keyword']}** | Search Volume: {kw['volume']}/month | Competition: {kw['competition']}\n"
            
            output += "\n## Trending Keywords (Growing Interest)\n"
            for kw in keywords['trending']:
                output += f"- **{kw['keyword']}** | Growth: +{kw['growth']}% | Current Volume: {kw['volume']}/month\n"
            
            output += "\n## Recommendations:\n"
            output += "- Include primary keywords in product title and first bullet point\n"
            output += "- Use long-tail keywords in detailed description and backend search terms\n"
            output += "- Monitor trending keywords for seasonal campaign opportunities\n"
            
            return output
        except Exception as e:
            return f"Error generating SEO keywords: {str(e)}"

    def _generate_keywords(self, category: str, focus: str) -> Dict[str, List[Dict[str, Any]]]:
        """Generate keyword data based on product category."""
        category_lower = category.lower()
        
        # Smart home / Electronics keywords
        if any(word in category_lower for word in ['smart', 'electronics', 'tech', 'gadget']):
            return {
                'primary': [
                    {'keyword': 'smart home device', 'volume': '246,000', 'competition': 'Medium'},
                    {'keyword': 'alexa compatible', 'volume': '135,000', 'competition': 'Medium'},
                    {'keyword': 'voice control', 'volume': '89,000', 'competition': 'Low'},
                    {'keyword': 'home automation', 'volume': '67,000', 'competition': 'Medium'},
                    {'keyword': 'smart speaker', 'volume': '74,000', 'competition': 'High'},
                ],
                'long_tail': [
                    {'keyword': 'best smart home devices for beginners', 'volume': '12,000', 'competition': 'Low'},
                    {'keyword': 'affordable smart home starter kit', 'volume': '8,500', 'competition': 'Low'},
                    {'keyword': 'smart home devices that work with alexa', 'volume': '18,000', 'competition': 'Low'},
                    {'keyword': 'wireless smart home security', 'volume': '9,200', 'competition': 'Low'},
                    {'keyword': 'energy saving smart devices', 'volume': '6,800', 'competition': 'Low'},
                ],
                'trending': [
                    {'keyword': 'AI smart home', 'volume': '22,000', 'growth': '156'},
                    {'keyword': 'matter compatible devices', 'volume': '15,000', 'growth': '203'},
                    {'keyword': 'smart home privacy', 'volume': '11,000', 'growth': '89'},
                ]
            }
        
        # Kitchen / Home appliances keywords
        elif any(word in category_lower for word in ['kitchen', 'appliance', 'cook', 'home', 'vacuum']):
            return {
                'primary': [
                    {'keyword': 'air fryer', 'volume': '368,000', 'competition': 'High'},
                    {'keyword': 'robot vacuum', 'volume': '201,000', 'competition': 'High'},
                    {'keyword': 'kitchen gadgets', 'volume': '98,000', 'competition': 'Medium'},
                    {'keyword': 'smart appliances', 'volume': '76,000', 'competition': 'Medium'},
                    {'keyword': 'home appliances', 'volume': '165,000', 'competition': 'High'},
                ],
                'long_tail': [
                    {'keyword': 'best air fryer for family of 4', 'volume': '14,000', 'competition': 'Low'},
                    {'keyword': 'quiet robot vacuum for pets', 'volume': '9,800', 'competition': 'Low'},
                    {'keyword': 'small kitchen appliances must have', 'volume': '11,500', 'competition': 'Low'},
                    {'keyword': 'dishwasher safe kitchen gadgets', 'volume': '5,600', 'competition': 'Low'},
                    {'keyword': 'robot vacuum with self emptying', 'volume': '16,000', 'competition': 'Low'},
                ],
                'trending': [
                    {'keyword': 'air fryer recipes', 'volume': '89,000', 'growth': '134'},
                    {'keyword': 'smart kitchen appliances', 'volume': '34,000', 'growth': '178'},
                    {'keyword': 'eco friendly appliances', 'volume': '19,000', 'growth': '92'},
                ]
            }
        
        # General e-commerce keywords
        else:
            return {
                'primary': [
                    {'keyword': f'{category} best sellers', 'volume': '45,000', 'competition': 'Medium'},
                    {'keyword': f'{category} reviews', 'volume': '38,000', 'competition': 'Low'},
                    {'keyword': f'buy {category} online', 'volume': '52,000', 'competition': 'High'},
                    {'keyword': f'{category} deals', 'volume': '67,000', 'competition': 'Medium'},
                    {'keyword': f'top rated {category}', 'volume': '29,000', 'competition': 'Low'},
                ],
                'long_tail': [
                    {'keyword': f'best {category} for home use', 'volume': '8,200', 'competition': 'Low'},
                    {'keyword': f'affordable {category} high quality', 'volume': '6,500', 'competition': 'Low'},
                    {'keyword': f'{category} with warranty', 'volume': '4,900', 'competition': 'Low'},
                    {'keyword': f'professional {category} for beginners', 'volume': '7,100', 'competition': 'Low'},
                ],
                'trending': [
                    {'keyword': f'sustainable {category}', 'volume': '12,000', 'growth': '145'},
                    {'keyword': f'smart {category}', 'volume': '18,000', 'growth': '167'},
                ]
            }


class DataAnalysisInput(BaseModel):
    """Input schema for DataAnalysisTool."""
    analysis_type: str = Field(..., description="Type of analysis: 'pricing', 'features', 'reviews', or 'trends'")
    product_data: str = Field(..., description="Product information or data points to analyze")


class DataAnalysisTool(BaseTool):
    name: str = "Product Data Analysis Tool"
    description: str = (
        "Analyzes product data including pricing trends, feature comparisons, review sentiment, and market trends. "
        "Use this to extract insights from product information, identify patterns, and make data-driven recommendations. "
        "Supports analysis types: pricing, features, reviews, trends."
    )
    args_schema: Type[BaseModel] = DataAnalysisInput

    def _run(self, analysis_type: str, product_data: str) -> str:
        """
        Performs data analysis on product information.
        In production, this would use pandas, numpy, and ML libraries for deeper analysis.
        """
        try:
            analysis_type = analysis_type.lower()
            
            if analysis_type == 'pricing':
                return self._analyze_pricing(product_data)
            elif analysis_type == 'features':
                return self._analyze_features(product_data)
            elif analysis_type == 'reviews':
                return self._analyze_reviews(product_data)
            elif analysis_type == 'trends':
                return self._analyze_trends(product_data)
            else:
                return f"Unknown analysis type: {analysis_type}. Supported types: pricing, features, reviews, trends"
                
        except Exception as e:
            return f"Error performing data analysis: {str(e)}"

    def _analyze_pricing(self, data: str) -> str:
        """Analyze pricing strategy and competitive positioning."""
        output = "## Pricing Analysis\n\n"
        output += "**Competitive Price Points:**\n"
        output += "- Budget Tier: $25-$50 (captures 35% of market)\n"
        output += "- Mid-Range: $50-$150 (captures 45% of market, highest conversion)\n"
        output += "- Premium: $150-$300+ (captures 20% of market, higher margins)\n\n"
        
        output += "**Recommendations:**\n"
        output += "- Position at $79-$129 for optimal conversion in mid-range segment\n"
        output += "- Price 10-15% below top competitor to capture price-conscious buyers\n"
        output += "- Offer launch discount: 20% off first 2 weeks to build momentum\n"
        output += "- Bundle pricing: Save 15% when buying 2+ items\n\n"
        
        output += "**Psychological Pricing:**\n"
        output += "- Use .99 or .97 endings (e.g., $79.99 vs $80.00)\n"
        output += "- Show 'Compare at' price to highlight savings\n"
        output += "- Display 'Prime' savings badge for eligible customers\n"
        
        return output

    def _analyze_features(self, data: str) -> str:
        """Analyze product features and competitive advantages."""
        output = "## Feature Analysis\n\n"
        output += "**Must-Have Features (Customer Expectations):**\n"
        output += "1. Easy setup/installation (mentioned in 87% of reviews)\n"
        output += "2. App control/smartphone integration (82% preference)\n"
        output += "3. Voice assistant compatibility (76% for smart products)\n"
        output += "4. Energy efficiency/eco-friendly (71% consideration)\n"
        output += "5. Warranty/customer support (84% decision factor)\n\n"
        
        output += "**Differentiating Features (Competitive Advantages):**\n"
        output += "- AI-powered automation (emerging trend, +167% interest)\n"
        output += "- Multi-device ecosystem integration\n"
        output += "- Premium materials/build quality\n"
        output += "- Extended warranty (2-3 years vs industry 1 year)\n"
        output += "- US-based customer support (24/7 availability)\n\n"
        
        output += "**Feature Prioritization:**\n"
        output += "- Tier 1 (Essential): Easy setup, quality construction, basic functionality\n"
        output += "- Tier 2 (Expected): App control, voice compatibility, good warranty\n"
        output += "- Tier 3 (Delighters): AI features, ecosystem integration, premium support\n"
        
        return output

    def _analyze_reviews(self, data: str) -> str:
        """Analyze customer review patterns and sentiment."""
        output = "## Review Sentiment Analysis\n\n"
        output += "**Overall Sentiment Distribution:**\n"
        output += "- Positive (4-5 stars): 73% of reviews\n"
        output += "- Neutral (3 stars): 15% of reviews\n"
        output += "- Negative (1-2 stars): 12% of reviews\n\n"
        
        output += "**Common Positive Themes:**\n"
        output += "1. 'Easy to use' / 'Simple setup' (mentioned 2,341 times)\n"
        output += "2. 'Great value' / 'Worth the money' (mentioned 1,876 times)\n"
        output += "3. 'Works perfectly' / 'Reliable' (mentioned 1,654 times)\n"
        output += "4. 'Fast shipping' (mentioned 1,203 times)\n\n"
        
        output += "**Common Pain Points (Address in Marketing):**\n"
        output += "1. Confusion during initial setup (8% of reviews) → Create setup video\n"
        output += "2. Compatibility questions (6% of reviews) → Clear compatibility chart\n"
        output += "3. Shipping damage concerns (4% of reviews) → Highlight packaging quality\n\n"
        
        output += "**Review Strategy Recommendations:**\n"
        output += "- Target 100+ reviews in first month (use Early Reviewer Program)\n"
        output += "- Maintain 4.5+ star average for optimal conversion\n"
        output += "- Respond to ALL negative reviews within 24 hours\n"
        output += "- Include review highlights in A+ content\n"
        
        return output

    def _analyze_trends(self, data: str) -> str:
        """Analyze market and seasonal trends."""
        output = "## Market Trends Analysis\n\n"
        output += "**Current Market Trends (2025):**\n"
        output += "1. **AI Integration** → +167% year-over-year interest\n"
        output += "   - Products with 'AI-powered' or 'smart learning' features see 40% higher CTR\n"
        output += "2. **Sustainability** → +145% growth in 'eco-friendly' searches\n"
        output += "   - Eco-certifications increase perceived value by 23%\n"
        output += "3. **Voice Control** → Now expected standard (76% of buyers)\n"
        output += "4. **Video Commerce** → 80% conversion boost with product videos\n\n"
        
        output += "**Seasonal Trends:**\n"
        output += "- Peak Season: Nov-Dec (Black Friday/Cyber Monday, Holiday shopping)\n"
        output += "- Secondary Peak: Jan (New Year resolutions), Sept (Back to school)\n"
        output += "- Current Month (October): Pre-holiday preparation phase\n"
        output += "  * Recommendation: Launch now to build reviews before holiday rush\n\n"
        
        output += "**Emerging Opportunities:**\n"
        output += "- TikTok Shop integration (43% YoY growth in social commerce)\n"
        output += "- Influencer partnerships (micro-influencers: 10K-100K followers)\n"
        output += "- User-generated content campaigns (increases trust by 79%)\n"
        output += "- Subscription/bundle models (34% higher lifetime value)\n"
        
        return output
