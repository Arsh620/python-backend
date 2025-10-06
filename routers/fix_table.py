from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db_config import get_db

router = APIRouter(prefix="/fix", tags=["database"])

@router.post("/add-created-at-column")
def add_created_at_column(db: Session = Depends(get_db)):
    try:
        # Add created_at column to existing table
        db.execute(text("""
            ALTER TABLE user_activity_logs 
            ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """))
        db.commit()
        
        return {
            "success": True,
            "message": "created_at column added successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/table-structure")
def get_table_structure(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'user_activity_logs'
        """))
        
        columns = [{"name": row[0], "type": row[1]} for row in result]
        
        return {
            "success": True,
            "columns": columns
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }