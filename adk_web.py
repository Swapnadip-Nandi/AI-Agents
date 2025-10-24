"""
ADK Web Interface Server with Real-Time Log Streaming
Launch the multi-agent system through a web interface with session management
"""
import os
import sys
from pathlib import Path
import threading

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import enhanced components
from workflows.enhanced_campaign_workflow import EnhancedCampaignWorkflow
from shared.session_manager import SessionManager
from shared.realtime_streaming import LogStreamer, ProgressTracker
from shared.logger import Logger

# Initialize Flask web server
try:
    from flask import Flask, render_template, request, jsonify, Response, stream_with_context
    import json
except ImportError:
    print("Flask not installed. Installing...")
    os.system("pip install flask")
    from flask import Flask, render_template, request, jsonify, Response, stream_with_context
    import json

app = Flask(__name__)
logger = Logger("ADK_Web_Server")

# Global session manager
session_manager = SessionManager(storage_root="./storage")

# Store active workflows by session ID
active_workflows = {}
workflow_lock = threading.Lock()

@app.route('/')
def index():
    """Main dashboard page"""
    # Get recent sessions
    recent_sessions = session_manager.list_sessions(limit=10)
    stats = session_manager.get_session_stats()
    
    return render_template('index.html', 
                          recent_sessions=recent_sessions,
                          stats=stats)

@app.route('/api/start', methods=['POST'])
def start_workflow():
    """Start the campaign workflow"""
    global active_workflows
    
    try:
        data = request.json
        product_info = data.get('product_info', {})
        
        if not product_info:
            return jsonify({"error": "Product information required"}), 400
        
        logger.info("Starting campaign workflow via web interface")
        
        # Create workflow instance
        workflow = EnhancedCampaignWorkflow(
            storage_root="./storage",
            session_manager=session_manager
        )
        
        # Run workflow in background thread
        def run_workflow():
            try:
                results = workflow.execute(product_info)
                with workflow_lock:
                    active_workflows[results['session_id']] = {
                        'status': 'completed',
                        'results': results
                    }
            except Exception as e:
                logger.error(f"Workflow error: {str(e)}")
                if workflow.session_id:
                    with workflow_lock:
                        active_workflows[workflow.session_id] = {
                            'status': 'failed',
                            'error': str(e)
                        }
        
        thread = threading.Thread(target=run_workflow, daemon=True)
        thread.start()
        
        # Wait a moment to get session ID
        import time
        time.sleep(0.5)
        
        session_id = workflow.session_id if workflow.session_id else "pending"
        
        with workflow_lock:
            active_workflows[session_id] = {
                'status': 'running',
                'thread': thread
            }
        
        return jsonify({
            "success": True,
            "message": "Workflow started successfully",
            "session_id": session_id
        })
        
    except Exception as e:
        logger.error(f"Start workflow error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/status')
def get_status():
    """Get current workflow status"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        # Return overall system status
        return jsonify({
            "system": "operational",
            "active_sessions": len([w for w in active_workflows.values() if w.get('status') == 'running']),
            "stats": session_manager.get_session_stats()
        })
    
    # Return specific session status
    with workflow_lock:
        workflow_info = active_workflows.get(session_id)
    
    if not workflow_info:
        metadata = session_manager.get_session_metadata(session_id)
        if metadata:
            return jsonify({
                "session_id": session_id,
                "status": metadata.status,
                "metadata": metadata.__dict__
            })
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify({
        "session_id": session_id,
        "status": workflow_info.get('status'),
        "results": workflow_info.get('results', {}),
        "error": workflow_info.get('error')
    })

@app.route('/api/sessions')
def list_sessions():
    """List all sessions"""
    status_filter = request.args.get('status')
    limit = request.args.get('limit', type=int)
    
    sessions = session_manager.list_sessions(status=status_filter, limit=limit)
    
    return jsonify({
        "sessions": [s.__dict__ for s in sessions],
        "stats": session_manager.get_session_stats()
    })

@app.route('/api/session/<session_id>/progress')
def get_session_progress(session_id):
    """Get session progress"""
    with workflow_lock:
        workflow_info = active_workflows.get(session_id)
    
    if workflow_info and workflow_info.get('status') == 'running':
        # Progress would be tracked in workflow
        return jsonify({
            "session_id": session_id,
            "status": "running",
            "message": "Workflow in progress"
        })
    
    metadata = session_manager.get_session_metadata(session_id)
    if metadata:
        return jsonify({
            "session_id": session_id,
            "status": metadata.status,
            "metadata": metadata.__dict__
        })
    
    return jsonify({"error": "Session not found"}), 404

@app.route('/api/session/<session_id>/logs')
def get_session_logs(session_id):
    """Get session logs (recent events)"""
    try:
        session_dir = session_manager.get_session_dir(session_id)
        
        if not session_dir.exists():
            return jsonify({"error": "Session not found"}), 404
        
        streamer = LogStreamer(session_dir)
        logs = streamer.get_recent_logs(count=100)
        
        return jsonify({
            "session_id": session_id,
            "logs": logs,
            "summary": streamer.get_log_summary()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/<session_id>/stream')
def stream_session_logs(session_id):
    """Stream session logs in real-time using Server-Sent Events"""
    try:
        session_dir = session_manager.get_session_dir(session_id)
        
        if not session_dir.exists():
            return jsonify({"error": "Session not found"}), 404
        
        streamer = LogStreamer(session_dir)
        
        def generate():
            for event in streamer.stream_logs(follow=True):
                yield event
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents')
def get_agents():
    """Get list of available agents"""
    agents = [
        {
            "id": "lead_planner",
            "name": "Lead Planner",
            "type": "orchestrator",
            "status": "active",
            "description": "Strategic campaign architect"
        },
        {
            "id": "market_research_analyst",
            "name": "Market Research Analyst",
            "type": "researcher",
            "status": "active",
            "description": "Competitive intelligence specialist"
        },
        {
            "id": "seo_specialist",
            "name": "SEO Specialist",
            "type": "specialist",
            "status": "active",
            "description": "Keyword optimization expert"
        },
        {
            "id": "copywriter",
            "name": "Copywriter",
            "type": "creator",
            "status": "active",
            "description": "Amazon listing content creator"
        },
        {
            "id": "social_media_marketer",
            "name": "Social Media Marketer",
            "type": "marketer",
            "status": "active",
            "description": "Multi-platform campaign designer"
        },
        {
            "id": "quality_validator",
            "name": "Quality Validator",
            "type": "validator",
            "status": "active",
            "description": "Compliance and quality assurance specialist"
        }
    ]
    return jsonify(agents)

@app.route('/api/cleanup', methods=['POST'])
def cleanup_sessions():
    """Manually trigger session cleanup"""
    try:
        count = session_manager.cleanup_old_sessions()
        return jsonify({
            "success": True,
            "message": f"Cleaned up {count} old sessions"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get recent system logs"""
    try:
        log_dir = project_root / "storage" / "logs"
        logs = []
        
        # Find most recent log file
        log_files = sorted(log_dir.glob("amazon_campaign_*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if log_files:
            with open(log_files[0], 'r', encoding='utf-8') as f:
                logs = f.readlines()[-50:]  # Last 50 lines
        
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 ADK Multi-Agent System - Enhanced Web Interface")
    print("="*80)
    print(f"\n📍 Server running at: http://localhost:8000")
    print(f"📁 Project directory: {project_root}")
    print("\n🤖 Available Agents:")
    print("   1. Lead Planner (Strategic Orchestrator)")
    print("   2. Market Research Analyst (Competitive Intelligence)")
    print("   3. SEO Specialist (Keyword Optimization)")
    print("   4. Copywriter (Content Creation)")
    print("   5. Social Media Marketer (Multi-platform Campaigns)")
    print("   6. Quality Validator (Compliance & QA)")
    print("\n✨ New Features:")
    print("   • Session-based tracking with unique IDs")
    print("   • Real-time log streaming (Server-Sent Events)")
    print("   • Long-term campaign learning")
    print("   • Async logging for performance")
    print("   • Auto cleanup after 7 days")
    print("\n💡 Open your browser and navigate to http://localhost:8000")
    print("="*80 + "\n")
    
    app.run(host='localhost', port=8000, debug=True, threaded=True)

