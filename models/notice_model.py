# e_notice_board/models/notice_model.py
from datetime import datetime
from .base import db

class Notice(db.Model):
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, default=1)  # 1=Low, 2=Medium, 3=High
    position = db.Column(db.String(50))  # Top, Middle, Bottom, etc.
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    display_duration = db.Column(db.Integer, default=10)  # seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    # 🔗 Link with assignments
    assignments = db.relationship(
        "Assignment",
        back_populates="notice",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f'<Notice {self.title}>'
