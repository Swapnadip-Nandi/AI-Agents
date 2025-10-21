# CrewAI Multi-Agent System - Complete User Guide

## 📋 PART 1: HOW TO RUN THE SYSTEM (Step-by-Step Terminal Commands)

### Prerequisites
- Windows PowerShell
- Python 3.13+ installed
- Virtual environment already set up at: `D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai-venv`
- API key configured in `.env` file

---

### Option 1: Quick Run (Recommended)

```powershell
# Step 1: Navigate to the project source directory
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"

# Step 2: Run the multi-agent system
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main
```

**Expected Duration:** 10-15 minutes  
**Output Files Location:** `D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src\`
- `amazon_campaign_final_report.md`
- `campaign_validation_report.md`

---

### Option 2: Test Connection First (Recommended for First Run)

```powershell
# Step 1: Navigate to source directory
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"

# Step 2: Test LLM connection (takes ~5 seconds)
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" crewai_multi_agent/test_simple.py

# Step 3: If test passes, run the full system
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main
```

---

### Option 3: Run with Different Product Categories

#### For Kitchen Appliance:
```powershell
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"

# Edit main.py to use run_kitchen_appliance() instead of run()
# Then execute:
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main
```

#### For Electronics:
```powershell
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"

# Edit main.py to use run_electronics() instead of run()
# Then execute:
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main
```

---

### Monitoring Execution

The system will display real-time progress:

```
✓ Primary LLM initialized: gemini/gemini-2.5-flash
================================================================================
AMAZON PRODUCT LAUNCH CAMPAIGN - MULTI-AGENT SYSTEM
================================================================================

Product: SmartHub Pro 360
Category: Smart Home Devices
Campaign Date: October 21, 2025

Initializing 6-Agent Workflow:
  1. Lead Planner - Campaign Strategy
  2. Market Researcher - Market Intelligence
  3. SEO Specialist - Keyword Optimization
  4. Copywriter - Content Creation
  5. Social Media Marketer - Social Campaign
  6. Critic/Validator - Quality Assurance

================================================================================

🚀 Starting crew execution (Attempt 1/3)...
📋 Task: planning_task - Status: Executing Task...
🔧 Tool: Web Search Tool - Used
✅ Task completed
```

---

### Verifying Success

```powershell
# Check if output files were created
dir "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src\*.md"

# View the final report
notepad "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src\amazon_campaign_final_report.md"

# View the validation report
notepad "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src\campaign_validation_report.md"
```

---

### Troubleshooting Commands

#### If you get API errors:
```powershell
# Wait 30 seconds and retry
timeout /t 30
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main
```

#### Check API connectivity:
```powershell
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -c "import google.generativeai as genai; genai.configure(api_key='YOUR_API_KEY'); print('API Connected'); print([m.name for m in genai.list_models()][:5])"
```

#### View .env configuration:
```powershell
type "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\.env"
```

---

### Clean Up Old Output Files (Before New Run)

```powershell
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"

# Delete old output files
del amazon_campaign_final_report.md
del campaign_validation_report.md

# Confirm deletion
dir *.md
```

---

### Running Multiple Times (Future Use)

#### Run 1 (Smart Home Device - Default):
```powershell
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main

# Rename output files to preserve them
ren amazon_campaign_final_report.md smart_home_campaign.md
ren campaign_validation_report.md smart_home_validation.md
```

#### Run 2 (Kitchen Appliance):
```powershell
cd "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\src"

# Edit main.py: Change line 187 from run() to run_kitchen_appliance()
# Then execute:
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" -m crewai_multi_agent.main

# Rename output files
ren amazon_campaign_final_report.md kitchen_campaign.md
ren campaign_validation_report.md kitchen_validation.md
```

---

### System Requirements Check

```powershell
# Check Python version (should be 3.13+)
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/python.exe" --version

# Check installed packages
& "D:/Practice Lab-AI-Agent/Programming Assignment/CrewAI-multi-agent/crewai-venv/Scripts/pip.exe" list | Select-String "crewai"

# Verify API key is set
$env:GEMINI_API_KEY = Get-Content "D:\Practice Lab-AI-Agent\Programming Assignment\CrewAI-multi-agent\crewai_multi_agent\.env" | Select-String "GEMINI_API_KEY"
Write-Host $env:GEMINI_API_KEY
```

---

## 🔑 Key Points for Future Runs

1. **Always run from the `src` directory**
2. **Use the virtual environment Python executable** (not global Python)
3. **Expected runtime: 10-15 minutes** for complete execution
4. **Output files are generated in the `src` directory**
5. **System automatically retries 3 times** if API errors occur
6. **Rate limited to 10 requests/minute** to prevent API overload
7. **All 6 agents work sequentially** with context sharing between tasks

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Model not found" error | Check `.env` file has correct model name: `gemini/gemini-2.5-flash` |
| "API overloaded" error | Wait 1-2 minutes and retry; system will auto-retry 3 times |
| No output files | Check terminal for errors; ensure execution completed successfully |
| Permission denied | Run PowerShell as Administrator |
| Module not found | Ensure you're in the `src` directory and using virtual environment Python |

---

**Last Updated:** October 21, 2025  
**Version:** 1.0  
**Status:** ✅ Fully Operational
