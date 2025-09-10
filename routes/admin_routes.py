# e_notice_board/routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models.notice_model import Notice
from utils.scheduler import check_and_deactivate_expired_notices
from models.admin_model import Admin
from models.monitor_model import Monitor
from models.assignment_model import Assignment
from models.base import db
from functools import wraps
from datetime import datetime
from functools import wraps
from routes.monitor_routes import monitor_status
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.admin_model import Admin
from models.base import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

from flask import make_response

@admin_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Auto-expire notices before showing stats
    check_and_deactivate_expired_notices()
    
    # Notices
    active_notices = Notice.query.filter_by(is_active=True, is_deleted=False).count()
    total_notices = Notice.query.filter_by(is_deleted=False).count()
    blocked_notices = Notice.query.filter_by(is_active=False, is_deleted=False).count()
    
    # Monitors
    total_monitors = Monitor.query.count()
    active_monitors_count = Monitor.query.filter_by(is_active=True).count()
    blocked_monitors_count = Monitor.query.filter_by(is_active=False).count()
    
    # **Actual monitor objects for template**
    active_monitors_list = Monitor.query.filter_by(is_active=True).all()

    return render_template(
        'admin/dashboard.html',
        active_notices=active_notices,
        total_notices=total_notices,
        blocked_notices=blocked_notices,
        total_monitors=total_monitors,
        active_monitors_count=active_monitors_count,
        blocked_monitors_count=blocked_monitors_count,
        monitors=active_monitors_list   # <-- pass the list
    )

@admin_bp.route('/create_monitor')
@login_required
def create_monitor():
    monitor = Monitor(name='Main Display', location='Office', screen_size='1920x1080')
    db.session.add(monitor)
    db.session.commit()
    flash(f'Monitor created with ID: {monitor.id}', 'success')
    return redirect(url_for('admin.dashboard'))

# @admin_bp.route('/create_test_data')
# @login_required
# def create_test_data():
#     try:
#         # Create a test monitor
#         monitor = Monitor.query.filter_by(name='Virtual Test Monitor').first()
#         if not monitor:
#             monitor = Monitor(
#                 name='Virtual Test Monitor',
#                 location='Testing Environment',
#                 screen_size='1920x1080',
#                 is_active=True  # <-- explicitly activate
#             )
#             db.session.add(monitor)
#             db.session.flush()
#             flash('Virtual monitor created and activated!', 'success')
#         else:
#             # Ensure existing monitor is active
#             if not monitor.is_active:
#                 monitor.is_active = True
#                 db.session.commit()
#                 flash('Existing monitor activated!', 'info')

#         # Create some test notices if they don't exist
#         notices_data = [
#             {
#                 'title': 'Welcome to E-Notice Board',
#                 'content': 'This is a test notice to demonstrate the system.\nPriority: High',
#                 'priority': 3,
#                 'position': 'middle',
#                 'display_duration': 8
#             },
#             {
#                 'title': 'Important Announcement',
#                 'content': 'All staff meeting tomorrow at 10 AM in the conference room.',
#                 'priority': 2,
#                 'position': 'top',
#                 'display_duration': 6
#             },
#             {
#                 'title': 'System Maintenance',
#                 'content': 'Scheduled maintenance this weekend. System will be offline from 10 PM to 2 AM.',
#                 'priority': 1,
#                 'position': 'bottom',
#                 'display_duration': 5
#             }
#         ]
        
#         created_notices = []
#         for notice_data in notices_data:
#             existing_notice = Notice.query.filter_by(title=notice_data['title']).first()
#             if not existing_notice:
#                 notice = Notice(**notice_data)
#                 db.session.add(notice)
#                 created_notices.append(notice)
        
#         if created_notices:
#             db.session.flush()  # Flush to get the notice IDs
#             flash(f'{len(created_notices)} test notices created!', 'success')
        
#         # Assign notices to monitor
#         monitor = Monitor.query.filter_by(name='Virtual Test Monitor').first()
#         notices = Notice.query.all()
        
#         assigned_count = 0
#         for notice in notices:
#             existing_assignment = Assignment.query.filter_by(
#                 notice_id=notice.id, 
#                 monitor_id=monitor.id
#             ).first()
            
#             if not existing_assignment:
#                 assignment = Assignment(notice_id=notice.id, monitor_id=monitor.id)
#                 db.session.add(assignment)
#                 assigned_count += 1
        
#         if assigned_count > 0:
#             db.session.commit()
#             flash(f'{assigned_count} notices assigned to virtual monitor!', 'success')
#         else:
#             db.session.commit()
#             flash('No new assignments were needed.', 'info')
        
#         return redirect(url_for('admin.dashboard'))
        
#     except Exception as e:
#         db.session.rollback()
#         flash(f'Error creating test data: {str(e)}', 'danger')
#         return redirect(url_for('admin.dashboard'))

@admin_bp.route('/create_test_data')
@login_required
def create_test_data():
    try:
        # --- 1️⃣ Create monitors ---
        monitors_data = [
            {"name": "Monitor 1", "location": "Room A", "screen_size": "1920x1080", "is_active": True},
            {"name": "Monitor 2", "location": "Room B", "screen_size": "1920x1080", "is_active": True},
            {"name": "Monitor 3", "location": "Room C", "screen_size": "1920x1080", "is_active": True}
        ]
        monitors = []
        for mdata in monitors_data:
            monitor = Monitor.query.filter_by(name=mdata['name']).first()
            if not monitor:
                monitor = Monitor(**mdata)
                db.session.add(monitor)
            else:
                monitor.is_active = True  # Ensure active
            monitors.append(monitor)
        db.session.flush()  # Get monitor IDs

        # --- 2️⃣ Create notices ---
        notices_data = [
            {"title": "Welcome to E-Notice Board", "content": "This is a test notice.", "priority": 3, "position": "middle", "display_duration": 8},
            {"title": "Important Announcement", "content": "All staff meeting tomorrow.", "priority": 2, "position": "top", "display_duration": 6},
            {"title": "System Maintenance", "content": "Scheduled maintenance this weekend.", "priority": 1, "position": "bottom", "display_duration": 5},
            {"title": "Notice 4", "content": "Extra notice 4 content.", "priority": 1, "position": "top", "display_duration": 4},
            {"title": "Notice 5", "content": "Extra notice 5 content.", "priority": 1, "position": "bottom", "display_duration": 3}
        ]
        notices = []
        for ndata in notices_data:
            notice = Notice.query.filter_by(title=ndata['title']).first()
            if not notice:
                notice = Notice(**ndata)
                db.session.add(notice)
            notices.append(notice)
        db.session.flush()  # Get notice IDs

        # --- 3️⃣ Assign notices to monitors ---
        assignments_map = {
            1: [1, 2, 3],       # Monitor 1 -> notices n1,n2,n3
            2: [1, 2, 5],       # Monitor 2 -> notices n1,n2,n5
            3: [2, 3, 4]        # Monitor 3 -> notices n2,n3,n4
        }
        assigned_count = 0
        for mid, notice_ids in assignments_map.items():
            for nid in notice_ids:
                existing = Assignment.query.filter_by(notice_id=nid, monitor_id=mid).first()
                if not existing:
                    assignment = Assignment(notice_id=nid, monitor_id=mid)
                    db.session.add(assignment)
                    assigned_count += 1

        db.session.commit()
        flash(f'Test data created successfully! {len(monitors)} monitors, {len(notices)} notices, {assigned_count} assignments.', 'success')
        return redirect(url_for('admin.dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error creating test data: {str(e)}', 'danger')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/notices')
@login_required
def list_notices():
    # Step 1: Check for expired notices and deactivate them
    check_and_deactivate_expired_notices()

    # Step 2: Fetch all active (non-deleted) notices in descending order
    notices = Notice.query.filter_by(is_deleted=False).order_by(Notice.created_at.desc()).all()

    # Step 3: Get the current UTC datetime
    now = datetime.utcnow()

    # Step 4: Pass both notices and current time to template
    return render_template('admin/list_notices.html', notices=notices, now=now)

@admin_bp.route('/edit_notice/<int:notice_id>', methods=['GET', 'POST'])
@login_required
def edit_notice(notice_id):
    """Edit an existing notice"""
    notice = Notice.query.get_or_404(notice_id)
    all_monitors = Monitor.query.all()  # Fetch all monitors for checkbox selection

    if request.method == 'POST':
        # --- Notice basic info ---
        notice.title = request.form.get('title')
        notice.content = request.form.get('content')
        notice.priority = request.form.get('priority', 1, type=int)
        notice.position = request.form.get('position')
        notice.display_duration = request.form.get('display_duration', 10, type=int)
        notice.is_active = True if request.form.get('is_active') else False

        # --- Time fields ---
        import pytz
        from datetime import datetime
        utc = pytz.UTC

        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')

        if start_time_str:
            notice.start_time = utc.localize(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M'))
        else:
            notice.start_time = datetime.now(utc)

        if end_time_str:
            notice.end_time = utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M'))
        else:
            notice.end_time = None

        # --- Assign monitors ---
        selected_ids = request.form.getlist('monitor_ids')  # Checkbox list from form
        selected_monitors = Monitor.query.filter(Monitor.id.in_(selected_ids)).all()
        notice.monitors = selected_monitors  # Replace old assignments

        db.session.commit()
        flash('Notice updated successfully!', 'success')
        return redirect(url_for('admin.list_notices'))

    # Pre-format dates for the form
    start_time_formatted = notice.start_time.strftime('%Y-%m-%dT%H:%M') if notice.start_time else ''
    end_time_formatted = notice.end_time.strftime('%Y-%m-%dT%H:%M') if notice.end_time else ''

    return render_template('admin/edit_notice.html', 
                           notice=notice,
                           all_monitors=all_monitors,  # Pass monitors for checkboxes
                           start_time_formatted=start_time_formatted,
                           end_time_formatted=end_time_formatted)

@admin_bp.route('/delete_notice/<int:notice_id>')
@login_required
def delete_notice(notice_id):
    """Soft delete a notice"""
    notice = Notice.query.get_or_404(notice_id)
    notice.is_deleted = True
    db.session.commit()
    flash('Notice deleted successfully!', 'success')
    return redirect(url_for('admin.list_notices'))

@admin_bp.route('/restore_notice/<int:notice_id>')
@login_required
def restore_notice(notice_id):
    """Restore a soft-deleted notice"""
    notice = Notice.query.get_or_404(notice_id)
    notice.is_deleted = False
    db.session.commit()
    flash('Notice restored successfully!', 'success')
    return redirect(url_for('admin.list_notices'))

@admin_bp.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('admin.add_admin'))

        existing_user = Admin.query.filter((Admin.username == username) | (Admin.email == email)).first()
        if existing_user:
            flash("Username or email already exists!", "danger")
            return redirect(url_for('admin.add_admin'))

        new_admin = Admin(username=username, email=email)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        flash(f"Admin '{username}' added successfully!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_admin.html')

@admin_bp.route('/monitors/add', methods=['GET', 'POST'])
@login_required
def add_monitor():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        screen_size = request.form.get('screen_size')

        if not name or not location or not screen_size:
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin.add_monitor'))

        new_monitor = Monitor(
            name=name,
            location=location,
            screen_size=screen_size,
            is_active=True
        )
        db.session.add(new_monitor)
        db.session.commit()

        flash(f'Monitor "{name}" added successfully!', 'success')
        return redirect(url_for('admin.list_monitors'))

    return render_template('admin/add_monitor.html')

@admin_bp.route('/monitors/delete/<int:monitor_id>', methods=['GET', 'POST'])
def delete_monitor(monitor_id):
    monitor = Monitor.query.get_or_404(monitor_id)
    db.session.delete(monitor)
    db.session.commit()
    flash(f"Monitor '{monitor.name}' deleted successfully!", "success")
    return redirect(url_for('monitor.monitor_status'))  # 👈 redirect to monitor list/status page

@admin_bp.route('/monitors/edit/<int:monitor_id>', methods=['GET', 'POST'])
def edit_monitor(monitor_id):
    monitor = Monitor.query.get_or_404(monitor_id)

    if request.method == 'POST':
        monitor.name = request.form['name']
        monitor.location = request.form['location']

        # Ensure is_active is properly converted to boolean
        is_active_str = request.form.get('is_active', '0')
        monitor.is_active = True if is_active_str == '1' else False

        db.session.commit()
        flash(f"Monitor '{monitor.name}' updated successfully!", "success")
        return redirect(url_for('monitor.monitor_status'))  # <-- make sure this endpoint exists

    return render_template('admin/edit_monitor.html', monitor=monitor)

@admin_bp.route('/permanent_delete_notice/<int:notice_id>')
@login_required
def permanent_delete_notice(notice_id):
    """Permanently delete a notice and its assignments"""
    notice = Notice.query.get_or_404(notice_id)
    
    # First delete any assignments for this notice
    Assignment.query.filter_by(notice_id=notice_id).delete()
    
    # Then delete the notice
    db.session.delete(notice)
    db.session.commit()
    flash('Notice permanently deleted!', 'success')
    return redirect(url_for('admin.list_notices'))

@admin_bp.route('/add_notice', methods=['GET', 'POST'])
@login_required
def add_notice():
    monitors = Monitor.query.filter_by(is_active=True).all()  # Only active monitors

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        priority = request.form.get('priority', 1, type=int)
        position = request.form.get('position')
        display_duration = request.form.get('display_duration', 10, type=int)

        # Parse date and time with UTC handling
        import pytz
        utc = pytz.UTC

        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')

        if start_time_str:
            start_time = utc.localize(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M'))
        else:
            start_time = datetime.now(utc)  # already timezone-aware

        if end_time_str:
            end_time = utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M'))
        else:
            end_time = None

        # Create notice
        notice = Notice(
            title=title,
            content=content,
            priority=priority,
            position=position,
            display_duration=display_duration,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(notice)
        db.session.commit()

        # Assign notice to selected monitors
        selected_monitors = request.form.getlist('monitor_ids')  # List of selected monitor IDs
        for monitor_id in selected_monitors:
            monitor = Monitor.query.get(int(monitor_id))
            if monitor:
                assignment = Assignment(notice_id=notice.id, monitor_id=monitor.id)
                db.session.add(assignment)
        db.session.commit()

        flash('Notice added and assigned successfully!', 'success')
        return redirect(url_for('admin.add_notice'))

    return render_template('admin/add_notice.html', monitors=monitors)

@admin_bp.route('/assign_notice', methods=['GET', 'POST'])
@login_required
def assign_notice():
    if request.method == 'POST':
        try:
            # Get selected notice ID
            notice_id = request.form.get('notice_id', type=int)
            # Get list of selected monitor IDs
            monitor_ids = request.form.getlist('monitor_ids')
            
            # Convert monitor IDs to integers and filter invalid
            monitor_ids = [int(mid) for mid in monitor_ids if mid.isdigit()]

            # Validation
            if not notice_id or not monitor_ids:
                flash('Please select both a notice and at least one monitor.', 'danger')
                return redirect(url_for('admin.assign_notice'))

            # Fetch the notice once
            notice = Notice.query.get(notice_id)
            if not notice or not notice.is_active:
                flash('Selected notice is invalid or inactive.', 'danger')
                return redirect(url_for('admin.assign_notice'))

            # Assign notice to monitors
            assigned_count = 0
            for mid in monitor_ids:
                monitor = Monitor.query.get(mid)
                if monitor and bool(monitor.is_active):  # ✅ Ensure proper boolean check
                    # Check if assignment already exists
                    existing = Assignment.query.filter_by(notice_id=notice_id, monitor_id=mid).first()
                    if not existing:
                        assignment = Assignment(notice_id=notice_id, monitor_id=mid)
                        db.session.add(assignment)
                        assigned_count += 1

            # Commit all at once
            if assigned_count > 0:
                db.session.commit()
                flash(f'Notice assigned to {assigned_count} monitor(s) successfully!', 'success')
            else:
                flash('No assignments were made. Selected monitors may already have this notice or are inactive.', 'info')

            return redirect(url_for('admin.assign_notice'))

        except (ValueError, TypeError) as e:
            flash('Invalid input. Please select valid notice and monitors.', 'danger')
            return redirect(url_for('admin.assign_notice'))

    # GET request: show active notices and active monitors
    notices = Notice.query.filter_by(is_active=True, is_deleted=False).all()
    monitors = Monitor.query.filter_by(is_active=True).all()
    assignments = Assignment.query.all()

    return render_template(
        'admin/assign_notice.html',
        notices=notices,
        monitors=monitors,
        assignments=assignments
    )

@admin_bp.route('/check_expired_notices')
@login_required
def check_expired_notices_route():
    """Manually check and deactivate expired notices"""
    expired_count = check_and_deactivate_expired_notices()
    flash(f'Deactivated {expired_count} expired notices.', 'success')
    return redirect(url_for('admin.list_notices'))

@admin_bp.route('/api/notices')
@login_required
def api_notices():
    notices = Notice.query.filter_by(is_active=True, is_deleted=False).order_by(Notice.priority.desc(), Notice.created_at.desc()).all()
    
    notices_data = []
    for notice in notices:
        notices_data.append({
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'priority': notice.priority,
            'position': notice.position,
            'display_duration': notice.display_duration
        })
    
    return jsonify(notices_data)