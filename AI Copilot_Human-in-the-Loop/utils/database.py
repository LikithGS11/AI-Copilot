import sqlite3
import json
import os
from datetime import datetime
from contextlib import contextmanager

# Database configuration
DB_PATH = "ai_copilot_hil_edit/modules.db"

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize the database with required tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Modules table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'draft'
            )
        """)
        
        # Sections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER NOT NULL,
                section_id TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                type TEXT NOT NULL,
                bloom_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
                UNIQUE(module_id, section_id)
            )
        """)
        
        # Approvals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER NOT NULL,
                is_approved BOOLEAN DEFAULT 0,
                is_rejected BOOLEAN DEFAULT 0,
                rejection_comments TEXT,
                approved_at TIMESTAMP,
                rejected_at TIMESTAMP,
                FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
                UNIQUE(section_id)
            )
        """)
        
        # Versions table (for tracking edits)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER NOT NULL,
                original_content TEXT NOT NULL,
                edited_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE
            )
        """)

def reset_db():
    """Clear all data from the database (for testing/reset purposes)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM versions")
        cursor.execute("DELETE FROM approvals")
        cursor.execute("DELETE FROM sections")
        cursor.execute("DELETE FROM modules")

def save_module_to_db(module_title, sections):
    """Save a complete module with all sections to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Insert module
        cursor.execute("""
            INSERT INTO modules (module_title, status)
            VALUES (?, ?)
        """, (module_title, 'draft'))
        module_id = cursor.lastrowid
        
        # Insert sections
        for section in sections:
            cursor.execute("""
                INSERT INTO sections (module_id, section_id, title, content, type, bloom_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                module_id,
                section['id'],
                section['title'],
                section['content'],
                section['type'],
                section.get('bloom_level')
            ))
            section_db_id = cursor.lastrowid
            
            # Initialize approval record
            cursor.execute("""
                INSERT INTO approvals (section_id, is_approved, is_rejected)
                VALUES (?, ?, ?)
            """, (section_db_id, 0, 0))
        
        return module_id

def get_module_by_id(module_id):
    """Retrieve a complete module from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get module
        cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
        module = cursor.fetchone()
        
        if not module:
            return None
        
        # Get sections
        cursor.execute("""
            SELECT s.*, a.is_approved, a.is_rejected, a.rejection_comments
            FROM sections s
            LEFT JOIN approvals a ON s.id = a.section_id
            WHERE s.module_id = ?
            ORDER BY s.id
        """, (module_id,))
        sections = cursor.fetchall()
        
        return {
            'id': module['id'],
            'module_title': module['module_title'],
            'created_at': module['created_at'],
            'updated_at': module['updated_at'],
            'status': module['status'],
            'sections': [dict(s) for s in sections]
        }

def get_all_modules():
    """Get all modules with their status."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, module_title, created_at, updated_at, status
            FROM modules
            ORDER BY created_at DESC
        """)
        modules = cursor.fetchall()
        return [dict(m) for m in modules]

def update_section_content(section_id, new_content):
    """Update section content and create a version record."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get original content
        cursor.execute("SELECT content FROM sections WHERE id = ?", (section_id,))
        result = cursor.fetchone()
        if result:
            original_content = result[0]
            
            # Create version record
            cursor.execute("""
                INSERT INTO versions (section_id, original_content, edited_content)
                VALUES (?, ?, ?)
            """, (section_id, original_content, new_content))
            
            # Update section
            cursor.execute("""
                UPDATE sections
                SET content = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_content, section_id))

def approve_section(section_id):
    """Mark a section as approved."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE approvals
            SET is_approved = 1, is_rejected = 0, approved_at = CURRENT_TIMESTAMP
            WHERE section_id = ?
        """, (section_id,))

def reject_section(section_id, comments=""):
    """Mark a section as rejected with optional comments."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE approvals
            SET is_rejected = 1, is_approved = 0, rejection_comments = ?, rejected_at = CURRENT_TIMESTAMP
            WHERE section_id = ?
        """, (comments, section_id))

def publish_module(module_id):
    """Mark a module as published."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE modules
            SET status = 'published', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (module_id,))

def get_module_stats(module_id):
    """Get approval statistics for a module."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                COUNT(*) as total_sections,
                SUM(CASE WHEN is_approved = 1 THEN 1 ELSE 0 END) as approved_count,
                SUM(CASE WHEN is_rejected = 1 THEN 1 ELSE 0 END) as rejected_count
            FROM sections s
            LEFT JOIN approvals a ON s.id = a.section_id
            WHERE s.module_id = ?
        """, (module_id,))
        
        stats = cursor.fetchone()
        return {
            'total_sections': stats[0] or 0,
            'approved_count': stats[1] or 0,
            'rejected_count': stats[2] or 0,
            'pending_count': (stats[0] or 0) - (stats[1] or 0) - (stats[2] or 0)
        }

def export_module_to_json(module_id):
    """Export a module to JSON format."""
    module = get_module_by_id(module_id)
    if not module:
        return None
    
    return {
        'module_title': module['module_title'],
        'sections': [
            {
                'id': s['section_id'],
                'title': s['title'],
                'content': s['content'],
                'type': s['type'],
                'bloom_level': s['bloom_level'],
                'is_approved': s['is_approved'],
                'rejection_comments': s['rejection_comments']
            }
            for s in module['sections']
        ]
    }

def get_section_versions(section_id):
    """Get all versions of a section."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, original_content, edited_content, created_at
            FROM versions
            WHERE section_id = ?
            ORDER BY created_at DESC
        """, (section_id,))
        versions = cursor.fetchall()
        return [dict(v) for v in versions]

# Initialize database on import
if not os.path.exists(DB_PATH):
    init_db()
