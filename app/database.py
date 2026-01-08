# データベース接続・操作
# 後で実装します

import sqlite3
from typing import Optional

DATABASE = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            quadrant INTEGER NOT NULL CHECK(quadrant IN (1, 2, 3, 4)),
            position INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            due_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # positionカラムが存在しない場合は追加（マイグレーション）
    cursor.execute('PRAGMA table_info(tasks)')
    columns = [column[1] for column in cursor.fetchall()]
    if 'position' not in columns:
        cursor.execute('ALTER TABLE tasks ADD COLUMN position INTEGER DEFAULT 0')
    
    conn.commit()
    conn.close()

def create_task(title: str, description: Optional[str], quadrant: int, due_date: Optional[str] = None):
    """新しいタスクを作成"""
    conn = get_connection()
    cursor = conn.cursor()
    # 同じ象限内の最大positionを取得して+1
    cursor.execute('SELECT COALESCE(MAX(position), -1) FROM tasks WHERE quadrant = ?', (quadrant,))
    max_position = cursor.fetchone()[0]
    new_position = max_position + 1
    
    cursor.execute('''
        INSERT INTO tasks (title, description, quadrant, position, due_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, quadrant, new_position, due_date))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def get_all_tasks():
    """すべてのタスクを取得"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY quadrant, position, created_at')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_tasks_by_quadrant(quadrant: int):
    """指定された象限のタスクを順序付きで取得"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE quadrant = ? ORDER BY position, created_at', (quadrant,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_task_by_id(task_id: int):
    """IDでタスクを取得"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None, 
                quadrant: Optional[int] = None, position: Optional[int] = None, 
                completed: Optional[bool] = None, due_date: Optional[str] = None):
    """タスクを更新"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 更新するフィールドを動的に構築
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if quadrant is not None:
        updates.append("quadrant = ?")
        params.append(quadrant)
    if position is not None:
        updates.append("position = ?")
        params.append(position)
    if completed is not None:
        updates.append("completed = ?")
        params.append(completed)
    if due_date is not None:
        updates.append("due_date = ?")
        params.append(due_date)
    
    # updated_atを更新
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(task_id)
    
    if updates:
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()

def update_task_positions(quadrant: int, task_positions: list):
    """象限内のタスクの順序を一括更新
    task_positions: [(task_id, position), ...] の形式
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    for task_id, position in task_positions:
        cursor.execute('UPDATE tasks SET position = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
                      (position, task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    """タスクを削除"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# 動作確認用

if __name__ == "__main__":
    init_db()
    print("✅ データベースの初期化が完了しました！")
    
    # 動作確認
    task_id = create_task("テストタスク", "これはテストです", 1)
    print(f"✅ タスクを作成しました。ID: {task_id}")
    
    tasks = get_all_tasks()
    print(f"✅ タスク一覧: {len(tasks)}件")
    
    task = get_task_by_id(task_id)
    print(f"✅ タスクを取得: {task}")
    
    update_task(task_id, completed=True)
    print("✅ タスクを更新しました")
    
    delete_task(task_id)
    print("✅ タスクを削除しました")
