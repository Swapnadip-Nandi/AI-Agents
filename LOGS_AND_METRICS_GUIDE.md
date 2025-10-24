# 📊 Logs and Metrics Storage Guide

## 📍 Where Your Time-Series Data is Stored

### 1. **Application Logs** 📋

**Location**: `./storage/logs/`

**Files Generated**:
```
storage/logs/
├── amazon_campaign_20251023_012343.log  ← Main application logs (timestamped)
├── amazon_campaign_20251023_012414.log  ← Each workflow run creates a new file
└── errors/
    ├── errors_20251023_012343.log       ← Separate error logs
    └── errors_20251023_012414.log
```

**What's Logged**:
- ✅ Agent execution start/stop
- 🔧 Tool invocations
- 📊 Workflow stage transitions
- ⚠️ Warnings and errors
- 💾 Memory operations
- 🔄 State changes
- 🎯 Validation results

**Log Format**:
```
2025-10-23 01:24:14.410 | INFO | shared.logger:setup_logger:100 | Logger initialized successfully
2025-10-23 01:24:14.411 | INFO | shared.logger:info:224 | AMAZON CAMPAIGN MULTI-AGENT SYSTEM
```

**Time-Series Data Included**:
- Precise timestamps (millisecond accuracy): `YYYY-MM-DD HH:mm:ss.SSS`
- Log level (INFO, WARNING, ERROR, DEBUG, SUCCESS)
- Source location (file:function:line)
- Contextual messages

---

### 2. **Metrics Reports** 📊

**Location**: `./storage/results/`

**Files Generated**:
```
storage/results/
├── monitoring_report_20251023_012345.json    ← Workflow metrics (JSON)
├── monitoring_report_20251023_015623.json
└── amazon_listing_20251023_012345.json        ← Final outputs
```

**Metrics Tracked** (when workflow completes successfully):

#### Workflow-Level Metrics:
```json
{
  "workflow_summary": {
    "workflow_id": "campaign_workflow_abc123",
    "total_execution_time": 45.67,
    "started_at": "2025-10-23T01:24:14.410000",
    "ended_at": "2025-10-23T01:25:00.080000",
    "agents_executed": 6,
    "stages_completed": 4,
    "parallel_executions": 2,
    "total_tokens_used": 12500,
    "total_api_calls": 15,
    "total_tool_calls": 8,
    "total_errors": 0,
    "success": true
  }
}
```

#### Agent-Level Metrics:
```json
{
  "agent_performance": [
    {
      "agent_id": "market_research_analyst_001",
      "agent_name": "Market Research Analyst",
      "execution_time": 8.45,
      "started_at": "2025-10-23T01:24:15.000000",
      "ended_at": "2025-10-23T01:24:23.450000",
      "metrics": {
        "token_usage": 2500,
        "api_calls": 3,
        "tool_invocations": 2,
        "retry_count": 0
      },
      "tool_calls_count": 2,
      "error_count": 0,
      "success": true
    }
  ]
}
```

#### Stage Timing Data:
```json
{
  "stage_durations": {
    "research_phase": {
      "name": "Market Research & Analysis",
      "duration": 15.23
    },
    "content_creation": {
      "name": "Content Generation",
      "duration": 12.45
    }
  }
}
```

#### Event Timeline (Time-Series):
```json
{
  "events": [
    {
      "type": "workflow_started",
      "timestamp": "2025-10-23T01:24:14.410000",
      "data": {"workflow_id": "campaign_workflow_abc123"}
    },
    {
      "type": "stage_started",
      "timestamp": "2025-10-23T01:24:15.000000",
      "data": {"stage_id": "research_phase", "stage_name": "Market Research & Analysis"}
    },
    {
      "type": "parallel_execution",
      "timestamp": "2025-10-23T01:24:20.000000",
      "data": {"agent_count": 2, "duration": 8.5}
    }
  ]
}
```

---

### 3. **Memory Persistence** 💾

**Location**: `./storage/memory/`

**Files Generated**:
```
storage/memory/
├── lead_planner/
│   ├── short_term_memory.json
│   ├── long_term_memory.json
│   └── working_memory.json
├── market_research_analyst/
│   ├── short_term_memory.json
│   └── ...
└── ...
```

**What's Stored**:
- Agent-specific context and learnings
- Shared data between agents
- Historical campaign data
- Performance patterns

---

### 4. **Cache Data** 📦

**Location**: `./storage/cache/`

**Purpose**:
- API response caching
- Tool result caching
- Reduces redundant API calls

---

## 🔍 How to View Your Time-Series Data

### Option 1: Use the Log Viewer (Recommended)

```bash
# View comprehensive summary
python view_logs.py
```

**What You'll See**:
- 📋 List of all log files with timestamps
- 📊 Time-series analysis (events per minute, agent activities)
- 🔍 Latest log entries (colorized by level)
- 📈 Metrics report summary
- ❌ Error tracking

### Option 2: Direct File Access

```bash
# View latest log
Get-Content storage/logs/amazon_campaign_*.log | Select-Object -Last 50

# View all error logs
Get-Content storage/logs/errors/errors_*.log

# View latest metrics report
Get-Content storage/results/monitoring_report_*.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Option 3: Programmatic Access

```python
from view_logs import LogViewer

viewer = LogViewer()

# List all logs
log_files = viewer.list_log_files()

# Analyze time-series data
analysis = viewer.analyze_log_time_series()
print(f"Total entries: {analysis['total_entries']}")
print(f"Duration: {analysis['time_range']['duration_seconds']}s")
print(f"Agent activities: {analysis['agent_activities']}")

# View metrics
viewer.view_metrics_report()
```

---

## 📈 Time-Series Data Points Captured

### 1. **Execution Timeline**
- Workflow start/end times
- Agent execution periods
- Stage durations
- Tool invocation timing
- API call latency

### 2. **Resource Usage Over Time**
- Token consumption per agent
- API call frequency
- Memory operations
- Cache hit/miss rates

### 3. **Performance Metrics**
- Execution time trends
- Parallel execution efficiency
- Retry counts and patterns
- Error frequency

### 4. **Event Stream**
- Log level distribution over time
- Events per minute
- Agent activity patterns
- Tool usage patterns

---

## 📊 Sample Log Analysis Output

When you run `python view_logs.py`, you'll see:

```
================================================================================
📈 TIME SERIES DATA SUMMARY
================================================================================

📋 Log Files Available: 4

Recent Log Files:
   1. amazon_campaign_20251023_012414.log (2.15 KB) - 2025-10-23 01:24:14
   2. errors_20251023_012414.log (0.77 KB) - 2025-10-23 01:24:14
   3. amazon_campaign_20251023_012343.log (2.15 KB) - 2025-10-23 01:23:43
   4. errors_20251023_012343.log (0.78 KB) - 2025-10-23 01:23:43

--------------------------------------------------------------------------------
📊 Latest Log Analysis:
--------------------------------------------------------------------------------

File: amazon_campaign_20251023_012414.log
Total Entries: 15
Time Range: 2025-10-23T01:24:14.410000 to 2025-10-23T01:24:14.477000
Duration: 0.07s

Log Levels:
   ERROR: 2
   INFO: 12
   WARNING: 1

Agent Activities:
   Market Research Analyst: 1 executions
   SEO Specialist: 1 executions
   Copywriter: 1 executions

Tool Calls: 8

❌ Errors: 2
```

---

## 🎯 Log Rotation and Retention

**Configured in**: `config/logging.yaml`

```yaml
file:
  rotation:
    enabled: true
    max_size_mb: 10           # Rotate when file reaches 10 MB
    max_files: 10             # Keep last 10 files
    compress_old: true        # Compress rotated files to .zip
```

**How It Works**:
1. New log file created for each workflow run with timestamp
2. When file reaches 10 MB, it's rotated
3. Old files are compressed to `.zip`
4. Only last 10 files are kept

---

## 💡 Tips for Analyzing Time-Series Data

### 1. **Track Performance Trends**
```bash
# Compare execution times across multiple runs
python view_logs.py > logs_summary.txt
# Review stage_durations in metrics reports
```

### 2. **Identify Bottlenecks**
- Look for agents with longest execution_time
- Check tool_calls_count for excessive tool usage
- Review parallel_executions for optimization opportunities

### 3. **Monitor Error Patterns**
- Track error_count per agent over time
- Analyze error timestamps for patterns
- Review error logs for common failure modes

### 4. **Optimize Resource Usage**
- Monitor total_tokens_used trends
- Track api_calls frequency
- Analyze cache hit rates

---

## 📝 Quick Reference

| Data Type | Location | Format | Retention |
|-----------|----------|--------|-----------|
| Application Logs | `storage/logs/*.log` | Text (loguru format) | 10 files @ 10MB each |
| Error Logs | `storage/logs/errors/*.log` | Text (loguru format) | 10 files @ 10MB each |
| Metrics Reports | `storage/results/*.json` | JSON | Unlimited |
| Memory Data | `storage/memory/*/*.json` | JSON | Persistent |
| Cache | `storage/cache/` | Various | Session-based |

---

## 🚀 Next Steps

1. **Generate More Logs**: Run workflows to populate storage
   ```bash
   python main_workflow.py
   ```

2. **Analyze Trends**: Use the log viewer
   ```bash
   python view_logs.py
   ```

3. **Export Data**: Metrics reports are already in JSON for easy analysis
   ```bash
   python -c "import json; print(json.dumps(json.load(open('storage/results/monitoring_report_*.json')), indent=2))"
   ```

4. **Build Dashboards**: Parse JSON metrics for visualization tools

---

## ⚙️ Configuration

Edit `config/logging.yaml` to customize:

```yaml
logging:
  handlers:
    file:
      path: "./storage/logs"           # Change log directory
      level: "DEBUG"                    # Set log level
      rotation:
        max_size_mb: 10                 # File size before rotation
        max_files: 10                   # Number of files to keep
```

---

**Your time-series data is fully instrumented and ready for analysis! 🎉**
