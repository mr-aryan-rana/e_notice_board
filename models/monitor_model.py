# e_notice_board/models/monitor_model.py
from datetime import datetime
from .base import BaseModel, db

class Monitor(BaseModel):
    __tablename__ = 'monitors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    screen_size = db.Column(db.String(50))  # e.g., "1920x1080"
    is_active = db.Column(db.Boolean, default=True)

    # ✅ Timestamps for tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # 🔗 Relationship with Assignment
    assignments = db.relationship(
        "Assignment",
        back_populates="monitor",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Monitor id={self.id}, name='{self.name}', active={self.is_active}>"
