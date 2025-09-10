#e_notice_board/routes/monitor_routes.py
from flask import Blueprint, render_template, jsonify
from models.notice_model import Notice
from models.monitor_model import Monitor
from utils.scheduler import check_and_deactivate_expired_notices
from models.assignment_model import Assignment
from models.base import db
from datetime import datetime
from datetime import datetime
from models.monitor_model import Monitor
from models.notice_model import Notice
from models.assignment_model import Assignment
from models.base import db

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/display/<int:monitor_id>')
def display(monitor_id):
    monitor = Monitor.query.get_or_404(monitor_id)
    monitor.is_active = bool(monitor.is_active)  # ensure boolean

    if not monitor.is_active:
        return render_template('monitor/blocked.html', monitor=monitor)

    # Get assigned active notices
    notices = Notice.query.join(Assignment).filter(
        Assignment.monitor_id == monitor.id,
        Notice.is_active == True
    ).order_by(Notice.priority.desc()).all()

    return render_template('monitor/display.html', monitor=monitor, notices=notices)

# Monitor Notice API (JSON)
# -----------------------
@monitor_bp.route('/api/display/<int:monitor_id>')
def api_display(monitor_id):
    """Return assigned notices as JSON for a monitor."""
    monitor = Monitor.query.get_or_404(monitor_id)
    
    if not monitor.is_active:
        return jsonify({"status": "blocked", "message": "This monitor is blocked"}), 403

    # Ensure expired notices are deactivated
    check_and_deactivate_expired_notices()
    
    now = datetime.utcnow()

    assignments = (
        Assignment.query.join(Notice)
        .filter(
            Assignment.monitor_id == monitor.id,
            Notice.is_active == True,
            Notice.is_deleted == False,
            Notice.start_time <= now,
            db.or_(Notice.end_time.is_(None), Notice.end_time >= now)
        )
        .order_by(Notice.priority.desc(), Notice.created_at.desc())
        .all()
    )

    print(f"Monitor {monitor.name} has {len(assignments)} assignments at {now}")

    notices_data = [
        {
            'id': n.id,
            'title': n.title,
            'content': n.content,
            'priority': n.priority,
            'position': n.position,
            'display_duration': n.display_duration  # send in seconds
        }
        for n in (a.notice for a in assignments)
    ]

    return jsonify(notices_data)

# -----------------------
# Monitor Status Page
# -----------------------
@monitor_bp.route('/status')
def monitor_status():
    """Show all monitors and their status."""
    monitors = Monitor.query.all()  # Fetch all monitors regardless of status
    print(f"Total monitors: {len(monitors)}")
    return render_template('monitor/status.html', monitors=monitors)

# -----------------------
# Monitor Dashboard
# -----------------------
@monitor_bp.route('/dashboard/<int:monitor_id>')
def monitor_dashboard(monitor_id):
    """Monitor-specific dashboard showing assigned notices."""
    monitor = Monitor.query.get_or_404(monitor_id)

    if not monitor.is_active:
        print(f"Monitor {monitor.name} is blocked.")
        notices = []
    else:
        assignments = Assignment.query.filter_by(monitor_id=monitor.id).all()
        notices = [a.notice for a in assignments if a.notice.is_active and not a.notice.is_deleted]

    print(f"Monitor {monitor.name} dashboard with {len(notices)} notices.")
    return render_template('monitor/dashboard.html', monitor=monitor, notices=notices)