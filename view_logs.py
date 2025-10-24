"""
Log and Metrics Viewer
View time-series data from logs and monitoring reports
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re
from collections import defaultdict


class LogViewer:
    """View and analyze logs and metrics."""
    
    def __init__(self, log_dir: str = "./storage/logs", results_dir: str = "./storage/results"):
        """
        Initialize log viewer.
        
        Args:
            log_dir: Directory containing log files
            results_dir: Directory containing monitoring reports
        """
        self.log_dir = Path(log_dir)
        self.results_dir = Path(results_dir)
        
    def list_log_files(self) -> List[Path]:
        """List all available log files."""
        if not self.log_dir.exists():
            print(f"❌ Log directory not found: {self.log_dir}")
            return []
            
        log_files = list(self.log_dir.glob("amazon_campaign_*.log"))
        error_logs = list(self.log_dir.glob("errors/errors_*.log"))
        
        return sorted(log_files + error_logs, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def list_metrics_reports(self) -> List[Path]:
        """List all monitoring reports."""
        if not self.results_dir.exists():
            print(f"❌ Results directory not found: {self.results_dir}")
            return []
            
        return sorted(
            self.results_dir.glob("monitoring_report_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
    
    def view_latest_log(self, lines: int = 50):
        """
        View the latest log file.
        
        Args:
            lines: Number of lines to display (negative for tail)
        """
        log_files = self.list_log_files()
        
        if not log_files:
            print("📭 No log files found. Run a workflow to generate logs.")
            return
            
        latest_log = log_files[0]
        print(f"\n{'='*80}")
        print(f"📋 Latest Log File: {latest_log.name}")
        print(f"📅 Modified: {datetime.fromtimestamp(latest_log.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Size: {latest_log.stat().st_size / 1024:.2f} KB")
        print(f"{'='*80}\n")
        
        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                content = f.readlines()
                
            if lines < 0:
                # Show last N lines
                display_lines = content[lines:]
            else:
                # Show first N lines
                display_lines = content[:lines]
                
            for line in display_lines:
                # Colorize based on log level
                if 'ERROR' in line:
                    print(f"🔴 {line.strip()}")
                elif 'WARNING' in line:
                    print(f"🟡 {line.strip()}")
                elif 'SUCCESS' in line or '✅' in line:
                    print(f"🟢 {line.strip()}")
                elif 'INFO' in line:
                    print(f"🔵 {line.strip()}")
                else:
                    print(f"   {line.strip()}")
                    
            if len(content) > abs(lines):
                print(f"\n... ({len(content) - abs(lines)} more lines)")
                
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    
    def analyze_log_time_series(self, log_file: Path = None) -> Dict[str, Any]:
        """
        Analyze time-series data from a log file.
        
        Args:
            log_file: Specific log file to analyze (or latest if None)
            
        Returns:
            Time-series analysis dictionary
        """
        if log_file is None:
            log_files = self.list_log_files()
            if not log_files:
                return {}
            log_file = log_files[0]
        
        # Parse log entries
        entries = []
        timestamp_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})'
        level_pattern = r'\| ([A-Z]+)\s+\|'
        
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
            print(f"❌ Error parsing log file: {e}")
            return {}
        
        if not entries:
            return {}
        
        # Analyze time series
        analysis = {
            'file': log_file.name,
            'total_entries': len(entries),
            'time_range': {
                'start': entries[0]['timestamp'].isoformat(),
                'end': entries[-1]['timestamp'].isoformat(),
                'duration_seconds': (entries[-1]['timestamp'] - entries[0]['timestamp']).total_seconds()
            },
            'log_levels': defaultdict(int),
            'events_per_minute': defaultdict(int),
            'agent_activities': defaultdict(int),
            'tool_calls': [],
            'errors': []
        }
        
        for entry in entries:
            # Count log levels
            analysis['log_levels'][entry['level']] += 1
            
            # Events per minute
            minute_key = entry['timestamp'].strftime('%Y-%m-%d %H:%M')
            analysis['events_per_minute'][minute_key] += 1
            
            # Extract agent activities
            if 'Agent Started:' in entry['message']:
                agent_match = re.search(r'Agent Started: (.+?) \(', entry['message'])
                if agent_match:
                    analysis['agent_activities'][agent_match.group(1)] += 1
            
            # Extract tool calls
            if '🔧 Tool Call:' in entry['message']:
                analysis['tool_calls'].append({
                    'timestamp': entry['timestamp'].isoformat(),
                    'message': entry['message']
                })
            
            # Collect errors
            if entry['level'] == 'ERROR':
                analysis['errors'].append({
                    'timestamp': entry['timestamp'].isoformat(),
                    'message': entry['message']
                })
        
        return analysis
    
    def view_metrics_report(self, report_file: Path = None):
        """
        View a monitoring metrics report.
        
        Args:
            report_file: Specific report file (or latest if None)
        """
        if report_file is None:
            reports = self.list_metrics_reports()
            if not reports:
                print("📭 No metrics reports found. Run a workflow with monitoring enabled.")
                return
            report_file = reports[0]
        
        try:
            with open(report_file, 'r') as f:
                report = json.load(f)
            
            print(f"\n{'='*80}")
            print(f"📊 Metrics Report: {report_file.name}")
            print(f"{'='*80}\n")
            
            # Workflow Summary
            workflow = report.get('workflow_summary', {})
            print("🚀 Workflow Summary:")
            print(f"   ID: {workflow.get('workflow_id', 'N/A')}")
            print(f"   Status: {'✅ Success' if workflow.get('success', False) else '❌ Failed'}")
            print(f"   Started: {workflow.get('started_at', 'N/A')}")
            print(f"   Ended: {workflow.get('ended_at', 'N/A')}")
            print(f"   Duration: {workflow.get('total_execution_time', 0):.2f}s")
            print(f"   Agents: {workflow.get('agents_executed', 0)}")
            print(f"   Stages: {workflow.get('stages_completed', 0)}")
            print(f"   Parallel Executions: {workflow.get('parallel_executions', 0)}")
            
            # Resource Usage
            print(f"\n💰 Resource Usage:")
            print(f"   Total Tokens: {workflow.get('total_tokens_used', 0):,}")
            print(f"   API Calls: {workflow.get('total_api_calls', 0)}")
            print(f"   Tool Calls: {workflow.get('total_tool_calls', 0)}")
            print(f"   Errors: {workflow.get('total_errors', 0)}")
            
            # Stage Timings
            stages = workflow.get('stage_durations', {})
            if stages:
                print(f"\n⏱️  Stage Durations:")
                for stage_id, stage_data in stages.items():
                    print(f"   {stage_data['name']}: {stage_data['duration']:.2f}s")
            
            # Agent Performance
            agents = report.get('agent_performance', [])
            if agents:
                print(f"\n🤖 Agent Performance:")
                for agent in agents:
                    status = '✅' if agent.get('success', False) else '❌'
                    print(f"   {status} {agent.get('agent_name', 'Unknown')}: {agent.get('execution_time', 0):.2f}s")
                    print(f"      Tools: {agent.get('tool_calls_count', 0)}, Errors: {agent.get('error_count', 0)}")
            
            # Events Timeline
            events = report.get('events', [])
            if events:
                print(f"\n📅 Events Timeline ({len(events)} events):")
                for event in events[:10]:  # Show first 10
                    print(f"   [{event['timestamp']}] {event['type']}")
                if len(events) > 10:
                    print(f"   ... ({len(events) - 10} more events)")
            
        except Exception as e:
            print(f"❌ Error reading metrics report: {e}")
    
    def generate_time_series_summary(self):
        """Generate a comprehensive time-series summary."""
        print("\n" + "="*80)
        print("📈 TIME SERIES DATA SUMMARY")
        print("="*80 + "\n")
        
        # Log files summary
        log_files = self.list_log_files()
        print(f"📋 Log Files Available: {len(log_files)}")
        
        if log_files:
            print("\nRecent Log Files:")
            for i, log_file in enumerate(log_files[:5], 1):
                size_kb = log_file.stat().st_size / 1024
                modified = datetime.fromtimestamp(log_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"   {i}. {log_file.name} ({size_kb:.2f} KB) - {modified}")
            
            # Analyze latest log
            print("\n" + "-"*80)
            print("📊 Latest Log Analysis:")
            print("-"*80)
            analysis = self.analyze_log_time_series()
            
            if analysis:
                print(f"\nFile: {analysis['file']}")
                print(f"Total Entries: {analysis['total_entries']:,}")
                print(f"Time Range: {analysis['time_range']['start']} to {analysis['time_range']['end']}")
                print(f"Duration: {analysis['time_range']['duration_seconds']:.2f}s")
                
                print(f"\nLog Levels:")
                for level, count in sorted(analysis['log_levels'].items()):
                    print(f"   {level}: {count}")
                
                if analysis['agent_activities']:
                    print(f"\nAgent Activities:")
                    for agent, count in sorted(analysis['agent_activities'].items()):
                        print(f"   {agent}: {count} executions")
                
                if analysis['tool_calls']:
                    print(f"\nTool Calls: {len(analysis['tool_calls'])}")
                
                if analysis['errors']:
                    print(f"\n❌ Errors: {len(analysis['errors'])}")
                    for error in analysis['errors'][:3]:
                        print(f"   [{error['timestamp']}] {error['message'][:100]}...")
        
        # Metrics reports summary
        print("\n" + "="*80)
        reports = self.list_metrics_reports()
        print(f"📊 Metrics Reports Available: {len(reports)}")
        
        if reports:
            print("\nRecent Metrics Reports:")
            for i, report_file in enumerate(reports[:5], 1):
                size_kb = report_file.stat().st_size / 1024
                modified = datetime.fromtimestamp(report_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"   {i}. {report_file.name} ({size_kb:.2f} KB) - {modified}")
        
        print("\n" + "="*80)
        print("\n💡 TIP: Logs are stored in ./storage/logs/")
        print("💡 TIP: Metrics reports are stored in ./storage/results/")
        print("💡 TIP: Run 'python main_workflow.py' to generate new logs and metrics\n")


def main():
    """Main entry point."""
    viewer = LogViewer()
    
    print("\n" + "="*80)
    print("🔍 ADK MULTI-AGENT SYSTEM - LOG & METRICS VIEWER")
    print("="*80)
    
    # Generate comprehensive summary
    viewer.generate_time_series_summary()
    
    print("\n" + "="*80)
    print("📋 DETAILED LOG VIEW (Last 50 lines)")
    print("="*80)
    viewer.view_latest_log(lines=-50)
    
    print("\n" + "="*80)
    print("📊 DETAILED METRICS REPORT")
    print("="*80)
    viewer.view_metrics_report()


if __name__ == "__main__":
    main()
