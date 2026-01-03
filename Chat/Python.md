# Python

## 2024-01-02 - models.pyの役割

### 質問
models.py の役割はなに？

### 回答
`models.py` は**Domain Layer（ドメイン層）**の一部で、データモデルとビジネスルールを定義するファイルです。

### models.pyの役割

#### 1. データの構造を定義
- タスクデータがどのような構造か定義
- どのフィールドが必要か、どのフィールドが任意か

#### 2. バリデーション（検証）
- データが正しい形式かチェック
- 例: `quadrant` が1-4の範囲内か

#### 3. FastAPIでの使用
- リクエストデータのバリデーション
- レスポンスデータの構造定義

### レイヤードアーキテクチャでの位置

```
┌─────────────────────────────────┐
│   Presentation Layer (HTMX)  │
├─────────────────────────────────┤
│   Application Layer (FastAPI)   │  ← models.pyを使う
├─────────────────────────────────┤
│   Domain Layer (Models)         │  ← models.py（ここ！）
│   - app/models.py               │    データモデル、ビジネスルール
├─────────────────────────────────┤
│   Infrastructure Layer (DB)     │
│   - app/database.py             │
└─────────────────────────────────┘
```

### Pydanticとは？

**Pydantic = データバリデーションライブラリ**

- Pythonの型ヒントを使ってデータを検証
- FastAPIと統合されている
- 自動でバリデーションとシリアライゼーション

### 具体例

#### models.pyで定義
```python
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    quadrant: int  # 1-4
    completed: bool = False
```

#### FastAPIで使用
```python
from app.models import Task

@app.post("/api/tasks")
async def create_task(task: Task):  # ← 自動でバリデーション
    # task.title が正しい形式か自動でチェック
    # task.quadrant が1-4の範囲かチェック
    return task
```

### データベースとの関係

```
データベース（SQLite）
  ↓
database.py（データ取得）
  ↓
models.py（データ構造を定義）
  ↓
FastAPI（APIエンドポイント）
```

**流れ：**
1. データベースからデータを取得（`database.py`）
2. データをTaskモデルに変換（`models.py`）
3. FastAPIがTaskモデルをJSONに変換して返す

### 重要なポイント
- Domain Layer（ドメイン層）の一部
- データの構造とバリデーションルールを定義
- FastAPIでリクエスト/レスポンスのバリデーションに使われる
- ビジネスルール（例: quadrantは1-4のみ）を定義

### 関連トピック
- [アーキテクチャ設計.md](./アーキテクチャ設計.md)
- [FastAPI.md](./FastAPI.md)
- [SQLite.md](./SQLite.md)

---

## 2024-01-02 - インスタンスとは何か

### 質問
インスタンスとは何か？理解していない。

### 回答
インスタンスは「設計図（クラス）から作られた実物」です。

### 具体例

#### 例1: 車の設計図と実物
```
設計図（クラス）: 「車」という設計図
  ↓ 設計図から作る
実物（インスタンス）: 実際の車（トヨタのプリウス、ホンダのフィットなど）
```

#### 例2: Pythonコードで理解する
```python
# 設計図（クラス）の定義
class Car:
    def __init__(self, name):
        self.name = name
    
    def drive(self):
        print(f"{self.name}が走ります")

# 設計図から実物（インスタンス）を作る
car1 = Car("プリウス")  # ← これが「インスタンス」
car2 = Car("フィット")  # ← これも「インスタンス」

# インスタンスを使う
car1.drive()  # 「プリウスが走ります」と表示
car2.drive()  # 「フィットが走ります」と表示
```

### FastAPIでの例
```python
# FastAPIという「設計図（クラス）」から
# 実物（インスタンス）を作る
app = FastAPI()  # ← これが「インスタンス」

# このインスタンスを使って、エンドポイントを登録する
@app.get("/")  # ← appというインスタンスを使っている
def read_root():
    return "Hello"
```

### 重要なポイント
- **クラス** = 設計図（「車」という概念）
- **インスタンス** = 実物（実際の車「プリウス」）
- インスタンスを作ることを「インスタンス化」と言う
- `app = FastAPI()` でFastAPIのインスタンスを作成

### 関連トピック
- [FastAPI.md](./FastAPI.md)

