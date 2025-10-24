# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This installs:
- Google GenAI SDK (ADK)
- DuckDuckGo Search (free web search)
- Loguru (logging)
- PyYAML, Pydantic (configuration)
- And other utilities

### Step 2: Configure API Key

1. Copy the example environment file:
```powershell
copy .env.example .env
```

2. Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your free API key:** https://makersuite.google.com/app/apikey

> **Note:** The system works in demo mode without an API key, using simulated agent outputs.

### Step 3: Run the System

```powershell
python main.py
```

That's it! The system will:
1. Load configurations
2. Execute all 6 agents through the workflow
3. Generate campaign outputs
4. Save results to `./storage/results/`

## 📋 What Happens When You Run

```
🚀 Amazon Campaign Multi-Agent System (Google ADK)
================================================================================

Initializing system...
✅ Amazon Campaign System initialized successfully

Using sample product input: Premium Wireless Bluetooth Headphones

🚀 Starting workflow: campaign_20250122_143022
📋 Stage 1: Strategic Planning
🤖 Executing: Lead Planner
🔍 Stage 2: Market Intelligence (Parallel Execution)
🤖 Executing: Market Research Analyst
🤖 Executing: SEO Specialist
✍️ Stage 3: Content Creation
🤖 Executing: Copywriter
📱 Stage 4: Social Media Campaign
🤖 Executing: Social Media Marketer
✅ Stage 5: Quality Validation
🤖 Executing: Quality Validator
Validation Score: 85.5/100
💾 Saved JSON output: storage/results/campaign_20250122_143022.json
💾 Saved Markdown output: storage/results/campaign_20250122_143022.md

================================================================================
✅ Campaign Generation Complete!
================================================================================

Quality Score: 85.5/100
Status: PASSED

Outputs saved to: ./storage/results/
```

## 📁 Output Files

After execution, check `./storage/results/`:

### 1. JSON Output (`campaign_TIMESTAMP.json`)
Complete machine-readable data including:
- Campaign plan
- Market insights
- SEO strategy
- Amazon listing (title, bullets, description)
- Social media campaigns
- Validation report
- Workflow metrics

### 2. Markdown Report (`campaign_TIMESTAMP.md`)
Human-readable executive summary with:
- Campaign overview
- Market research findings
- SEO keywords
- Formatted Amazon listing
- Social media strategy
- Quality scores and recommendations

## 🎯 Sample Output Preview

```markdown
# Amazon Campaign Report: Premium Wireless Bluetooth Headphones

## Product Title
Premium Wireless Bluetooth Headphones - Noise Cancelling | Electronics

## Bullet Points
✓ PREMIUM QUALITY: Active Noise Cancellation (ANC) technology
✓ KEY BENEFIT: Industry-leading 40-hour battery life
✓ VERSATILE USE: Premium leather ear cushions for comfort
✓ CUSTOMER SATISFACTION: Backed by our 100% satisfaction guarantee
✓ TRUSTED BRAND: Join thousands of satisfied customers

## Validation Report
Overall Status: PASSED
Quality Score: 85.5/100
```

## 🔧 Customization

### Change Product Input

Edit `main.py` - function `create_sample_input()`:

```python
def create_sample_input() -> Dict[str, Any]:
    return {
        "product_info": {
            "product_name": "Your Product Name Here",
            "product_category": "Your Category",
            "brand_name": "Your Brand",
            "product_features": [
                "Feature 1",
                "Feature 2",
                "Feature 3"
            ],
            # ... add more details
        }
    }
```

### Adjust Agent Behavior

Edit configuration files in `./config/`:
- `agent_registry.yaml` - Agent roles and capabilities
- `workflow_config.yaml` - Execution flow and timing
- `validator_rules.yaml` - Compliance rules
- `memory_config.yaml` - Memory settings

### Enable/Disable Features

Edit `.env`:
```env
# Enable/disable features
ENABLE_PARALLEL_EXECUTION=true
ENABLE_HALLUCINATION_CHECK=true
ENABLE_CACHE=true
LOG_LEVEL=INFO  # or DEBUG for more details
```

## 🧪 Testing Individual Components

### Test Web Search
```python
from tools.web_search_tool import WebSearchTool

search = WebSearchTool()
results = search.search("amazon marketplace trends")
print(results)
```

### Test Keyword Research
```python
from tools.keyword_research_tool import KeywordResearchTool

kw_tool = KeywordResearchTool()
keywords = kw_tool.generate_keywords("bluetooth headphones", "electronics")
print(keywords)
```

### Test Compliance Checker
```python
from tools.compliance_checker import ComplianceChecker

checker = ComplianceChecker()
result = checker.check_compliance("Your product title here", "title")
print(result)
```

## 📊 Monitoring & Logs

### View Logs
Check `./storage/logs/` for detailed execution logs:
- `amazon_campaign_TIMESTAMP.log` - Full execution log
- `errors/errors_TIMESTAMP.log` - Error-only log

### Memory Snapshots
Check `./storage/memory/` for agent memory states:
- `long_term_memory.json` - Persistent memory
- `checkpoint_*.json` - Workflow checkpoints

## 🐛 Troubleshooting

### Issue: Module Import Errors
**Solution:** Ensure you're in the project directory and Python can find modules:
```powershell
$env:PYTHONPATH = "."
python main.py
```

### Issue: API Key Not Found
**Solution:** Create `.env` file with your Gemini API key:
```powershell
copy .env.example .env
# Edit .env and add your key
```

### Issue: No Outputs Generated
**Solution:** Check `./storage/logs/` for errors. Ensure write permissions.

### Issue: Low Quality Scores
**Solution:** 
1. Check validation report in output
2. Review `validator_rules.yaml` for compliance rules
3. Adjust product input to avoid prohibited claims

## 🎓 Understanding the System

### Agent Responsibilities

1. **Lead Planner** - Strategy and coordination
2. **Market Research** - Competitive intelligence
3. **SEO Specialist** - Keyword optimization
4. **Copywriter** - Content creation
5. **Social Media Marketer** - Campaign design
6. **Quality Validator** - Compliance and accuracy

### Workflow Stages

1. **Planning** - Define objectives and strategy
2. **Research** - Parallel market and SEO analysis
3. **Content** - Generate Amazon listing
4. **Social** - Design social campaigns
5. **Validation** - Check quality and compliance

### Key Features

✅ **Memory** - Agents share context across stages  
✅ **Parallel Execution** - Stage 2 runs concurrently  
✅ **Tool Integration** - 6 tools (2 external, 3 custom, 1 bonus)  
✅ **Hallucination Detection** - Multi-layer validation  
✅ **Structured Output** - JSON + Markdown formats  
✅ **Monitoring** - Complete execution tracking  

## 📚 Next Steps

1. **Customize for your products** - Edit sample input
2. **Integrate real LLM** - Add Gemini API key for actual AI responses
3. **Extend agents** - Add custom logic in agent functions
4. **Add more tools** - Create new tools in `./tools/`
5. **Deploy** - Use in production for real campaigns

## 🤝 Support

For issues or questions:
1. Check logs in `./storage/logs/`
2. Review configuration in `./config/`
3. Refer to Google ADK docs: https://google.github.io/adk-docs/

---

**Ready to create amazing Amazon campaigns? Run `python main.py` now!** 🚀
