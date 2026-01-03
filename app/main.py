from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.database import init_db, create_task, get_all_tasks, get_task_by_id, update_task, delete_task
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
            completed=bool(row[4]),
            due_date=datetime.fromisoformat(row[5]) if row[5] else None,
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
    """指定された象限のタスクをHTMLで取得"""
    rows = get_all_tasks()
    tasks = []
    for row in rows:
        if row[3] == quadrant_id:  # quadrantカラム
            task = Task(
                id=row[0],
                title=row[1],
                description=row[2],
                quadrant=row[3],
                completed=bool(row[4]),
                due_date=datetime.fromisoformat(row[5]) if row[5] else None,
                created_at=datetime.fromisoformat(row[6]),
                updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
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
    update_task(task_id=task_id, quadrant=new_quadrant)
    
    # 更新されたタスクを取得
    row = get_task_by_id(task_id)
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        quadrant=row[3],
        completed=bool(row[4]),
        due_date=datetime.fromisoformat(row[5]) if row[5] else None,
        created_at=datetime.fromisoformat(row[6]),
        updated_at=datetime.fromisoformat(row[7])
    )
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
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
            completed=bool(row[4]),
            due_date=datetime.fromisoformat(row[5]) if row[5] else None,
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7])
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