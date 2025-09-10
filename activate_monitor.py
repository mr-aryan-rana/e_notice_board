# activate_monitor.py
from datetime import datetime
from app import create_app
from models.base import db
from models.monitor_model import Monitor
from models.notice_model import Notice
from models.assignment_model import Assignment  # must import!

app = create_app()

with app.app_context():
    # 1️⃣ Ensure virtual monitor exists
    monitor = Monitor.query.filter_by(name='Virtual Test Monitor').first()
    if not monitor:
        monitor = Monitor(
            name='Virtual Test Monitor',
            location='Testing Environment',
            screen_size='1920x1080',
            is_active=True
        )
        db.session.add(monitor)
        db.session.commit()
        print("✅ Virtual monitor created and activated.")
    elif not monitor.is_active:
        monitor.is_active = True
        db.session.commit()
        print("✅ Existing monitor activated.")
    else:
        print("✅ Monitor already active.")

    # 2️⃣ Ensure notices exist
    notices_data = [
        {
            'title': 'Welcome to E-Notice Board',
            'content': 'This is a test notice to demonstrate the system.\nPriority: High',
            'priority': 3,
            'position': 'middle',
            'display_duration': 8
        },
        {
            'title': 'Important Announcement',
            'content': 'All staff meeting tomorrow at 10 AM in the conference room.',
            'priority': 2,
            'position': 'top',
            'display_duration': 6
        },
        {
            'title': 'System Maintenance',
            'content': 'Scheduled maintenance this weekend. System will be offline from 10 PM to 2 AM.',
            'priority': 1,
            'position': 'bottom',
            'display_duration': 5
        }
    ]

    created_notices = []
    for notice_data in notices_data:
        notice = Notice.query.filter_by(title=notice_data['title']).first()
        if not notice:
            notice = Notice(**notice_data)
            db.session.add(notice)
            created_notices.append(notice)

    if created_notices:
        db.session.flush()  # ensure notice.id exists
        db.session.commit()
        print(f"✅ {len(created_notices)} test notices created.")
    else:
        print("ℹ️ All test notices already exist.")

    # 3️⃣ Assign notices to monitor
    assigned_count = 0
    for notice in Notice.query.all():
        # Check if assignment already exists
        existing = Assignment.query.filter_by(
            monitor_id=monitor.id,
            notice_id=notice.id
        ).first()
        if not existing:
            assignment = Assignment(
                monitor_id=monitor.id,
                notice_id=notice.id
            )
            db.session.add(assignment)
            assigned_count += 1

    if assigned_count:
        db.session.commit()
        print(f"✅ {assigned_count} notices assigned to the virtual monitor!")
    else:
        print("ℹ️ All notices already assigned.")

    print("🎉 Monitor activation and test data setup complete.")
