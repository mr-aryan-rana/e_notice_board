# e_notice_board/utils/db_helper.py
from models import db

def init_db():
    """Initialize the database"""
    db.create_all()

def clear_db():
    """Clear all data from the database"""
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()