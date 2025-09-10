from app import create_app
from models.base import db

app = create_app()

with app.app_context():
    # For SQLite, we need to use raw SQL to alter the table
    conn = db.engine.connect()
    
    # Check if is_deleted column exists in notices table
    result = conn.execute("PRAGMA table_info(notices)")
    columns = [row[1] for row in result]
    
    if 'is_deleted' not in columns:
        print("Adding is_deleted column to notices table...")
        conn.execute("ALTER TABLE notices ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE")
        print("Column added successfully!")
    else:
        print("is_deleted column already exists.")
    
    conn.close()