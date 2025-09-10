from models.base import db
from models.monitor_model import Monitor
from app import create_app
from datetime import datetime

app = create_app()
with app.app_context():
    new_monitor = Monitor(
        name="noticeboard4",
        location="bca",
        screen_size="1920x1080",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_monitor)
    db.session.commit()
    print("Monitor added successfully ✅")
