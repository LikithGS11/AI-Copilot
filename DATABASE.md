# Database Structure

This project uses **SQLite** to store and manage educational modules with full version control and approval tracking.

## Database File
- **Location:** `ai_copilot_hil_edit/modules.db`
- **Type:** SQLite 3
- **Auto-created:** Yes, on first app run

## Tables

### 1. **modules**
Stores the main module records.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Unique module identifier |
| `module_title` | TEXT | Name of the module |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |
| `status` | TEXT | Module status: 'draft' or 'published' |

**Example:**
```
id | module_title | created_at | updated_at | status
1  | RAG Module   | 2025-11-14 | 2025-11-14 | draft
```

### 2. **sections**
Stores individual sections (Learning Objectives, Lessons, Assessments).

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Unique section database ID |
| `module_id` | INTEGER (FK) | Reference to parent module |
| `section_id` | TEXT | Unique section identifier (e.g., 'lo1', 'lesson1') |
| `title` | TEXT | Section title |
| `content` | TEXT | Section content |
| `type` | TEXT | Type: 'learning_objective', 'lesson', or 'assessment' |
| `bloom_level` | TEXT | Bloom's taxonomy level (optional) |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

**Constraints:**
- Foreign key to `modules.id`
- Unique constraint on `(module_id, section_id)`

### 3. **approvals**
Tracks approval/rejection status for each section.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Unique approval record ID |
| `section_id` | INTEGER (FK) | Reference to section |
| `is_approved` | BOOLEAN | Whether section is approved |
| `is_rejected` | BOOLEAN | Whether section is rejected |
| `rejection_comments` | TEXT | Reason for rejection |
| `approved_at` | TIMESTAMP | When approved |
| `rejected_at` | TIMESTAMP | When rejected |

**Constraints:**
- Foreign key to `sections.id`
- Unique constraint on `section_id` (one approval record per section)

### 4. **versions**
Maintains version history of all edits to sections.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Unique version ID |
| `section_id` | INTEGER (FK) | Reference to section |
| `original_content` | TEXT | Original content before edit |
| `edited_content` | TEXT | New edited content |
| `created_at` | TIMESTAMP | Edit timestamp |

**Use Cases:**
- Track all changes to sections
- Compare versions
- Rollback if needed

## Key Features

### ✅ Automatic Initialization
The database is created automatically on the first app run with all tables and constraints.

### ✅ Version Control
Every time a section is edited, a new version record is created, maintaining full audit trail.

### ✅ Approval Tracking
Each section has its own approval/rejection record with comments and timestamps.

### ✅ Cascading Deletes
If a module is deleted, all associated sections, approvals, and versions are automatically deleted.

## Database Functions

### Core Operations
```python
# Initialize database
init_db()

# Save a new module
module_id = save_module_to_db(module_title, sections)

# Get a complete module
module = get_module_by_id(module_id)

# Get all modules
modules = get_all_modules()

# Get module statistics
stats = get_module_stats(module_id)
# Returns: {total_sections, approved_count, rejected_count, pending_count}
```

### Edit & Approval Operations
```python
# Update section content (creates version record)
update_section_content(section_id, new_content)

# Mark section as approved
approve_section(section_id)

# Mark section as rejected
reject_section(section_id, comments="Reason for rejection")

# Publish module (change status to 'published')
publish_module(module_id)
```

### Export & Retrieval
```python
# Export module to JSON
export_data = export_module_to_json(module_id)

# Get version history of a section
versions = get_section_versions(section_id)
```

## App Integration

### Generate Module (4.1)
When you generate a module, it's automatically saved to:
1. **Database** (primary storage)
2. **JSON file** (backward compatibility)

### Editor (4.2)
- Tracks edits in the `versions` table
- Updates section content
- Records approvals/rejections with comments

### Module Library (DB) - NEW PAGE
New page to browse all modules in the database:
- View module statistics
- See approval status of all sections
- View version history
- Export modules as JSON

### Analytics
Uses database data to generate real-time statistics.

## Database Queries

### Get modules by status
```sql
SELECT * FROM modules WHERE status = 'published';
```

### Get approval statistics for a module
```sql
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN is_approved = 1 THEN 1 ELSE 0 END) as approved,
  SUM(CASE WHEN is_rejected = 1 THEN 1 ELSE 0 END) as rejected
FROM sections s
LEFT JOIN approvals a ON s.id = a.section_id
WHERE s.module_id = ?;
```

### Get all rejections
```sql
SELECT s.title, a.rejection_comments, a.rejected_at
FROM sections s
JOIN approvals a ON s.id = a.section_id
WHERE a.is_rejected = 1;
```

### Get version history for a section
```sql
SELECT * FROM versions
WHERE section_id = ?
ORDER BY created_at DESC;
```

## Backup & Recovery

### Export Module
Use the "📥 Export Module as JSON" button in Module Library to download any module.

### Database File
To backup your entire database, copy `ai_copilot_hil_edit/modules.db` to a safe location.

## Performance Notes

- Database uses SQLite, suitable for single-user/small team use
- Indexes are created on foreign keys automatically
- For large-scale production, consider PostgreSQL or MySQL
