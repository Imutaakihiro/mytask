"""
FastAPIアプリケーションのテスト
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, get_all_tasks, delete_task
import os

# テスト用のデータベースファイル名
TEST_DATABASE = "test_tasks.db"

@pytest.fixture(scope="function")
def client():
    """テスト用のクライアントを作成"""
    # テスト用のデータベースに切り替え
    import app.database as db_module
    original_db = db_module.DATABASE
    db_module.DATABASE = TEST_DATABASE
    
    # データベースを初期化
    init_db()
    
    # テストクライアントを作成
    client = TestClient(app)
    
    yield client
    
    # テスト後にクリーンアップ
    # テスト用データベースを削除
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)
    
    # 元のデータベース名に戻す
    db_module.DATABASE = original_db

def test_read_root(client):
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Eisenhower Matrix" in response.text

def test_hello_endpoint(client):
    """/api/hello エンドポイントのテスト"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert "HTMXが正常に動作しています" in response.text

def test_get_tasks_empty(client):
    """空のタスク一覧を取得するテスト"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_create_task(client):
    """タスクを作成するテスト"""
    task_data = {
        "title": "テストタスク",
        "description": "これはテストです",
        "quadrant": 1,
        "completed": False
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 200
    
    task = response.json()
    assert task["title"] == "テストタスク"
    assert task["description"] == "これはテストです"
    assert task["quadrant"] == 1
    assert task["completed"] == False
    assert "id" in task
    assert "created_at" in task

def test_get_task_by_id(client):
    """IDでタスクを取得するテスト"""
    # まずタスクを作成
    task_data = {
        "title": "取得テスト",
        "quadrant": 2
    }
    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # IDでタスクを取得
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == "取得テスト"

def test_get_task_not_found(client):
    """存在しないタスクIDで取得するテスト"""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404

def test_update_task(client):
    """タスクを更新するテスト"""
    # まずタスクを作成
    task_data = {
        "title": "更新前",
        "quadrant": 1
    }
    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # タスクを更新
    update_data = {
        "title": "更新後",
        "description": "更新されました",
        "quadrant": 2,
        "completed": True
    }
    response = client.put(f"/api/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "更新後"
    assert task["description"] == "更新されました"
    assert task["quadrant"] == 2
    assert task["completed"] == True

def test_delete_task(client):
    """タスクを削除するテスト"""
    # まずタスクを作成
    task_data = {
        "title": "削除テスト",
        "quadrant": 1
    }
    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # タスクを削除
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    
    # 削除されたことを確認
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404

def test_get_tasks_by_quadrant(client):
    """象限ごとにタスクを取得するテスト"""
    # 複数のタスクを作成
    for i in range(3):
        task_data = {
            "title": f"タスク{i+1}",
            "quadrant": 1
        }
        client.post("/api/tasks", json=task_data)
    
    # 象限1のタスクを取得
    response = client.get("/api/tasks/quadrant/1")
    assert response.status_code == 200
    assert "タスク1" in response.text

def test_create_task_html(client):
    """HTMX用：タスクを作成してHTMLを返すテスト"""
    form_data = {
        "title": "HTMLタスク",
        "quadrant": "1",
        "description": "HTMLテスト"
    }
    response = client.post("/api/tasks/html", data=form_data)
    assert response.status_code == 200
    assert "HTMLタスク" in response.text

def test_task_quadrant_validation(client):
    """象限のバリデーションテスト（1-4の範囲外）"""
    task_data = {
        "title": "無効な象限",
        "quadrant": 5  # 無効な値
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 422  # バリデーションエラー

def test_task_title_required(client):
    """タイトルが必須であることのテスト"""
    task_data = {
        "quadrant": 1
        # titleが欠けている
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 422  # バリデーションエラー

