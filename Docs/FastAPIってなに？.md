# FastAPIってなに？ - 未経験エンジニア向けガイド

## はじめに

この記事は、**プログラミング未経験の方**や**Web開発を始めたばかりの方**に向けて、FastAPIをわかりやすく説明します。

専門用語はできるだけ避け、具体例を多く使って説明します。

---

## 1. FastAPIとは何か？

### 1.1 超シンプルに言うと

**FastAPI = PythonでWebアプリを作るための便利なツール**

PythonでWebアプリを作る時、**「どこにアクセスしたら、どんな処理をするか」**を簡単に定義できるフレームワークです。

### 1.2 具体例で理解する

#### FastAPIなしの場合（難しい）

```python
# FastAPIなしだと、こんなに複雑...
import http.server
import socketserver

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Hello</h1>')
        elif self.path == '/api/hello':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"message": "Hello"}')
        # ... もっと複雑なコードが必要

# サーバーを起動
server = socketserver.TCPServer(("", 8000), MyHandler)
server.serve_forever()
```

**問題点：**
- コードが複雑
- 理解しにくい
- 機能を追加するのが大変

#### FastAPIを使った場合（簡単）

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "<h1>Hello</h1>"

@app.get("/api/hello")
def hello():
    return {"message": "Hello"}
```

**メリット：**
- コードがシンプル
- 理解しやすい
- 機能を追加しやすい

### 1.3 FastAPIは「言語」ではない

よくある誤解：
- ❌ FastAPIは新しいプログラミング言語
- ❌ FastAPIはPythonの代わり

正しい理解：
- ✅ FastAPIは**Pythonのフレームワーク**（ツールの一種）
- ✅ Pythonで書く
- ✅ Webアプリを作るための便利な機能がたくさんある

---

## 2. なぜFastAPIが生まれたのか？

### 2.1 Web開発の歴史

#### 昔のWeb開発（2000年代）

```
PythonでWebアプリを作る
  ↓
CGI（Common Gateway Interface）を使う
  ↓
コードが複雑、遅い
```

**特徴：**
- シンプルな仕組み
- でも、コードが複雑、遅い

#### 現代のWeb開発（2010年代～）

```
PythonでWebアプリを作る
  ↓
FlaskやDjangoなどのフレームワークを使う
  ↓
コードが簡単、速い
```

**特徴：**
- フレームワークでコードが簡単
- でも、まだ改善の余地がある

### 2.2 FastAPIの登場（2018年）

FastAPIは「**シンプルさと速さを両立**」するために生まれました。

```
PythonでWebアプリを作る
  ↓
FastAPIを使う
  ↓
コードが簡単、超速い、自動でドキュメント生成
```

**特徴：**
- ✅ コードが簡単（Flaskより簡単）
- ✅ 超速い（Node.jsやGoと同等の速度）
- ✅ 自動でAPIドキュメントを生成
- ✅ 型安全性（エラーを早く発見できる）

---

## 3. 他のフレームワークとの違い

### 3.1 PythonのWebフレームワーク比較

| フレームワーク | 特徴 | 向いている場面 |
|---------------|------|---------------|
| **FastAPI** | モダン、高速、自動ドキュメント | モダンなAPI開発、学習 |
| Flask | シンプル、軽量、柔軟 | 小規模アプリ、カスタマイズ重視 |
| Django | 多機能、大規模向け、ORM内蔵 | 大規模アプリ、管理画面が必要 |

### 3.2 コードの比較

#### Flaskの場合

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def read_root():
    return "<h1>Hello</h1>"

@app.route("/api/hello")
def hello():
    return {"message": "Hello"}
```

**特徴：**
- シンプル
- でも、自動ドキュメント生成がない
- 型安全性が弱い

#### FastAPIの場合

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "<h1>Hello</h1>"

@app.get("/api/hello")
def hello():
    return {"message": "Hello"}
```

**特徴：**
- シンプル（Flaskと同じくらい）
- ✅ 自動でAPIドキュメントを生成（`/docs`にアクセス）
- ✅ 型安全性が強い（エラーを早く発見）

### 3.3 速度の比較

| フレームワーク | 速度 |
|-------------|------|
| FastAPI | ⚡ 超速い（Node.jsやGoと同等） |
| Flask | 🐢 普通 |
| Django | 🐢 普通 |

**なぜFastAPIが速いのか？**
- 非同期処理（`async/await`）をサポート
- 複数のリクエストを同時に処理できる

---

## 4. FastAPIの基本的な使い方

### 4.1 準備：FastAPIをインストール

まず、FastAPIをインストールします。

```bash
pip install fastapi uvicorn
```

**説明：**
- `fastapi`: FastAPI本体
- `uvicorn`: Webサーバー（FastAPIを動かすためのもの）

### 4.2 最小限のアプリ

#### ステップ1: ファイルを作成

`main.py`というファイルを作成します。

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**説明：**
- `from fastapi import FastAPI`: FastAPIを読み込む
- `app = FastAPI()`: アプリケーションを作成
- `@app.get("/")`: 「/」にアクセスした時の処理を定義
- `def read_root()`: 処理内容を定義
- `return {"message": "Hello World"}`: JSONを返す

#### ステップ2: サーバーを起動

```bash
uvicorn main:app --reload
```

**説明：**
- `main`: ファイル名（`main.py`）
- `app`: アプリケーションの変数名（`app = FastAPI()`）
- `--reload`: コードを変更したら自動で再起動

#### ステップ3: ブラウザで確認

ブラウザで `http://localhost:8000` にアクセスします。

**結果：**
```json
{"message": "Hello World"}
```

### 4.3 エンドポイントとは？

**エンドポイント = 「どこにアクセスしたら、どんな処理をするか」を定義する場所**

#### 具体例

```python
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello"}
```

**説明：**
- `@app.get("/")`: 「/」にアクセスしたら、`read_root()`を実行
- `@app.get("/api/hello")`: 「/api/hello」にアクセスしたら、`hello()`を実行

#### 動作の流れ

```
ユーザーがブラウザで http://localhost:8000/ にアクセス
  ↓
FastAPIが「/」というエンドポイントを探す
  ↓
@app.get("/") で定義された関数（read_root）を実行
  ↓
{"message": "Hello World"} を返す
  ↓
ブラウザに表示される
```

### 4.4 HTTPメソッドとは？

**HTTPメソッド = リクエストの種類**

| メソッド | 意味 | 例 |
|---------|------|-----|
| `GET` | データを取得する（読み取り） | タスク一覧を取得 |
| `POST` | データを作成する（新規作成） | 新しいタスクを作成 |
| `PUT` | データを更新する（更新） | タスクを更新 |
| `DELETE` | データを削除する（削除） | タスクを削除 |

#### 実装例

```python
# GET: タスク一覧を取得
@app.get("/api/tasks")
def get_tasks():
    return [{"id": 1, "title": "タスク1"}]

# POST: 新しいタスクを作成
@app.post("/api/tasks")
def create_task(task: dict):
    # タスクを作成する処理
    return {"id": 2, "title": task["title"]}

# PUT: タスクを更新
@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    # タスクを更新する処理
    return {"id": task_id, "title": task["title"]}

# DELETE: タスクを削除
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    # タスクを削除する処理
    return {"message": "削除しました"}
```

---

## 5. 実際の例：タスク管理アプリ

### 5.1 タスク一覧を取得する

#### Python（バックエンド）

```python
@app.get("/api/tasks")
async def get_tasks():
    """すべてのタスクを取得"""
    tasks = [
        {"id": 1, "title": "タスク1", "completed": False},
        {"id": 2, "title": "タスク2", "completed": True}
    ]
    return tasks
```

**説明：**
- `@app.get("/api/tasks")`: 「/api/tasks」にGETリクエストが来たら実行
- `async def`: 非同期関数（複数のリクエストを同時に処理できる）
- `return tasks`: タスク一覧をJSONで返す

#### 動作

```
ユーザーがブラウザで http://localhost:8000/api/tasks にアクセス
  ↓
FastAPIがGETリクエストを受け取る
  ↓
get_tasks() を実行
  ↓
タスク一覧をJSONで返す
  ↓
ブラウザに表示される
```

### 5.2 タスクを作成する

#### Python（バックエンド）

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    """新しいタスクを作成"""
    # タスクを作成する処理
    new_task = {
        "id": 3,
        "title": task.title,
        "completed": task.completed
    }
    return new_task
```

**説明：**
- `TaskCreate`: タスクのデータ構造を定義（Pydanticモデル）
- `@app.post("/api/tasks")`: 「/api/tasks」にPOSTリクエストが来たら実行
- `task: TaskCreate`: リクエストのデータを自動でバリデーション（検証）

#### 動作

```
ユーザーがフォームからタスクを送信
  ↓
FastAPIがPOSTリクエストを受け取る
  ↓
リクエストのデータを自動でバリデーション
  ↓
create_task() を実行
  ↓
新しいタスクをJSONで返す
```

### 5.3 HTMLを返す（HTMXと組み合わせる）

#### Python（バックエンド）

```python
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/tasks/html", response_class=HTMLResponse)
async def create_task_html(request: Request):
    form_data = await request.form()
    title = form_data.get("title")
    
    # タスクを作成
    task = {"id": 1, "title": title}
    
    # HTMLを返す（HTMX用）
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
    })
```

**説明：**
- `response_class=HTMLResponse`: HTMLを返すことを指定
- `Jinja2Templates`: HTMLテンプレートエンジン（変数を埋め込める）
- `templates.TemplateResponse()`: HTMLテンプレートをレンダリング

#### 動作

```
HTMXが /api/tasks/html にPOSTリクエストを送信
  ↓
FastAPIがHTMLフラグメントを返す
  ↓
HTMXが自動で画面に挿入
  ↓
ページ全体はリロードされない
```

---

## 6. FastAPIの特徴的な機能

### 6.1 自動APIドキュメント生成

FastAPIは、**自動でAPIドキュメントを生成**します。

#### 使い方

1. サーバーを起動
   ```bash
   uvicorn main:app --reload
   ```

2. ブラウザで `http://localhost:8000/docs` にアクセス

3. **Swagger UI**が表示される

**特徴：**
- ✅ すべてのエンドポイントが表示される
- ✅ リクエストとレスポンスの形式が表示される
- ✅ 実際にAPIを試せる（「Try it out」ボタン）

#### 例

```python
@app.get("/api/tasks")
async def get_tasks():
    return [{"id": 1, "title": "タスク1"}]
```

**自動で生成されるドキュメント：**
- エンドポイント: `GET /api/tasks`
- レスポンス: `[{"id": 1, "title": "タスク1"}]`
- 実際に試せるボタン

### 6.2 型安全性（Pydantic）

FastAPIは、**型安全性**をサポートしています。

#### 例

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str  # 文字列である必要がある
    completed: bool = False  # 真偽値、デフォルトはFalse

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    return task
```

**メリット：**
- ✅ 間違ったデータが来たら、自動でエラーを返す
- ✅ IDE（エディタ）で補完が効く
- ✅ エラーを早く発見できる

#### 動作

```
正しいデータ:
{"title": "タスク1", "completed": false}
  ↓
✅ 正常に処理される

間違ったデータ:
{"title": 123, "completed": "yes"}
  ↓
❌ 自動でエラーを返す
```

### 6.3 非同期処理（async/await）

FastAPIは、**非同期処理**をサポートしています。

#### 例

```python
@app.get("/api/tasks")
async def get_tasks():
    # データベースから取得（時間がかかる）
    tasks = await get_tasks_from_database()
    return tasks
```

**メリット：**
- ✅ 複数のリクエストを同時に処理できる
- ✅ 速い（データベースの待ち時間に他のリクエストを処理）

#### 比較

**同期処理（遅い）:**
```
リクエスト1 → データベース待ち（3秒） → レスポンス
リクエスト2 → データベース待ち（3秒） → レスポンス
合計: 6秒
```

**非同期処理（速い）:**
```
リクエスト1 → データベース待ち（3秒） ↘
リクエスト2 → データベース待ち（3秒） → 同時に処理
合計: 3秒
```

---

## 7. FastAPIのメリット・デメリット

### 7.1 メリット

#### ✅ コードが簡単

```python
@app.get("/")
def read_root():
    return {"message": "Hello"}
```

- シンプルで理解しやすい
- 機能を追加しやすい

#### ✅ 超速い

- Node.jsやGoと同等の速度
- 非同期処理で複数のリクエストを同時に処理

#### ✅ 自動でAPIドキュメントを生成

- `/docs`にアクセスするだけで、すべてのAPIが確認できる
- 実際にAPIを試せる

#### ✅ 型安全性

- 間違ったデータが来たら、自動でエラーを返す
- エラーを早く発見できる

#### ✅ 学習コストが低い

- Pythonの基本だけ知っていれば使える
- 複雑な設定が不要

### 7.2 デメリット

#### ❌ 比較的新しい（2018年）

- 情報が少ない場合がある
- でも、公式ドキュメントが充実している

#### ❌ 大規模アプリには不向きな場合がある

- Djangoの方が、大規模アプリには適している場合がある
- でも、多くの企業で使われている

---

## 8. よくある質問（FAQ）

### Q1: FastAPIは新しい技術ですか？

**A:** はい、2018年にリリースされた比較的新しい技術です。でも、**Pythonの標準的な機能を使っている**ため、安定しています。

### Q2: FastAPIはFlaskやDjangoの代わりになりますか？

**A:** 場合によります。
- **シンプルなAPI**: FastAPIが最適
- **大規模なアプリ**: Djangoの方が適している場合がある
- **カスタマイズ重視**: Flaskの方が適している場合がある

### Q3: FastAPIを使うには、Pythonの知識は必要ですか？

**A:** はい、必要です。でも、**Pythonの基本だけ**知っていれば使えます。

### Q4: FastAPIは本番環境で使えますか？

**A:** はい、使えます。多くの企業で使われています。

### Q5: FastAPIとHTMXは一緒に使えますか？

**A:** はい、一緒に使えます。実際、このプロジェクトでも使っています。

---

## 9. まとめ

### FastAPIとは

- **PythonでWebアプリを作るための便利なツール**
- **コードが簡単、超速い、自動でドキュメント生成**
- **学習コストが低い**（Pythonの基本だけ）

### 向いている場面

- ✅ モダンなAPI開発
- ✅ シンプルなWebアプリ
- ✅ 学習・プロトタイプ
- ✅ HTMXと組み合わせた開発

### 向いていない場面

- ❌ 大規模なアプリ（Djangoの方が適している場合がある）
- ❌ 複雑なカスタマイズが必要（Flaskの方が適している場合がある）

### 次のステップ

1. **FastAPIの公式ドキュメントを読む**
   - https://fastapi.tiangolo.com/

2. **実際にコードを書いてみる**
   - 簡単な例から始める
   - タスク管理アプリを作ってみる

3. **HTMXと組み合わせてみる**
   - FastAPIでHTMLを返す
   - HTMXで部分更新

---

**参考資料**

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [FastAPIのチュートリアル](https://fastapi.tiangolo.com/tutorial/)
- [FastAPIのGitHub](https://github.com/tiangolo/fastapi)

---

**作成日**: 2024-01-02  
**対象読者**: プログラミング未経験者、Web開発初心者

