import sys
import os
# Ensure ai_copilot_hil_edit package path is discoverable when running this test
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.database import reset_db, init_db, save_module_to_db, get_module_by_id, update_section_content, approve_section, reject_section, get_module_stats, get_section_versions

# Reset and init
reset_db()
init_db()

# Create sample module
sections = [
    {"id": "sec1", "title": "Intro", "content": "Original intro", "type": "lesson", "bloom_level": "Understand"},
    {"id": "sec2", "title": "Topic", "content": "Original topic", "type": "lesson", "bloom_level": "Apply"}
]
module_title = "Test Module Buttons"

module_id = save_module_to_db(module_title, sections)
print(f"Saved module id: {module_id}")

module = get_module_by_id(module_id)
print("Module fetched:")
print({"id": module['id'], "title": module['module_title'], "sections_count": len(module['sections'])})

first = module['sections'][0]
print("First section DB record:", {"db_id": first['id'], "section_id": first['section_id'], "content": first['content']})

# Update content
update_section_content(first['id'], "Updated intro content")
print("Updated section content in DB.")

# Approve section
approve_section(first['id'])
print("Approved first section.")

# Stats
stats = get_module_stats(module_id)
print("Module stats:", stats)

# Versions
versions = get_section_versions(first['id'])
print("Versions for first section:", versions)

# Reject second section
second = module['sections'][1]
reject_section(second['id'], "Needs clarification")
print("Rejected second section with comment.")

# Final stats
stats2 = get_module_stats(module_id)
print("Final module stats:", stats2)

print("TEST COMPLETE")
