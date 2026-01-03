# SQLite

## 2024-01-02 - SQLiteで問題は起こるか

### 質問
SQLiteだったらなにか問題は起こる？

### 回答
タスク管理アプリならSQLiteで問題ありません。

**SQLiteの特徴：**
- ファイルベース（単一ファイルでデータベース）
- サーバー不要（PostgreSQL/MySQLと異なる）
- 軽量で高速
- 設定が簡単

**問題点と対策：**
1. **同時書き込みの制限**
   - 複数ユーザーが同時に書き込むと競合の可能性
   - 対策: 単一ユーザー想定なら問題なし

2. **大規模データには不向き**
   - 数GB以上のデータには不向き
   - 対策: タスク管理なら問題なし（数千〜数万件まで対応可能）

3. **ネットワーク共有には不向き**
   - 複数サーバーからの同時アクセスは非推奨
   - 対策: ローカル開発・単一サーバーなら問題なし

### 重要なポイント
- ファイルベースのデータベース
- サーバー不要で簡単に使える
- 単一ユーザー・小規模データには最適
- タスク管理アプリには十分

### 参考コード例
```python
import sqlite3

# データベース接続
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# テーブル作成
cursor.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        quadrant INTEGER NOT NULL
    )
''')

conn.commit()
conn.close()
```

### 関連トピック
- [データベース設計.md](./データベース設計.md)

---

## 2024-01-02 - SQLiteのテーブルの作り方

### 質問
まずテーブルの作り方を教えてください

### 回答
SQLiteでテーブルを作成する方法を説明します。

### 基本的な流れ

1. **データベースに接続**
2. **SQL文を実行してテーブルを作成**
3. **変更をコミット**
4. **接続を閉じる**

### 基本的なコード例

```python
import sqlite3

# 1. データベースに接続（ファイルがなければ作成される）
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# 2. テーブルを作成するSQL文を実行
cursor.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        quadrant INTEGER NOT NULL CHECK(quadrant IN (1, 2, 3, 4)),
        completed BOOLEAN DEFAULT 0,
        due_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

# 3. 変更をコミット（保存）
conn.commit()

# 4. 接続を閉じる
conn.close()
```

### SQL文の説明

#### CREATE TABLE
```sql
CREATE TABLE テーブル名 (
    カラム名 データ型 制約,
    ...
)
```

#### データ型
- **INTEGER**: 整数
- **TEXT**: 文字列
- **BOOLEAN**: 真偽値（SQLiteでは0/1で保存）

#### 制約
- **PRIMARY KEY**: 主キー（一意の識別子）
- **AUTOINCREMENT**: 自動増分（idを自動で1, 2, 3...と割り当て）
- **NOT NULL**: 必須項目（空欄不可）
- **DEFAULT**: デフォルト値
- **CHECK**: 値のチェック（quadrantは1-4のみ）

### このプロジェクトでのテーブル構造

要件定義書に基づいたテーブル：

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- タスクID（自動採番）
    title TEXT NOT NULL,                   -- タイトル（必須）
    description TEXT,                      -- 説明（任意）
    quadrant INTEGER NOT NULL              -- 象限（1-4、必須）
        CHECK(quadrant IN (1, 2, 3, 4)),
    completed BOOLEAN DEFAULT 0,          -- 完了フラグ（デフォルト: 未完了）
    due_date TEXT,                        -- 期限（任意）
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,  -- 作成日時（自動）
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP   -- 更新日時（自動）
);
```

### 実装のポイント

#### 1. データベースファイルの場所
```python
# プロジェクトルートに tasks.db を作成
conn = sqlite3.connect('tasks.db')

# または、app/ ディレクトリ内に作成
conn = sqlite3.connect('app/tasks.db')
```

#### 2. エラーハンドリング
```python
try:
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE ...')
    conn.commit()
except sqlite3.Error as e:
    print(f"エラーが発生しました: {e}")
finally:
    if conn:
        conn.close()
```

#### 3. テーブルが既に存在する場合
```python
# IF NOT EXISTS を使うと、既に存在していてもエラーにならない
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        ...
    )
''')
```

### 実装の流れ（このプロジェクト）

1. **`app/database.py` を作成**
   - データベース接続関数
   - テーブル作成関数

2. **初期化スクリプトを作成**
   - データベースとテーブルを作成

3. **動作確認**
   - テーブルが作成されているか確認

### 重要なポイント
- `sqlite3.connect()` でデータベースに接続
- `cursor.execute()` でSQL文を実行
- `conn.commit()` で変更を保存
- `conn.close()` で接続を閉じる
- `IF NOT EXISTS` で既存テーブルをチェック

### 次のステップ
1. `app/database.py` にデータベース接続とテーブル作成の関数を実装
2. 初期化スクリプトを作成
3. 動作確認

### 関連トピック
- [データベース設計.md](./データベース設計.md)
- [開発プロセス.md](./開発プロセス.md)

