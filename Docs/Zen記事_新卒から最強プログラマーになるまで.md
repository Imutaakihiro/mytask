# 新卒から最強プログラマーになるまで

## はじめに

新卒エンジニアとして入社した頃、私は「プログラマー」という職業に漠然とした憧れを抱いていました。しかし、実際の開発現場では、フレームワークの使い方、データベース設計、アーキテクチャの理解など、学ぶべきことが山積みでした。

この記事では、**HTMX + FastAPI + SQLite** でタスク管理アプリを構築する過程で得た学びと、新卒から「最強プログラマー」を目指すまでの道のりを記録します。

---

## 新卒時代の自分

### 最初の壁

入社当初、私は以下のような状態でした：

- **技術スタックの選択**: ReactやVue.jsなどのモダンフレームワークに慣れ親しんでいたが、なぜその技術を選ぶのか、その判断基準が分からなかった
- **データベース設計**: SQLiteの基本的な使い方は知っていたが、テーブル設計やリレーション設計の原則が理解できていなかった
- **アーキテクチャ**: コードを書くことはできたが、「なぜその構造にするのか」という設計思想が欠けていた

### 気づきの瞬間

ある日、先輩エンジニアから言われた言葉が、私の転機となりました：

> 「技術を学ぶだけでは不十分だ。**なぜその技術を選ぶのか、どう設計するのか**を理解することが重要だ」

この言葉をきっかけに、私は**ハンズオン形式での学習**を始めました。

---

## 転機：HTMXとFastAPIとの出会い

### 技術スタックの選択

プロジェクトで **HTMX + FastAPI + SQLite** を選んだ理由：

1. **HTMX**: 
   - モダンなSPAフレームワークとは異なるアプローチ
   - サーバーサイドレンダリングの良さを再発見
   - シンプルなHTMLでインタラクティブなUIを実現

2. **FastAPI**:
   - Pythonの型安全性を活かしたAPI開発
   - 自動生成されるAPIドキュメント（Swagger UI）
   - 非同期処理のパフォーマンス

3. **SQLite**:
   - シンプルなデータベース設計から学ぶ
   - リレーション設計の基礎を理解
   - マイグレーションの重要性を実感

### 技術スタックの比較

#### HTMX vs 従来のSPAフレームワーク

| 項目 | HTMX | React/Vue/Angular |
|------|------|-------------------|
| **学習コスト** | 低い（HTML属性を追加するだけ） | 高い（JavaScript/TypeScript、状態管理、ビルドツール） |
| **コード量** | 少ない（HTML属性のみ） | 多い（コンポーネント、状態管理、API呼び出し） |
| **SEO** | 強い（サーバーサイドレンダリング） | 弱い（クライアントサイドレンダリング） |
| **複雑なインタラクション** | 不向き | 得意 |
| **リアルタイム更新** | 追加の仕組みが必要 | 対応しやすい |

**実装例の比較：**

**React + Node.jsの場合**
```javascript
// フロントエンド（React）
function TaskList() {
  const [tasks, setTasks] = useState([]);
  
  useEffect(() => {
    fetch('/api/tasks')
      .then(res => res.json())
      .then(data => setTasks(data));
  }, []);
  
  return (
    <div>
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </div>
  );
}
```

**HTMX + FastAPIの場合**
```html
<!-- フロントエンド（HTML + HTMX） -->
<div id="tasks" 
     hx-get="/api/tasks" 
     hx-trigger="load">
  <!-- タスクがここに自動で表示される -->
</div>
```

```python
# バックエンド（FastAPI）
@app.get("/api/tasks")
async def get_tasks():
    tasks = get_all_tasks()
    return render_template("task_list.html", tasks=tasks)
```

**違い：**
- HTMX: JavaScriptを書かずにHTML属性だけで動的になる
- React: JavaScriptで状態管理とDOM操作が必要

#### FastAPI vs 他のバックエンドフレームワーク

| フレームワーク | 言語 | 特徴 | 向いている場面 |
|---------------|------|------|---------------|
| **FastAPI** | Python | モダン、高速、自動ドキュメント生成、非同期処理 | モダンなAPI開発、学習 |
| Flask | Python | シンプル、軽量、柔軟 | 小規模アプリ、カスタマイズ重視 |
| Django | Python | 多機能、大規模向け、ORM内蔵 | 大規模アプリ、管理画面が必要 |
| Express | JavaScript | Node.js用、軽量、柔軟 | Node.jsエコシステム、リアルタイム処理 |
| Rails | Ruby | 規約重視、開発速度重視 | スタートアップ、迅速な開発 |

**FastAPIを選んだ理由：**
- ✅ モダンで高速（非同期処理）
- ✅ 自動APIドキュメント生成（Swagger UI）
- ✅ 型ヒントを活用した開発体験
- ✅ Pythonの学習に最適

#### SQLite vs 他のデータベース

| データベース | 特徴 | 向いている場面 |
|------------|------|---------------|
| **SQLite** | ファイルベース、設定不要、軽量 | 小規模アプリ、単一ユーザー、プロトタイプ |
| PostgreSQL | 高機能、堅牢、拡張性 | 大規模アプリ、複数ユーザー、本番環境 |
| MySQL | 広く使われている、安定性 | 中規模アプリ、既存システムとの連携 |

**SQLiteを選んだ理由：**
- ✅ 設定が簡単（ファイルベース）
- ✅ 単一ユーザー想定のタスク管理アプリに最適
- ✅ データベース設計の基礎を学べる
- ✅ タスク管理には十分な性能

### 技術スタックの全体比較

#### 従来のスタック（SPA）
```
フロントエンド: React/Vue/Angular
  ↓ (JSON API)
バックエンド: Node.js/Python/Java
  ↓
データベース: PostgreSQL/MySQL
```

**特徴：**
- フロントエンドとバックエンドが分離
- APIでJSONをやり取り
- 複雑な状態管理が必要
- SEO対策が難しい
- 学習コストが高い

**必要な技術：**
- JavaScript/TypeScript
- React/Vue/Angular
- 状態管理ライブラリ（Redux、Vuexなど）
- ビルドツール（Webpack、Viteなど）
- API設計

#### HTMX + FastAPIスタック
```
HTML（HTMX属性付き）
  ↓ (HTML)
FastAPI（Python）
  ↓
データベース: SQLite/PostgreSQL
```

**特徴：**
- サーバーサイドでHTMLを生成
- ページ遷移なしで部分更新
- シンプルで理解しやすい
- SEOに強い
- 学習コストが低い

**必要な技術：**
- HTML（基本）
- HTMX（属性を追加するだけ）
- Python（基本）
- FastAPI（フレームワーク）
- データベース（SQLite）

### 重要な学び

**技術を選ぶ基準**を理解することが、プログラマーとしての第一歩でした。

- ✅ プロジェクトの要件に合った技術を選ぶ
- ✅ チームのスキルセットを考慮する
- ✅ 将来の拡張性を考える
- ✅ 学習コストと開発速度のバランスを取る

**このプロジェクトでの選択理由：**
- **HTMX**: 技術習得が目的、シンプルなタスク管理アプリ、JavaScriptを書かなくて良い
- **FastAPI**: Pythonの学習、モダンで高速、自動APIドキュメント生成
- **SQLite**: 設定が簡単、単一ユーザー想定、データベース設計の基礎を学べる

### HTMXとFastAPIだからこその機能

HTMXとFastAPIの組み合わせで実現できる、他のスタックでは難しい機能があります。

#### 1. HTMLフラグメントの返却と部分更新

**HTMXはHTMLを期待する**ため、FastAPIでHTMLフラグメントを返すことで、JavaScriptを書かずに部分更新が可能です。

**実装例：**

```python
# FastAPI: HTMLフラグメントを返す
@app.get("/api/tasks/quadrant/{quadrant_id}", response_class=HTMLResponse)
async def get_tasks_by_quadrant_html(request: Request, quadrant_id: int):
    tasks = get_tasks_by_quadrant(quadrant_id)
    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks
    })
```

```html
<!-- HTMX: HTML属性だけで部分更新 -->
<div id="quadrant-1" 
     hx-get="/api/tasks/quadrant/1"
     hx-trigger="load, refresh from:body"
     hx-swap="innerHTML">
  <!-- タスクが自動で表示される -->
</div>
```

**他のスタックとの違い：**
- **React + Node.js**: JSONを返して、JavaScriptでDOMを操作する必要がある
- **HTMX + FastAPI**: HTMLを返すだけで、HTMXが自動でDOMを更新

#### 2. 同一エンドポイントでJSONとHTMLの両方を返せる

FastAPIの`response_class`と`Accept`ヘッダーを活用することで、**同じエンドポイントでJSONとHTMLの両方を返せます**。

**実装例：**

```python
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Request

@app.get("/api/tasks/{task_id}")
async def get_task(request: Request, task_id: int):
    task = get_task_by_id(task_id)
    
    # AcceptヘッダーでJSONかHTMLかを判定
    accept = request.headers.get("accept", "")
    
    if "text/html" in accept:
        # HTMXリクエスト: HTMLを返す
        return templates.TemplateResponse("task_detail.html", {
            "request": request,
            "task": task
        })
    else:
        # APIリクエスト: JSONを返す
        return JSONResponse(content=task.dict())
```

**メリット：**
- ✅ 同じエンドポイントでHTMXとAPIの両方に対応
- ✅ コードの重複を削減
- ✅ 型安全性を保ちながらHTMLも返せる

#### 3. Jinja2テンプレートエンジンとの組み合わせ

FastAPIはJinja2テンプレートエンジンを標準サポートしており、**サーバーサイドでHTMLを生成**できます。

**実装例：**

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.post("/api/tasks/html", response_class=HTMLResponse)
async def create_task_html(request: Request):
    form_data = await request.form()
    task = create_task(
        title=form_data.get("title"),
        quadrant=int(form_data.get("quadrant"))
    )
    # Jinja2テンプレートでHTMLを生成
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": task
    })
```

**メリット：**
- ✅ サーバーサイドでHTMLを生成（SEOに強い）
- ✅ テンプレートの再利用が容易
- ✅ 型安全なデータをテンプレートに渡せる

#### 4. 非同期処理とHTMXの組み合わせ

FastAPIの非同期処理（`async/await`）とHTMXの組み合わせで、**パフォーマンスを向上**させながら、シンプルなUIを実現できます。

**実装例：**

```python
@app.get("/api/tasks/quadrant/{quadrant_id}", response_class=HTMLResponse)
async def get_tasks_by_quadrant_html(request: Request, quadrant_id: int):
    # 非同期でデータベースから取得
    tasks = await get_tasks_by_quadrant_async(quadrant_id)
    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks
    })
```

**メリット：**
- ✅ 非同期処理でパフォーマンス向上
- ✅ HTMXが自動で部分更新（JavaScript不要）
- ✅ シンプルなコードで高速なアプリを実現

#### 5. 型安全性（Pydantic）とHTMLテンプレートの両立

FastAPIのPydanticモデルで**型安全性を保ちながら**、HTMLテンプレートも使えます。

**実装例：**

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    quadrant: int
    description: str | None = None

@app.post("/api/tasks/html", response_class=HTMLResponse)
async def create_task_html(request: Request, task: TaskCreate):
    # Pydanticでバリデーション（型安全）
    created_task = create_task(
        title=task.title,
        quadrant=task.quadrant,
        description=task.description
    )
    # HTMLテンプレートで返す
    return templates.TemplateResponse("task_card.html", {
        "request": request,
        "task": created_task
    })
```

**メリット：**
- ✅ 型安全性を保ちながらHTMLも返せる
- ✅ バリデーションエラーを自動で検出
- ✅ IDEの補完が効く

#### 6. 部分更新の自動化

HTMXは**自動でDOMを更新**するため、JavaScriptを書かずに部分更新が可能です。

**実装例：**

```html
<!-- タスク追加フォーム -->
<form hx-post="/api/tasks/html"
      hx-target="#quadrant-1"
      hx-swap="afterbegin"
      hx-on::after-request="this.reset(); htmx.trigger('body', 'refresh')">
  <input type="text" name="title" required>
  <button type="submit">追加</button>
</form>

<!-- タスク一覧（自動で更新される） -->
<div id="quadrant-1" 
     hx-get="/api/tasks/quadrant/1"
     hx-trigger="load, refresh from:body"
     hx-swap="innerHTML">
</div>
```

**メリット：**
- ✅ JavaScriptを書かなくて良い
- ✅ サーバーサイドのロジックだけで完結
- ✅ デバッグが簡単（HTMLを見れば分かる）

#### 7. 型安全なAPIとHTMLの両立

FastAPIは**同じエンドポイントで型安全なAPIとHTMLの両方を返せます**。

**実装例：**

```python
# JSON API（型安全）
@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = get_task_by_id(task_id)
    return task  # Pydanticモデルを返す（型安全）

# HTML（HTMX用）
@app.get("/api/tasks/{task_id}/detail", response_class=HTMLResponse)
async def get_task_detail(request: Request, task_id: int):
    task = get_task_by_id(task_id)
    return templates.TemplateResponse("task_detail.html", {
        "request": request,
        "task": task
    })
```

**メリット：**
- ✅ 同じデータモデルをJSONとHTMLの両方で使える
- ✅ 型安全性を保ちながらHTMLも返せる
- ✅ APIドキュメント（Swagger UI）も自動生成される

### まとめ：HTMXとFastAPIの組み合わせの強み

| 機能 | HTMX + FastAPI | 他のスタック |
|------|----------------|-------------|
| **部分更新** | HTML属性だけで自動 | JavaScriptでDOM操作が必要 |
| **型安全性** | Pydanticで型安全 | TypeScriptが必要 |
| **テンプレート** | Jinja2でサーバーサイド生成 | クライアントサイドレンダリング |
| **非同期処理** | `async/await`で高速 | Node.jsでも可能だが複雑 |
| **APIとHTML** | 同じエンドポイントで両方 | 別々のエンドポイントが必要 |
| **学習コスト** | 低い（HTML + Python） | 高い（JavaScript + フレームワーク） |

**HTMXとFastAPIの組み合わせだからこそ実現できること：**
- ✅ JavaScriptを書かずに動的なWebアプリを作れる
- ✅ 型安全性を保ちながらHTMLも返せる
- ✅ サーバーサイドで完結（SEOに強い）
- ✅ シンプルなコードで高速なアプリを実現
- ✅ 学習コストが低い

---

## 実践：ハンズオン形式での学習

### 開発方針の確立

このプロジェクトでは、**AIに頼らず、自分でコードを書く**という方針を貫きました。

#### AIの役割
- 技術的な説明・ガイド
- コードの例示・参考実装
- 質問への回答
- エラーの原因説明と解決方法の提案
- 次のステップの提案

#### 自分の役割
- **自分でコードを書く**
- ハンズオン形式で学習しながら実装
- 不明点があれば質問する

### 段階的な学習の重要性

プロジェクトを以下の順序で進めました：

1. **Phase 0: プロジェクト基盤構築**
   - プロジェクト構造の作成
   - 仮想環境とパッケージインストール
   - 最小限の動作確認

2. **Phase 1: データ層の構築（Infrastructure + Domain）**
   - データベース設計
   - データベース初期化
   - データモデル定義（Pydantic）
   - データアクセス層

3. **Phase 2: API層の構築（Application）**
   - FastAPIアプリケーション作成
   - APIエンドポイント実装（1つずつ）
   - 各エンドポイントの動作確認

4. **Phase 3: UI層の構築（Presentation）**
   - 基本レイアウト作成
   - HTMX統合（機能ごとに）
   - 各機能の動作確認

5. **Phase 4: 高度な機能**
   - ドラッグ&ドロップ実装
   - エクスポート機能

### 重要なポイント

- **小さく始める**: 最小限の例から始める
- **動作確認を頻繁に行う**: 各ステップで必ず動作確認
- **エラーは早めに発見・修正**: 動作する状態を保つ
- **リファクタリングのタイミング**: 動作するコードができたらリファクタリング

---

## 成長：アーキテクチャ設計の理解

### Clean Architectureとの出会い

プロジェクトを進める中で、**Clean Architecture** と **レイヤードアーキテクチャ** の重要性を学びました。

#### レイヤー分離の原則

```
┌─────────────────────────────────┐
│   Presentation Layer (HTMX)    │  ← ユーザーインターフェース
├─────────────────────────────────┤
│   Application Layer (FastAPI)   │  ← ビジネスロジック
├─────────────────────────────────┤
│   Domain Layer (Models)         │  ← データモデル
├─────────────────────────────────┤
│   Infrastructure Layer (DB)     │  ← データベース
└─────────────────────────────────┘
```

#### 依存関係の方向

- 外側のレイヤーは内側のレイヤーに依存する
- 内側のレイヤーは外側のレイヤーに依存しない
- 例: FastAPIはModelsに依存するが、ModelsはFastAPIに依存しない

### ボトムアップアプローチ

**データベース → モデル → API → UI** の順で実装することで、以下のメリットを得ました：

1. **基盤が固まる**: データ層が完成してからUIを実装することで、変更に強い構造になる
2. **テストしやすい**: 各レイヤーを独立してテストできる
3. **理解が深まる**: データの流れを追いながら実装することで、全体像を把握できる

### 重要な学び

- ✅ **設計原則を理解する**: Clean Architecture、DDDなどの名著から学ぶ
- ✅ **実践で体得する**: 理論だけでなく、実際にコードを書いて理解する
- ✅ **段階的に拡張する**: 小さく始めて、動作確認しながら拡張する

---

## 現在：最強プログラマーへの道

### 得られたスキル

このプロジェクトを通じて、以下のスキルを身につけました：

#### 1. 技術スタックの選択力
- プロジェクトの要件に合った技術を選べるようになった
- 技術のトレードオフを理解できるようになった

#### 2. アーキテクチャ設計力
- Clean Architectureの原則を理解し、実践できるようになった
- レイヤー分離の重要性を理解し、保守性の高いコードを書けるようになった

#### 3. 段階的な開発力
- 小さく始めて段階的に拡張する開発手法を身につけた
- 動作確認を頻繁に行い、エラーを早めに発見できるようになった

#### 4. ハンズオン形式での学習力
- AIに頼らず、自分でコードを書く習慣が身についた
- 質問する力、調べる力が向上した

### まだまだ学ぶべきこと

最強プログラマーになるためには、まだまだ学ぶべきことがあります：

- **テスト駆動開発（TDD）**: テストを先に書いてから実装する手法
- **リファクタリング**: 動作するコードを改善する技術
- **パフォーマンス最適化**: アプリケーションの速度を向上させる技術
- **セキュリティ**: セキュアなコードを書く技術
- **チーム開発**: コードレビュー、ペアプログラミングなどの協力手法

---

## まとめ：学びと今後の展望

### 重要な気づき

このプロジェクトを通じて、以下の重要な気づきを得ました：

1. **技術を学ぶだけでは不十分**: なぜその技術を選ぶのか、どう設計するのかを理解することが重要
2. **ハンズオン形式での学習**: AIに頼らず、自分でコードを書くことで、理解が深まる
3. **段階的な開発**: 小さく始めて段階的に拡張することで、エラーを早めに発見できる
4. **アーキテクチャ設計**: Clean Architectureなどの設計原則を理解し、実践することで、保守性の高いコードを書ける

### 今後の展望

最強プログラマーになるため、今後は以下のことに取り組みます：

- ✅ **テスト駆動開発（TDD）の実践**: テストを先に書いてから実装する
- ✅ **リファクタリングの技術**: 動作するコードを改善する技術を学ぶ
- ✅ **パフォーマンス最適化**: アプリケーションの速度を向上させる
- ✅ **セキュリティ**: セキュアなコードを書く技術を学ぶ
- ✅ **チーム開発**: コードレビュー、ペアプログラミングなどの協力手法を学ぶ

### 最後に

新卒から最強プログラマーになるまでの道のりは、まだ始まったばかりです。しかし、このプロジェクトを通じて、**技術を学ぶだけではなく、なぜその技術を選ぶのか、どう設計するのかを理解すること**の重要性を実感しました。

これからも、ハンズオン形式での学習を続け、段階的にスキルを向上させていきます。

---

**参考資料**

- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- [HTMX公式ドキュメント](https://htmx.org/)
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)

---

**プロジェクト情報**

- **リポジトリ**: https://github.com/Imutaakihiro/mytask.git
- **技術スタック**: HTMX + FastAPI + SQLite
- **開発方針**: ハンズオン形式での学習、段階的な開発、Clean Architectureの実践

