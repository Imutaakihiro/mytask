# FastAPI

## 2024-01-02 - FastAPIとは何か

### 質問
HTMXとFastAPIのアプリを作成したい。FastAPIについて知りたい。

### 回答
FastAPIはPythonのWebフレームワークです。

**FastAPIの特徴：**
- モダンで高速
- 自動APIドキュメント生成（Swagger UI）
- 型ヒントを活用
- 非同期処理（async/await）をサポート

**他のフレームワークとの比較：**
- Flask: シンプル、軽量
- Django: 多機能、大規模向け
- FastAPI: モダン、高速、自動ドキュメント

### 重要なポイント
- PythonのWebフレームワーク
- 非同期処理をサポート（async/await）
- 自動でAPIドキュメントを生成
- 型ヒントを活用した開発

### 参考コード例
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    return "<h1>Hello FastAPI</h1>"

@app.get("/api/hello", response_class=HTMLResponse)
async def hello():
    return "<p>Hello from FastAPI!</p>"
```

### 関連トピック
- [HTMX.md](./HTMX.md)
- [Python.md](./Python.md)

---

## 2024-01-02 - FastAPIの基本コード解説（app/main.py）

### 質問
`app/main.py` のコードを詳しく解説してほしい。

### 回答
FastAPIアプリケーションの基本構造について解説します。

**主要なコンポーネント：**

1. **インポート文**
   - `FastAPI`: アプリケーションインスタンスを作成
   - `Jinja2Templates`: HTMLテンプレートエンジン
   - `HTMLResponse`: HTMLレスポンスを返すためのクラス
   - `Request`: HTTPリクエスト情報を扱うオブジェクト

2. **アプリケーションインスタンス**
   - `app = FastAPI()` でアプリケーションを作成
   - このインスタンスにエンドポイントを登録

3. **テンプレートエンジンの設定**
   - `Jinja2Templates(directory="templates")` でテンプレートディレクトリを指定
   - `templates/` ディレクトリ内のHTMLファイルを読み込む

4. **ルートエンドポイント**
   - `@app.get("/")` でルートパスへのGETリクエストを処理
   - `async def` で非同期関数として定義
   - `templates.TemplateResponse()` でHTMLテンプレートをレンダリング

### 重要なポイント
- **非同期処理**: `async def` で定義することで、複数のリクエストを効率的に処理
- **テンプレートエンジン**: Jinja2を使用してHTMLテンプレートに変数を埋め込む
- **リクエストオブジェクト**: FastAPIのテンプレートでは `request` を渡す必要がある

### 参考コード例
```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

# FastAPIアプリケーションインスタンスを作成
app = FastAPI()

# テンプレートエンジンの設定
templates = Jinja2Templates(directory="templates")

# ルートエンドポイント
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

### 動作フロー
1. ユーザーが `http://localhost:8000/` にアクセス
2. FastAPIがGETリクエストを受け取る
3. `read_root()` 関数が呼ばれる
4. `templates/index.html` を読み込んでレンダリング
5. レンダリングされたHTMLをレスポンスとして返す

### 関連トピック
- [HTMX.md](./HTMX.md)
- [Python.md](./Python.md)

---

## 2024-01-02 - エンドポイントとテンプレートエンジンとは何か

### 質問
エンドポイントとテンプレートエンジンとは何か？理解していない。

### 回答
エンドポイントとテンプレートエンジンについて、具体例を使って説明します。

---

## エンドポイント（Endpoint）とは？

### 簡単に言うと
「Webアプリケーションの特定のURL（アドレス）で、特定の処理を行う場所」です。

### 具体例

#### 例1: レストランのメニュー
```
レストランのメニュー:
- 「ハンバーガー」を注文 → キッチンでハンバーガーを作る
- 「サラダ」を注文 → キッチンでサラダを作る
- 「ドリンク」を注文 → キッチンでドリンクを出す
```

#### 例2: Webアプリケーション
```
Webアプリケーション:
- 「/」にアクセス → トップページを表示
- 「/api/tasks」にアクセス → タスク一覧を返す
- 「/api/tasks/1」にアクセス → ID=1のタスクを返す
```

### FastAPIでの例
```python
app = FastAPI()

# エンドポイント1: ルートパス（/）
@app.get("/")  # ← これが「エンドポイント」
def read_root():
    return "トップページ"

# エンドポイント2: /api/hello
@app.get("/api/hello")  # ← これも「エンドポイント」
def hello():
    return "Hello World"

# エンドポイント3: /api/tasks
@app.get("/api/tasks")  # ← これも「エンドポイント」
def get_tasks():
    return ["タスク1", "タスク2"]
```

### エンドポイントの構成要素
```
@app.get("/api/tasks")
     ↑    ↑
     │    └─ URLパス（どこにアクセスするか）
     └─ HTTPメソッド（GET, POST, PUT, DELETEなど）
```

**HTTPメソッドの意味:**
- `GET`: データを取得する（読み取り）
- `POST`: データを作成する（新規作成）
- `PUT`: データを更新する（更新）
- `DELETE`: データを削除する（削除）

### 実際の動作
```
ユーザーがブラウザで http://localhost:8000/ にアクセス
  ↓
FastAPIが「/」というエンドポイントを探す
  ↓
@app.get("/") で定義された関数（read_root）を実行
  ↓
結果を返す（「トップページ」という文字列）
```

### 重要なポイント
- エンドポイント = URLパス + HTTPメソッド + 処理内容
- 複数のエンドポイントを定義できる
- それぞれ異なる処理を行う

---

## テンプレートエンジン（Template Engine）とは？

### 簡単に言うと
「HTMLテンプレートに変数を埋め込んで、動的なHTMLを生成する仕組み」です。

### 具体例

#### 例1: 手紙のテンプレート
```
テンプレート（雛形）:
━━━━━━━━━━━━━━━━━━━━
こんにちは、{{名前}}さん
今日は{{日付}}です。
━━━━━━━━━━━━━━━━━━━━

変数を埋め込む:
名前 = "太郎"
日付 = "2024年1月2日"

結果:
━━━━━━━━━━━━━━━━━━━━
こんにちは、太郎さん
今日は2024年1月2日です。
━━━━━━━━━━━━━━━━━━━━
```

#### 例2: HTMLテンプレート
```
テンプレート（index.html）:
<html>
  <body>
    <h1>こんにちは、{{name}}さん</h1>
    <p>今日は{{date}}です。</p>
  </body>
</html>

変数を埋め込む:
name = "太郎"
date = "2024年1月2日"

結果（レンダリング後）:
<html>
  <body>
    <h1>こんにちは、太郎さん</h1>
    <p>今日は2024年1月2日です。</p>
  </body>
</html>
```

### FastAPIでの例

#### 1. テンプレートファイル（templates/index.html）を作成
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>
    <h1>こんにちは、{{name}}さん</h1>
    <p>現在の時刻: {{time}}</p>
</body>
</html>
```

#### 2. FastAPIでテンプレートエンジンを使う
```python
from fastapi.templating import Jinja2Templates

# テンプレートエンジンの設定
templates = Jinja2Templates(directory="templates")

# エンドポイントでテンプレートを使う
@app.get("/")
async def read_root(request: Request):
    # 変数を定義
    context = {
        "request": request,  # FastAPIで必須
        "title": "ホームページ",
        "name": "太郎",
        "time": "2024年1月2日 12:00"
    }
    
    # テンプレートに変数を埋め込んでHTMLを生成
    return templates.TemplateResponse("index.html", context)
```

### テンプレートエンジンのメリット
1. **HTMLとデータを分離できる**
   - HTMLは `templates/` ディレクトリに
   - データはPythonコードで管理

2. **同じテンプレートで異なるデータを表示できる**
   ```python
   # ユーザー1用
   context = {"name": "太郎"}
   
   # ユーザー2用
   context = {"name": "花子"}
   ```

3. **ループや条件分岐が使える**
   ```html
   {% for task in tasks %}
       <p>{{task.title}}</p>
   {% endfor %}
   ```

### 重要なポイント
- テンプレートエンジン = HTMLテンプレート + 変数 → 動的なHTMLを生成
- Jinja2 = Pythonでよく使われるテンプレートエンジン
- `{{変数名}}` で変数を表示
- `{% コマンド %}` でループや条件分岐

---

## 3つの概念の関係

```
1. インスタンス（app = FastAPI()）
   ↓
2. エンドポイント（@app.get("/")）
   ↓
3. テンプレートエンジン（templates.TemplateResponse()）
   ↓
   動的なHTMLを生成して返す
```

### 実際のコードでの関係
```python
# 1. インスタンスを作る
app = FastAPI()

# 2. テンプレートエンジンを設定
templates = Jinja2Templates(directory="templates")

# 3. エンドポイントを定義
@app.get("/")  # ← エンドポイント
async def read_root(request: Request):
    # 4. テンプレートエンジンでHTMLを生成
    return templates.TemplateResponse("index.html", {"request": request})
```

### 関連トピック
- [Python.md](./Python.md)
- [HTMX.md](./HTMX.md)

---

## 2024-01-02 - app/main.pyの各行の詳細解説

### 質問
`app/main.py` のコードをもっと細かく、何をしているのかを知りたい。

### 回答
各行が何をしているか、内部でどのような処理が行われているかを詳しく解説します。

### 1-4行目: インポート文

#### 1行目: `from fastapi import FastAPI`
- FastAPIパッケージから `FastAPI` クラスをインポート
- Webアプリケーションの基盤クラス
- このクラスでアプリを作成し、ルーティングやミドルウェアを管理

#### 2行目: `from fastapi.templating import Jinja2Templates`
- FastAPIのテンプレート機能から `Jinja2Templates` をインポート
- 内部でJinja2を使用してHTMLテンプレートをレンダリング
- テンプレートファイルの読み込みと変数の埋め込みを担当

#### 3行目: `from fastapi.responses import HTMLResponse`
- HTMLレスポンス用のクラスをインポート
- レスポンスのContent-Typeを `text/html` に設定
- ブラウザがHTMLとして解釈するためのヘッダーを付与

#### 4行目: `from fastapi import Request`
- HTTPリクエスト情報を扱う `Request` をインポート
- リクエストヘッダー、クエリパラメータ、パスパラメータなどにアクセス可能
- テンプレートに渡すために使用

### 7行目: FastAPIアプリケーションインスタンスの作成

#### 何をしているか
1. `FastAPI()` を呼び出してインスタンスを作成
2. 内部でルーティングテーブル、ミドルウェアスタック、依存関係注入システムなどを初期化
3. この `app` にエンドポイントを登録

#### 内部で起こっていること
```python
# 内部的には以下のような処理が行われています
app = FastAPI()
# ↓ 内部的に
# - ルーティングテーブルを初期化
# - ミドルウェアスタックを初期化
# - 依存関係注入システムを初期化
# - OpenAPIスキーマの準備
```

### 10行目: テンプレートエンジンの設定

#### 何をしているか
1. `Jinja2Templates` のインスタンスを作成
2. `directory="templates"` でテンプレートディレクトリを指定
3. 内部でJinja2の環境を初期化し、テンプレートの読み込み準備

#### 内部で起こっていること
```python
# 内部的には以下のような処理が行われています
templates = Jinja2Templates(directory="templates")
# ↓ 内部的に
# - Jinja2の環境（Environment）を作成
# - テンプレートローダーを設定（templates/ディレクトリから読み込む）
# - テンプレートのキャッシュを準備
```

### 13行目: デコレータ（エンドポイントの登録）

#### 何をしているか
1. `@app.get("/")` でルートパス（`/`）へのGETリクエストを処理するエンドポイントを登録
2. `response_class=HTMLResponse` でレスポンスタイプをHTMLに指定

#### デコレータの動作
```python
# デコレータは以下のような処理を行います
@app.get("/", response_class=HTMLResponse)
# ↓ 内部的に
# 1. 次の関数（read_root）を受け取る
# 2. その関数を app のルーティングテーブルに登録
# 3. URLパス: "/"
# 4. HTTPメソッド: GET
# 5. レスポンスクラス: HTMLResponse
# 6. 関数: read_root
```

### 14行目: 関数の定義

#### 何をしているか
1. `async def` で非同期関数を定義
2. `request: Request` でリクエスト情報を受け取る

#### `async def` の意味
- 非同期関数として定義
- 複数のリクエストを同時に処理可能
- I/O待ち（データベースアクセスなど）の間に他のリクエストを処理

#### `request: Request` の意味
- HTTPリクエスト情報を含むオブジェクト
- テンプレートに渡すために必要（FastAPIのテンプレート機能の要件）
- リクエストヘッダー、クエリパラメータなどにもアクセス可能

### 15行目: テンプレートレスポンスの返却

#### 何をしているか
1. `templates.TemplateResponse()` を呼び出し
2. `"index.html"` を指定してテンプレートを読み込む
3. `{"request": request}` でテンプレートに変数を渡す
4. レンダリングされたHTMLをレスポンスとして返す

#### 内部で起こっていること（ステップごと）

**ステップ1: テンプレートファイルの読み込み**
```
templates/index.html を読み込む
```

**ステップ2: テンプレートの解析**
```
Jinja2がテンプレートを解析
- {{変数名}} を探す
- {% コマンド %} を探す
```

**ステップ3: 変数の埋め込み**
```
{"request": request} の変数をテンプレートに埋め込む
- テンプレート内で {{request}} があれば、requestオブジェクトを埋め込む
```

**ステップ4: HTMLの生成**
```
レンダリングされたHTMLを生成
例:
<html>
  <body>
    <h1>Hello</h1>
  </body>
</html>
```

**ステップ5: レスポンスオブジェクトの作成**
```
HTMLResponseオブジェクトを作成
- Content-Type: text/html
- ステータスコード: 200
- ボディ: レンダリングされたHTML
```

### 全体の動作フロー（詳細版）

```
1. ユーザーがブラウザで http://localhost:8000/ にアクセス
   ↓
2. ブラウザがHTTPリクエストを送信
   - メソッド: GET
   - パス: /
   ↓
3. FastAPIがリクエストを受け取る
   - ルーティングテーブルを確認
   - "/" というパスと "GET" というメソッドの組み合わせを探す
   ↓
4. @app.get("/") で登録された関数（read_root）を見つける
   ↓
5. read_root(request) を実行
   - requestオブジェクトにはリクエスト情報が含まれている
   ↓
6. templates.TemplateResponse() を呼び出す
   - templates/index.html を読み込む
   - テンプレートを解析
   - 変数を埋め込む
   - HTMLを生成
   ↓
7. HTMLResponseオブジェクトを返す
   - Content-Type: text/html
   - ステータスコード: 200
   - ボディ: レンダリングされたHTML
   ↓
8. FastAPIがHTTPレスポンスを送信
   ↓
9. ブラウザがHTMLを受け取って表示
```

### 重要なポイント
- **非同期処理**: `async def` で複数のリクエストを同時に処理可能
- **テンプレートエンジン**: Jinja2でHTMLテンプレートに変数を埋め込む
- **リクエストオブジェクト**: FastAPIのテンプレート機能では必須
- **レスポンスクラス**: ブラウザがHTMLとして解釈するためのヘッダーを設定

### 関連トピック
- [Python.md](./Python.md)
- [HTMX.md](./HTMX.md)


