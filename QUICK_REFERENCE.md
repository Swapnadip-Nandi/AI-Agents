# Quick Reference - Enhanced Features

## 🚀 Quick Start

```bash
# 1. Setup
python setup_enhanced.py

# 2. Run workflow (CLI)
python main_enhanced.py

# 3. Start web interface
python adk_web.py
# Then open: http://localhost:8000
```

---

## 📋 Key Concepts

### Session ID
Every workflow execution gets a unique UUID:
```
a7d60252-2537-46d5-b2e6-5498ca6082cb
```

### Storage Structure
```
storage/sessions/<session-uuid>/
  ├── logs/session_timeseries.jsonl    # All events
  ├── logs/agent_<id>.jsonl            # Per-agent
  ├── memory/                          # Session memory
  ├── results/                         # JSON + Markdown
  └── session_manifest.json            # Metadata
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/start` | POST | Start new workflow |
| `/api/sessions` | GET | List all sessions |
| `/api/status?session_id=X` | GET | Get session status |
| `/api/session/X/logs` | GET | Get session logs |
| `/api/session/X/stream` | GET | Stream logs (SSE) |
| `/api/session/X/progress` | GET | Get progress |
| `/api/cleanup` | POST | Cleanup old sessions |
| `/api/agents` | GET | List available agents |

---

## 💾 Memory Types

| Type | Scope | Duration | Use Case |
|------|-------|----------|----------|
| **short_term** | Agent | Session | Current workflow context |
| **long_term** | System | Persistent | Historical data, templates |
| **working** | Agent | Task | Temporary calculations |
| **shared** | Global | Workflow | Agent collaboration |

```python
# Store
memory.store(agent_id, "key", value, memory_type="short_term")

# Retrieve
value = memory.retrieve(agent_id, "key", memory_type="short_term")

# Learn from past
suggestions = memory.get_learning_suggestions(product_info)
```

---

## 📝 Logging

### Basic Logging
```python
logger.info("Message", agent_id="lead_planner")
logger.error("Error occurred", agent_id="copywriter", error="Details")
logger.success("Task completed", score=95)
```

### Structured Events
```python
logger.agent_started(agent_id, agent_name, task="Description")
logger.agent_completed(agent_id, agent_name, duration_ms=1500)
logger.tool_called(agent_id, tool_name, parameters={})
logger.memory_operation(agent_id, "store", "short_term", "key")
```

### Read Logs
```python
events = logger.read_logs(
    agent_id="copywriter",
    event_type="agent_completed",
    limit=10
)
```

---

## 🧠 Campaign Learning

### Save Template (Automatic for ≥85% score)
```python
template_id = memory.save_campaign_template(
    product_name="Product",
    category="Electronics",
    quality_score=95.0,
    keywords=["keyword1", "keyword2"],
    listing_structure={...},
    social_strategy={...},
    success_metrics={...}
)
```

### Find Similar Campaigns
```python
suggestions = memory.find_similar_campaigns(
    category="Electronics",
    keywords=["wireless", "bluetooth"],
    min_quality_score=85.0,
    limit=5
)

for template, similarity in suggestions:
    print(f"{template.product_name}: {similarity*100}% similar")
```

---

## 📊 Session Management

```python
from shared.session_manager import SessionManager

session_mgr = SessionManager(storage_root="./storage", retention_days=7)

# Create session
session_id = session_mgr.create_session(product_name="Product")

# Update session
session_mgr.update_session(session_id, status="completed", quality_score=95)

# List sessions
sessions = session_mgr.list_sessions(status="completed", limit=10)

# Get statistics
stats = session_mgr.get_session_stats()

# Cleanup old sessions
count = session_mgr.cleanup_old_sessions()
```

---

## 🌊 Real-Time Streaming

### JavaScript (Browser)
```javascript
const eventSource = new EventSource(`/api/session/${sessionId}/stream`);

eventSource.addEventListener('log_event', (e) => {
    const event = JSON.parse(e.data);
    console.log(`[${event.level}] ${event.message}`);
    updateUI(event);
});

eventSource.addEventListener('error', (e) => {
    console.error('Stream error');
    eventSource.close();
});
```

### Python
```python
from shared.realtime_streaming import LogStreamer

streamer = LogStreamer(session_dir)

# Get recent logs
logs = streamer.get_recent_logs(count=50)

# Get summary
summary = streamer.get_log_summary()
```

---

## 📈 Progress Tracking

```python
from shared.realtime_streaming import ProgressTracker

tracker = ProgressTracker(session_id)

# Update stage
tracker.update_stage(stage_index=0, progress=50.0)  # 0-5 for 6 stages

# Get status
status = tracker.get_status()
print(f"Overall: {status['overall_progress']}%")
print(f"Current: {status['current_stage_name']}")
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
GOOGLE_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

### Session Manager
```python
SessionManager(
    storage_root="./storage",
    retention_days=7,      # Cleanup after 7 days
    auto_cleanup=True      # Auto cleanup on init
)
```

### Async Logger
```python
AsyncLogger(
    session_id=session_id,
    session_dir=session_dir,
    buffer_size=1000,      # Queue size
    flush_interval=1.0     # Flush every 1 second
)
```

### Enhanced Memory
```python
EnhancedMemoryManager(
    session_id=session_id,
    session_dir=session_dir,
    storage_root=storage_root,
    enable_caching=True,   # Enable LRU cache
    cache_size=100         # Cache 100 entries
)
```

---

## 🎯 Workflow Execution

```python
from workflows.enhanced_campaign_workflow import EnhancedCampaignWorkflow

workflow = EnhancedCampaignWorkflow(storage_root="./storage")

product_info = {
    "name": "Product Name",
    "category": "Category",
    "target_audience": "Target Audience",
    "keywords": ["keyword1", "keyword2"]
}

results = workflow.execute(product_info)

# Access results
session_id = results['session_id']
quality_score = results['campaign_results']['validation_report']['overall_score']
duration = results['workflow_duration']
metrics = results['metrics']
memory_stats = results['memory_stats']
```

---

## 📦 Directory Structure

```
./
├── shared/
│   ├── session_manager.py         # NEW: Session management
│   ├── async_logger.py            # NEW: Async logging
│   ├── enhanced_memory.py         # NEW: Enhanced memory
│   └── realtime_streaming.py      # NEW: Log streaming
│
├── workflows/
│   └── enhanced_campaign_workflow.py  # NEW: Enhanced workflow
│
├── main_enhanced.py               # NEW: CLI entry point
├── setup_enhanced.py              # NEW: Setup script
├── adk_web.py                     # UPDATED: Web interface
│
├── ENHANCED_FEATURES_GUIDE.md     # NEW: Feature guide
├── IMPLEMENTATION_SUMMARY.md      # NEW: Implementation summary
└── QUICK_REFERENCE.md            # NEW: This file
```

---

## 🐛 Debugging

### Check Session Logs
```bash
# View time-series log
cat storage/sessions/<session-id>/logs/session_timeseries.jsonl | jq

# View agent-specific log
cat storage/sessions/<session-id>/logs/agent_lead_planner.jsonl | jq

# View session manifest
cat storage/sessions/<session-id>/session_manifest.json | jq
```

### Check System Status
```bash
# List all sessions
ls -la storage/sessions/

# Check session index
cat storage/session_index.json | jq

# View templates
cat storage/memory/templates/templates_index.json | jq
```

### Monitor in Real-Time
```bash
# Terminal 1: Run workflow
python main_enhanced.py

# Terminal 2: Tail logs
tail -f storage/sessions/<session-id>/logs/session_timeseries.jsonl | jq
```

---

## ⚡ Performance Tips

1. **Enable Caching** - Reduces memory retrieval time by ~80%
2. **Adjust Buffer Size** - Larger buffer for high-volume logging
3. **Increase Flush Interval** - For better batch writing
4. **Regular Cleanup** - Remove old sessions to save space
5. **Use Session ID** - Always track sessions for debugging

---

## 📚 Common Tasks

### Start a New Campaign
```bash
python main_enhanced.py
```

### View Past Campaigns
```bash
python -c "
from shared.session_manager import SessionManager
sm = SessionManager()
for s in sm.list_sessions(limit=5):
    print(f'{s.session_id}: {s.product_name} - {s.quality_score}%')
"
```

### Clean Up Old Sessions
```bash
python -c "
from shared.session_manager import SessionManager
sm = SessionManager()
count = sm.cleanup_old_sessions()
print(f'Cleaned up {count} sessions')
"
```

### Find Similar Campaigns
```bash
python -c "
from shared.enhanced_memory import EnhancedMemoryManager
from pathlib import Path
memory = EnhancedMemoryManager('test', Path('.'), Path('./storage'))
suggestions = memory.find_similar_campaigns(category='Electronics', limit=3)
for template, score in suggestions:
    print(f'{template.product_name}: {score*100:.1f}%')
"
```

---

## 🎓 Learning Path

1. ✅ Run `setup_enhanced.py` to set up directories
2. ✅ Execute `main_enhanced.py` to see session-based workflow
3. ✅ Check `storage/sessions/<id>/` to see session structure
4. ✅ Run `adk_web.py` to explore web interface
5. ✅ Test real-time log streaming in browser
6. ✅ Review session logs and manifests
7. ✅ Experiment with campaign learning features

---

**Made with ❤️ following industry best practices!**
