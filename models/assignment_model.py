# e_notice_board/models/assignment_model.py
from .base import BaseModel, db
from datetime import datetime

class Assignment(BaseModel):
    __tablename__ = 'assignments'
    
    notice_id = db.Column(db.Integer, db.ForeignKey('notices.id'), nullable=False)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitors.id'), nullable=False)

    # Relationships
    notice = db.relationship("Notice", back_populates="assignments")
    monitor = db.relationship("Monitor", back_populates="assignments")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Assignment Notice:{self.notice_id} Monitor:{self.monitor_id}>'
