# 📊 Time-Series Data Location Summary

## Quick Answer

**Your logs and metrics are stored in these directories:**

```
D:\Practice Lab-AI-Agent\Programming Assignment\ADK_Draft-2\storage\
├── logs/                    ← ✅ APPLICATION LOGS HERE
│   ├── amazon_campaign_YYYYMMDD_HHMMSS.log
│   └── errors/
│       └── errors_YYYYMMDD_HHMMSS.log
│
├── results/                 ← ✅ METRICS REPORTS HERE
│   └── monitoring_report_YYYYMMDD_HHMMSS.json
│
├── memory/                  ← Agent memory persistence
│   ├── lead_planner/
│   ├── market_research_analyst/
│   └── ...
│
└── cache/                   ← API/tool response cache
```

---

## 🎯 Viewing Your Time-Series Data

### 1. **Quick View - Latest Logs**

```powershell
# View latest log file (last 50 lines)
python view_logs.py
```

**Output includes:**
- 📋 List of all log files with timestamps
- 📊 Time-series analysis (15 entries over 0.067 seconds)
- 🔵 INFO, 🟡 WARNING, 🔴 ERROR counts
- 🤖 Agent activity timeline
- 🔧 Tool call tracking

### 2. **Visual Timeline**

```powershell
# ASCII timeline visualization
python visualize_timeline.py
```

**Shows:**
```
Timeline (each character = 100ms):
Legend: . = INFO  ! = WARNING  X = ERROR  ✓ = SUCCESS

  0.0s |X

📊 Statistics:
🔴 ERROR       2 ██████
🔵 INFO       12 ████████████████████████████████████████
🟡 WARNING     1 ███
```

### 3. **Direct File Access**

```powershell
# View latest log
Get-Content storage\logs\amazon_campaign_*.log | Select-Object -Last 100

# View errors only
Get-Content storage\logs\errors\errors_*.log

# List all logs with timestamps
Get-ChildItem storage\logs\*.log | Sort-Object LastWriteTime -Descending
```

---

## 📈 Currently Available Data

Based on your current runs, you have:

**Log Files**: 4 files
1. `amazon_campaign_20251023_012414.log` (2.15 KB) - 2025-10-23 01:24:14
2. `errors_20251023_012414.log` (0.77 KB) - 2025-10-23 01:24:14
3. `amazon_campaign_20251023_012343.log` (2.15 KB) - 2025-10-23 01:23:43
4. `errors_20251023_012343.log` (0.78 KB) - 2025-10-23 01:23:43

**Time-Series Data Captured**:
- ⏱️ Duration: 0.067 seconds per run
- 📝 15 log entries per run
- 🔵 12 INFO messages
- 🟡 1 WARNING message
- 🔴 2 ERROR messages

---

## 🚀 Generate Complete Metrics

To get full time-series metrics including:
- Agent execution timeline
- Token usage over time
- API call frequency
- Tool invocation patterns
- Stage duration breakdown
- Parallel execution tracking

**Fix the workflow first**, then run:

```powershell
python main_workflow.py
```

This will create:
- ✅ Complete application logs with all agent activities
- ✅ `monitoring_report_YYYYMMDD_HHMMSS.json` with comprehensive metrics
- ✅ Agent performance data
- ✅ Event timeline
- ✅ Resource usage statistics

---

## 📊 Metrics Report Structure (When Generated)

```json
{
  "workflow_summary": {
    "workflow_id": "campaign_workflow_abc123",
    "total_execution_time": 45.67,          ← Time-series: Total duration
    "started_at": "2025-10-23T01:24:14",    ← Time-series: Start timestamp
    "ended_at": "2025-10-23T01:25:00",      ← Time-series: End timestamp
    "agents_executed": 6,
    "total_tokens_used": 12500,             ← Time-series: Token consumption
    "total_api_calls": 15,                  ← Time-series: API frequency
    "total_tool_calls": 8                   ← Time-series: Tool usage
  },
  
  "agent_performance": [                     ← Time-series: Per-agent metrics
    {
      "agent_name": "Market Research Analyst",
      "execution_time": 8.45,
      "started_at": "2025-10-23T01:24:15",
      "ended_at": "2025-10-23T01:24:23",
      "metrics": {
        "token_usage": 2500,
        "api_calls": 3,
        "tool_invocations": 2
      }
    }
  ],
  
  "stage_durations": {                       ← Time-series: Stage timing
    "research_phase": {
      "name": "Market Research & Analysis",
      "duration": 15.23
    }
  },
  
  "events": [                                ← Time-series: Event stream
    {
      "type": "workflow_started",
      "timestamp": "2025-10-23T01:24:14.410",
      "data": {}
    },
    {
      "type": "agent_completed",
      "timestamp": "2025-10-23T01:24:23.450"
    }
  ]
}
```

---

## 🔍 Log File Format

Each log entry contains time-series data:

```
2025-10-23 01:24:14.410 | INFO | shared.logger:setup_logger:100 | Logger initialized
│                       │        │                                 │
│                       │        │                                 └─ Message
│                       │        └─ Source (file:function:line)
│                       └─ Level (INFO, WARNING, ERROR, DEBUG, SUCCESS)
└─ Timestamp (millisecond precision)
```

**Time-Series Fields**:
- **Timestamp**: `YYYY-MM-DD HH:mm:ss.SSS` (millisecond accuracy)
- **Level**: Categorizes event severity
- **Source**: Tracks which component generated the event
- **Message**: Event details (often includes agent names, tool calls, etc.)

---

## 🎯 What Time-Series Data You Can Extract

### From Logs (`storage/logs/*.log`):

1. **Event Timeline**
   - When each event occurred (millisecond precision)
   - Event frequency over time
   - Error occurrence patterns

2. **Agent Activity**
   - Agent start/stop times
   - Agent execution duration
   - Agent interaction patterns

3. **Tool Usage**
   - Tool invocation timestamps
   - Tool execution frequency
   - Tool success/failure rates

4. **System Health**
   - Error rate over time
   - Warning frequency
   - Success rate trends

### From Metrics (`storage/results/*.json`):

1. **Performance Trends**
   - Execution time per workflow run
   - Token consumption over time
   - API call frequency

2. **Resource Utilization**
   - Token usage per agent
   - API calls per stage
   - Tool invocations per workflow

3. **Workflow Efficiency**
   - Stage duration breakdown
   - Parallel execution time savings
   - Bottleneck identification

4. **Quality Metrics**
   - Error count trends
   - Success rate over time
   - Retry pattern analysis

---

## 📁 Complete File Paths

**Application Logs:**
```
D:\Practice Lab-AI-Agent\Programming Assignment\ADK_Draft-2\storage\logs\amazon_campaign_20251023_012414.log
```

**Error Logs:**
```
D:\Practice Lab-AI-Agent\Programming Assignment\ADK_Draft-2\storage\logs\errors\errors_20251023_012414.log
```

**Metrics Reports (when generated):**
```
D:\Practice Lab-AI-Agent\Programming Assignment\ADK_Draft-2\storage\results\monitoring_report_20251023_012414.json
```

**Memory Persistence:**
```
D:\Practice Lab-AI-Agent\Programming Assignment\ADK_Draft-2\storage\memory\{agent_name}\{memory_type}_memory.json
```

---

## 🛠️ Tools Available

| Tool | Purpose | Usage |
|------|---------|-------|
| `view_logs.py` | View and analyze logs | `python view_logs.py` |
| `visualize_timeline.py` | ASCII timeline visualization | `python visualize_timeline.py` |
| Direct file access | Raw log inspection | `Get-Content storage\logs\*.log` |

---

## 💡 Quick Tips

1. **Find Latest Log:**
   ```powershell
   Get-ChildItem storage\logs\*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 1
   ```

2. **Count Log Entries:**
   ```powershell
   (Get-Content storage\logs\amazon_campaign_*.log | Measure-Object -Line).Lines
   ```

3. **Extract Errors Only:**
   ```powershell
   Get-Content storage\logs\*.log | Select-String "ERROR"
   ```

4. **View Metrics in JSON:**
   ```powershell
   Get-Content storage\results\monitoring_report_*.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
   ```

---

## ✅ Summary

✅ **Logs Location**: `storage/logs/`
✅ **Metrics Location**: `storage/results/`
✅ **Viewer Tools**: `view_logs.py`, `visualize_timeline.py`
✅ **Format**: Text logs (loguru) + JSON metrics
✅ **Timestamp Precision**: Milliseconds
✅ **Retention**: 10 files @ 10MB each (configurable)

**All time-series data is automatically captured when you run workflows!** 🎉
