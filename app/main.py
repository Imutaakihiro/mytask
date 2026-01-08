from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.database import init_db, create_task, get_all_tasks, get_task_by_id, get_tasks_by_quadrant, update_task, update_task_positions, delete_task
from app.models import Task, TaskCreate
from datetime import datetime
from fastapi import HTTPException

# FastAPIアプリケーションインスタンスを作成
app = FastAPI()
# アプリ起動時にデータベースを初期化
@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ データベースの初期化が完了しました！")

# テンプレートエンジンの設定
templates = Jinja2Templates(directory="templates")

# ルートエンドポイント
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/hello")
async def hello():
    return "<p>HTMXが正常に動作しています！</p>"

@app.get("/api/tasks")
async def get_tasks():
    """すべてのタスクを取得"""
    rows = get_all_tasks()
    tasks = []
    for row in rows:
        task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            quadrant=row[3],
            completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
            due_date=datetime.fromisoformat(row[6]) if row[6] else None,
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        )
        tasks.append(task)
    return tasks

@app.post("/api/tasks", response_model=Task)
async def create_new_task(task: TaskCreate):
    """新しいタスクを作成"""
    task_id = create_task(
        title=task.title,
        description=task.description,
        quadrant=task.quadrant,
        due_date=task.due_date.isoformat() if task.due_date else None
    )
    # 作成されたタスクを取得
    row = get_task_by_id(task_id)
    created_task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return created_task

@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """IDでタスクを取得"""
    row = get_task_by_id(task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return task

@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_existing_task(task_id: int, task: TaskCreate):
    """タスクを更新"""
    # タスクが存在するか確認
    existing = get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        quadrant=task.quadrant,
        completed=task.completed,
        due_date=task.due_date.isoformat() if task.due_date else None
    )
    
    # 更新されたタスクを取得
    row = get_task_by_id(task_id)
    updated_task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return updated_task

@app.delete("/api/tasks/{task_id}")
async def delete_existing_task(task_id: int):
    """タスクを削除"""
    # タスクが存在するか確認
    existing = get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    delete_task(task_id)
    return {"message": "Task deleted successfully"}

# HTMX用のHTMLエンドポイント
@app.get("/api/tasks/quadrant/{quadrant_id}", response_class=HTMLResponse)
async def get_tasks_by_quadrant_html(request: Request, quadrant_id: int):
    """指定された象限のタスクをHTMLで取得（順序付き）"""
    rows = get_tasks_by_quadrant(quadrant_id)
    tasks = []
    for row in rows:
        task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            quadrant=row[3],
            completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
            due_date=datetime.fromisoformat(row[6]) if row[6] else None,
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        )
        tasks.append(task)
    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks,
        "quadrant_id": quadrant_id
    })

@app.post("/api/tasks/html", response_class=HTMLResponse)
async def create_task_html(request: Request):
    """HTMX用：タスクを作成してHTMLを返す"""
    form_data = await request.form()
    task_id = create_task(
        title=form_data.get("title"),
        description=form_data.get("description"),
        quadrant=int(form_data.get("quadrant")),
        due_date=form_data.get("due_date") if form_data.get("due_date") else None
    )
    # 作成されたタスクを取得
    row = get_task_by_id(task_id)
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
    })

@app.delete("/api/tasks/{task_id}/html", response_class=HTMLResponse)
async def delete_task_html(request: Request, task_id: int):
    """HTMX用：タスクを削除"""
    existing = get_task_by_id(task_id)
    if not existing:
        return ""  # 既に削除されている場合は空を返す
    delete_task(task_id)
    return ""  # 削除成功時は空を返す（HTMXが要素を削除）

@app.get("/api/tasks/{task_id}/detail", response_class=HTMLResponse)
async def get_task_detail(request: Request, task_id: int):
    """カードクリック時の詳細表示"""
    row = get_task_by_id(task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return templates.TemplateResponse("task_detail.html", {
        "request": request,
        "task": task
    })

@app.put("/api/tasks/{task_id}/html", response_class=HTMLResponse)
async def update_task_html(request: Request, task_id: int):
    """HTMX用：タスクを更新してHTMLを返す"""
    form_data = await request.form()
    existing = get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_task(
        task_id=task_id,
        title=form_data.get("title"),
        description=form_data.get("description") if form_data.get("description") else None,
        due_date=form_data.get("due_date") if form_data.get("due_date") else None
    )
    
    # 更新されたタスクを取得
    row = get_task_by_id(task_id)
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
    })

@app.patch("/api/tasks/{task_id}", response_class=HTMLResponse)
async def patch_task_html(request: Request, task_id: int):
    """HTMX用：タスクを部分更新（完了状態など）"""
    form_data = await request.form()
    existing = get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 完了状態の更新
    completed = form_data.get("completed") == "true"
    update_task(task_id=task_id, completed=completed)
    
    # 更新されたタスクを取得
    row = get_task_by_id(task_id)
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
    })

@app.patch("/api/tasks/{task_id}/quadrant", response_class=HTMLResponse)
async def update_task_quadrant(request: Request, task_id: int):
    """HTMX用：タスクの象限を更新（ドラッグ&ドロップ用）"""
    form_data = await request.form()
    existing = get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_quadrant = int(form_data.get("quadrant"))
    old_quadrant = existing[3]  # 元の象限
    
    # 新しい象限の最大positionを取得して+1
    rows = get_tasks_by_quadrant(new_quadrant)
    new_position = len(rows)  # 最後尾に追加
    
    update_task(task_id=task_id, quadrant=new_quadrant, position=new_position)
    
    # 更新されたタスクを取得
    row = get_task_by_id(task_id)
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
        due_date=datetime.fromisoformat(row[6]) if row[6] else None,
        created_at=datetime.fromisoformat(row[7]),
        updated_at=datetime.fromisoformat(row[8])
    )
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
    })

@app.patch("/api/tasks/quadrant/{quadrant_id}/reorder", response_class=HTMLResponse)
async def reorder_tasks_in_quadrant(request: Request, quadrant_id: int):
    """HTMX用：同じ象限内でのタスクの順序を更新"""
    body = await request.json()
    task_ids = body.get("task_ids", [])  # [task_id1, task_id2, ...] の形式
    
    if not task_ids:
        raise HTTPException(status_code=400, detail="task_ids is required")
    
    # タスクIDとpositionのペアを作成
    task_positions = [(task_id, position) for position, task_id in enumerate(task_ids)]
    update_task_positions(quadrant_id, task_positions)
    
    # 更新後のタスク一覧を取得して返す
    rows = get_tasks_by_quadrant(quadrant_id)
    tasks = []
    for row in rows:
        task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            quadrant=row[3],
            completed=bool(row[5]),
            due_date=datetime.fromisoformat(row[6]) if row[6] else None,
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        )
        tasks.append(task)
    
    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks,
        "quadrant_id": quadrant_id
    })

@app.get("/api/export")
async def export_tasks():
    """Markdownエクスポート（タイトルのみ、簡潔版）"""
    from fastapi.responses import Response
    rows = get_all_tasks()
    
    # 象限ごとにタスクを分類
    quadrants = {1: [], 2: [], 3: [], 4: []}
    quadrant_names = {
        1: "Q1 · 緊急かつ重要",
        2: "Q2 · 重要",
        3: "Q3 · 緊急",
        4: "Q4 · その他"
    }
    
    for row in rows:
        quadrant = row[3]
        task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            quadrant=row[3],
            completed=bool(row[5]),  # positionが追加されたためインデックスが1つずれる
            due_date=datetime.fromisoformat(row[6]) if row[6] else None,
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        )
        quadrants[quadrant].append(task)
    
    # Markdownを生成（タイトルのみ、簡潔版）
    markdown = "# Eisenhower Matrix\n\n"
    markdown += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    markdown += "---\n\n"
    
    for quadrant_id in [1, 2, 3, 4]:
        markdown += f"## {quadrant_names[quadrant_id]}\n\n"
        if not quadrants[quadrant_id]:
            markdown += "—\n\n"
        else:
            for task in quadrants[quadrant_id]:
                checkbox = "- [x]" if task.completed else "- [ ]"
                markdown += f"{checkbox} {task.title}\n"
            markdown += "\n"
    
    # レスポンスを返す
    return Response(
        content=markdown,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="eisenhower-{datetime.now().strftime("%Y%m%d-%H%M")}.md"'
        }
    )