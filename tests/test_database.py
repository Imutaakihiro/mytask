"""
データベース操作のテスト
"""
import pytest
import os
from app.database import (
    init_db, create_task, get_all_tasks, get_task_by_id,
    get_tasks_by_quadrant, update_task, update_task_positions, delete_task
)

# テスト用のデータベースファイル名
TEST_DATABASE = "test_db_tasks.db"

@pytest.fixture(scope="function")
def setup_test_db():
    """テスト用のデータベースをセットアップ"""
    import app.database as db_module
    original_db = db_module.DATABASE
    db_module.DATABASE = TEST_DATABASE
    
    # データベースを初期化
    init_db()
    
    yield
    
    # テスト後にクリーンアップ
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)
    
    # 元のデータベース名に戻す
    db_module.DATABASE = original_db

def test_init_db(setup_test_db):
    """データベースの初期化テスト"""
    # init_db()はfixtureで実行済み
    # テーブルが存在することを確認
    import sqlite3
    conn = sqlite3.connect(TEST_DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None

def test_create_task(setup_test_db):
    """タスク作成のテスト"""
    task_id = create_task(
        title="テストタスク",
        description="説明",
        quadrant=1
    )
    assert task_id is not None
    assert isinstance(task_id, int)

def test_get_task_by_id(setup_test_db):
    """IDでタスクを取得するテスト"""
    task_id = create_task(
        title="取得テスト",
        description="説明",
        quadrant=2
    )
    
    task = get_task_by_id(task_id)
    assert task is not None
    assert task[1] == "取得テスト"  # title
    assert task[3] == 2  # quadrant

def test_get_all_tasks(setup_test_db):
    """すべてのタスクを取得するテスト"""
    # 複数のタスクを作成
    create_task("タスク1", None, 1)
    create_task("タスク2", None, 2)
    create_task("タスク3", None, 1)
    
    tasks = get_all_tasks()
    assert len(tasks) == 3

def test_get_tasks_by_quadrant(setup_test_db):
    """象限ごとにタスクを取得するテスト"""
    # 象限1に2つ、象限2に1つ作成
    create_task("Q1タスク1", None, 1)
    create_task("Q1タスク2", None, 1)
    create_task("Q2タスク1", None, 2)
    
    q1_tasks = get_tasks_by_quadrant(1)
    q2_tasks = get_tasks_by_quadrant(2)
    
    assert len(q1_tasks) == 2
    assert len(q2_tasks) == 1

def test_update_task(setup_test_db):
    """タスク更新のテスト"""
    task_id = create_task("元のタイトル", None, 1)
    
    update_task(task_id, title="更新されたタイトル")
    
    task = get_task_by_id(task_id)
    assert task[1] == "更新されたタイトル"

def test_update_task_positions(setup_test_db):
    """タスクの順序を更新するテスト"""
    # 3つのタスクを作成
    task_id1 = create_task("タスク1", None, 1)
    task_id2 = create_task("タスク2", None, 1)
    task_id3 = create_task("タスク3", None, 1)
    
    # 順序を変更（逆順にする）
    update_task_positions(1, [
        (task_id3, 0),
        (task_id2, 1),
        (task_id1, 2)
    ])
    
    # 順序が正しく更新されたことを確認
    tasks = get_tasks_by_quadrant(1)
    assert tasks[0][0] == task_id3  # 最初がtask_id3
    assert tasks[1][0] == task_id2
    assert tasks[2][0] == task_id1

def test_delete_task(setup_test_db):
    """タスク削除のテスト"""
    task_id = create_task("削除テスト", None, 1)
    
    delete_task(task_id)
    
    task = get_task_by_id(task_id)
    assert task is None

def test_task_position_auto_increment(setup_test_db):
    """タスク作成時にpositionが自動で設定されるテスト"""
    task_id1 = create_task("タスク1", None, 1)
    task_id2 = create_task("タスク2", None, 1)
    task_id3 = create_task("タスク3", None, 1)
    
    tasks = get_tasks_by_quadrant(1)
    # positionが0, 1, 2の順になっていることを確認
    assert tasks[0][4] == 0  # position
    assert tasks[1][4] == 1
    assert tasks[2][4] == 2

