import json
import sqlite3
import os

def migrate_worklogs(db_path, worklogs_json, tags_json):
    # Load JSON data
    with open(worklogs_json, 'r', encoding='utf-8') as f:
        worklogs = json.load(f)
    
    with open(tags_json, 'r', encoding='utf-8') as f:
        log_tags = json.load(f)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Migrating {len(worklogs)} work logs...")
    
    # Insert work logs
    for log in worklogs:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO work_log_worklog (id, date, task_description, created_at, user_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                log['id'],
                log['log_date'],
                log['task'],
                log['created_at'],
                log['user_id']
            ))
        except KeyError as e:
            print(f"Error in log {log.get('id')}: Missing key {e}")
        except sqlite3.Error as e:
            print(f"Database error in log {log.get('id')}: {e}")

    print(f"Migrating {len(log_tags)} work log tag relationships...")
    
    # Insert work log tag relationships
    for mapping in log_tags:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO work_log_worklog_tags (id, worklog_id, tag_id)
                VALUES (?, ?, ?)
            ''', (
                mapping['id'],
                mapping['worklog_id'],
                mapping['tag_id']
            ))
        except KeyError as e:
            print(f"Error in mapping {mapping.get('id')}: Missing key {e}")
        except sqlite3.Error as e:
            print(f"Database error in mapping {mapping.get('id')}: {e}")

    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    DB_PATH = "db_v2.sqlite3"
    WORKLOGS_JSON = "logs_worklog.json"
    TAGS_JSON = "logs_worklog_tags.json"
    
    if os.path.exists(WORKLOGS_JSON) and os.path.exists(TAGS_JSON):
        migrate_worklogs(DB_PATH, WORKLOGS_JSON, TAGS_JSON)
    else:
        print("Required JSON files not found.")
