"""
Time-Series Data Visualization
Generate simple charts from logs and metrics
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict
import re


def visualize_log_timeline(log_file: Path):
    """Create ASCII timeline visualization from log file."""
    
    print(f"\n{'='*80}")
    print(f"⏱️  LOG TIMELINE: {log_file.name}")
    print(f"{'='*80}\n")
    
    # Parse log entries
    timestamp_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})'
    level_pattern = r'\| ([A-Z]+)\s+\|'
    
    entries = []
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                timestamp_match = re.search(timestamp_pattern, line)
                level_match = re.search(level_pattern, line)
                
                if timestamp_match and level_match:
                    entries.append({
                        'timestamp': datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S.%f'),
                        'level': level_match.group(1).strip(),
                        'message': line.strip()
                    })
    except Exception as e:
        print(f"❌ Error reading log: {e}")
        return
    
    if not entries:
        print("📭 No log entries found")
        return
    
    # Calculate time buckets (100ms intervals)
    start_time = entries[0]['timestamp']
    end_time = entries[-1]['timestamp']
    duration = (end_time - start_time).total_seconds()
    
    print(f"Start: {start_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"End:   {end_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Duration: {duration:.3f} seconds\n")
    
    # Create timeline
    buckets = defaultdict(lambda: {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0, 'SUCCESS': 0})
    
    for entry in entries:
        elapsed = (entry['timestamp'] - start_time).total_seconds()
        bucket = int(elapsed * 10)  # 100ms buckets
        buckets[bucket][entry['level']] += 1
    
    # Display timeline
    print("Timeline (each character = 100ms):")
    print("Legend: . = INFO  ! = WARNING  X = ERROR  ✓ = SUCCESS\n")
    
    timeline = ""
    for i in range(max(buckets.keys()) + 1):
        bucket = buckets.get(i, {})
        
        if bucket.get('ERROR', 0) > 0:
            timeline += 'X'
        elif bucket.get('WARNING', 0) > 0:
            timeline += '!'
        elif bucket.get('SUCCESS', 0) > 0:
            timeline += '✓'
        elif bucket.get('INFO', 0) > 0:
            timeline += '.'
        else:
            timeline += ' '
    
    # Print timeline in chunks of 80 characters
    for i in range(0, len(timeline), 80):
        chunk = timeline[i:i+80]
        time_marker = f"{i * 0.1:.1f}s"
        print(f"{time_marker:>6} |{chunk}")
    
    # Statistics
    print(f"\n{'='*80}")
    print("📊 Statistics:")
    print(f"{'='*80}")
    
    level_counts = Counter(e['level'] for e in entries)
    for level, count in sorted(level_counts.items()):
        emoji = {'INFO': '🔵', 'WARNING': '🟡', 'ERROR': '🔴', 'SUCCESS': '🟢', 'DEBUG': '⚪'}.get(level, '⚫')
        bar = '█' * (count * 50 // len(entries))
        print(f"{emoji} {level:8} {count:4} {bar}")


def visualize_metrics_timeline(metrics_file: Path):
    """Create visualization from metrics report."""
    
    print(f"\n{'='*80}")
    print(f"📊 METRICS TIMELINE: {metrics_file.name}")
    print(f"{'='*80}\n")
    
    try:
        with open(metrics_file, 'r') as f:
            report = json.load(f)
    except Exception as e:
        print(f"❌ Error reading metrics: {e}")
        return
    
    # Workflow summary
    workflow = report.get('workflow_summary', {})
    print(f"Workflow: {workflow.get('workflow_id', 'N/A')}")
    print(f"Duration: {workflow.get('total_execution_time', 0):.2f}s")
    print(f"Status: {'✅ Success' if workflow.get('success') else '❌ Failed'}\n")
    
    # Agent timeline
    agents = report.get('agent_performance', [])
    if agents:
        print("Agent Execution Timeline:")
        print("-" * 80)
        
        # Sort by start time
        sorted_agents = sorted(
            agents,
            key=lambda x: x.get('started_at', '')
        )
        
        # Find earliest start
        start_times = [datetime.fromisoformat(a.get('started_at', '')) for a in sorted_agents if a.get('started_at')]
        if start_times:
            earliest = min(start_times)
            
            for agent in sorted_agents:
                if not agent.get('started_at'):
                    continue
                    
                start = datetime.fromisoformat(agent['started_at'])
                offset = (start - earliest).total_seconds()
                duration = agent.get('execution_time', 0)
                
                # Create bar
                bar_start = int(offset * 2)  # 0.5s per character
                bar_length = max(1, int(duration * 2))
                
                timeline = ' ' * bar_start + '█' * bar_length
                
                status = '✅' if agent.get('success') else '❌'
                name = agent.get('agent_name', 'Unknown')[:30]
                
                print(f"{status} {name:30} |{timeline[:60]}")
                print(f"{'':33} |{offset:6.2f}s → {offset + duration:6.2f}s ({duration:.2f}s)")
    
    # Resource usage over time
    print(f"\n{'='*80}")
    print("💰 Resource Usage:")
    print(f"{'='*80}")
    
    total_tokens = workflow.get('total_tokens_used', 0)
    total_api_calls = workflow.get('total_api_calls', 0)
    total_tool_calls = workflow.get('total_tool_calls', 0)
    
    max_val = max(total_tokens // 100, total_api_calls, total_tool_calls, 1)
    
    print(f"Tokens:     {total_tokens:6,} {'█' * (total_tokens // 100 * 40 // max_val)}")
    print(f"API Calls:  {total_api_calls:6,} {'█' * (total_api_calls * 40 // max_val)}")
    print(f"Tool Calls: {total_tool_calls:6,} {'█' * (total_tool_calls * 40 // max_val)}")
    
    # Events timeline
    events = report.get('events', [])
    if events:
        print(f"\n{'='*80}")
        print(f"📅 Event Timeline ({len(events)} events):")
        print(f"{'='*80}\n")
        
        # Group by type
        event_types = Counter(e['type'] for e in events)
        for event_type, count in sorted(event_types.items()):
            print(f"  {event_type:25} {count:3} {'█' * (count * 40 // len(events))}")


def main():
    """Main visualization."""
    log_dir = Path("./storage/logs")
    results_dir = Path("./storage/results")
    
    print("\n" + "="*80)
    print("📊 TIME-SERIES DATA VISUALIZATION")
    print("="*80)
    
    # Find latest log
    log_files = sorted(log_dir.glob("amazon_campaign_*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if log_files:
        visualize_log_timeline(log_files[0])
    else:
        print("\n📭 No log files found")
    
    # Find latest metrics
    metrics_files = sorted(results_dir.glob("monitoring_report_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if metrics_files:
        visualize_metrics_timeline(metrics_files[0])
    else:
        print("\n📭 No metrics reports found")
    
    print("\n" + "="*80)
    print("💡 Run 'python main_workflow.py' to generate complete metrics with timeline data")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
