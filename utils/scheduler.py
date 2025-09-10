# e_notice_board/utils/scheduler.py
from datetime import datetime
import pytz
from models.base import db
from models.notice_model import Notice
import threading
import time

def check_and_deactivate_expired_notices():
    """Check and deactivate any notices that have passed their end time"""
    try:
        # ✅ Use UTC to match how we save start_time / end_time
        now = datetime.now(pytz.UTC)

        expired_notices = Notice.query.filter(
            Notice.end_time.isnot(None),
            Notice.end_time < now,
            Notice.is_active == True
        ).all()
        
        if expired_notices:
            for notice in expired_notices:
                notice.is_active = False
                print(f"Deactivated expired notice: {notice.title} (End time: {notice.end_time})")
            
            db.session.commit()
            print(f"Deactivated {len(expired_notices)} expired notices at {now}")
        
        return len(expired_notices)
        
    except Exception as e:
        print(f"Error checking expired notices: {e}")
        return 0

def start_background_checker(app):
    """Start a background thread that checks for expired notices every minute"""
    def background_check():
        with app.app_context():
            while True:
                check_and_deactivate_expired_notices()
                time.sleep(60)  # Check every minute
    
    thread = threading.Thread(target=background_check, daemon=True)
    thread.start()
    print("Background notice checker started")
