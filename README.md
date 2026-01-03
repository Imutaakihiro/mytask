# アイゼンハワー・マトリックスタスク管理アプリ

HTMX + FastAPI + SQLite で構築するタスク管理アプリケーション

## 技術スタック

- **フロントエンド**: HTMX + HTML + CSS
- **バックエンド**: FastAPI (Python)
- **データベース**: SQLite

## プロジェクト構造

```
プロジェクト/
├── app/                    # アプリケーション層
│   ├── __init__.py
│   ├── main.py            # FastAPIアプリケーション
│   ├── models.py          # データモデル（Pydantic）
│   ├── database.py        # データベース接続・操作
│   └── routers/           # APIルーター
├── templates/             # HTMXテンプレート
├── static/                # CSS、JavaScript
├── tests/                 # テストコード
├── requirements.txt
└── README.md
```

## 開発方針

詳細は `.cursor/rules/devrules.mdc` を参照してください。

## 要件定義

詳細は `Docs/要件定義書.md` を参照してください。

