# HTMX

## 2024-01-02 - HTMXとは何か

### 質問
HTMXとPythonのアプリを作りたい。HTMXがどんな言語なのか0から教えてほしい。

### 回答
HTMXは「言語」ではなく、HTMLを拡張するJavaScriptライブラリです。

**HTMXの特徴：**
- HTMLに属性を追加するだけで動的なWebアプリが作れる
- JavaScriptを書かなくても、ページ遷移なしの部分更新が可能
- サーバーサイドでHTMLを生成する従来のアプローチを現代化

**従来のWeb開発との違い：**
- 従来: JavaScriptでAPIを呼び出し、DOMを操作
- HTMX: HTML属性（hx-get, hx-postなど）で自動的に部分更新

### 重要なポイント
- HTMXはHTMLを拡張するライブラリ（言語ではない）
- JavaScriptを書かなくても動的なWebアプリが作れる
- ページ遷移なしで部分更新が可能
- 学習コストが低い

### 参考コード例
```html
<!-- HTMXの基本例 -->
<button 
    hx-get="/api/hello"
    hx-target="#result"
    hx-swap="innerHTML"
>
    クリックしてね！
</button>

<div id="result">
    <!-- ここに結果が表示される -->
</div>
```

### 関連トピック
- [FastAPI.md](./FastAPI.md)
- [アーキテクチャ設計.md](./アーキテクチャ設計.md)

---

## 2024-01-02 - HTMXのCDNと本番運用

### 質問
HTMXはCDNで読み込める？本番運用でもCDNを使っていい？

### 回答
HTMXはCDNで読み込めますが、本番運用では推奨されません。

**HTMXの読み込み方法：**

1. **CDN（開発用）**
   ```html
   <script src="https://unpkg.com/htmx.org@1.9.10"></script>
   ```
   - 開発時は便利
   - 外部通信が発生する
   - `latest`を使うとアップデートで既存コードが動かなくなる可能性

2. **ローカルファイル（本番推奨）**
   - スクリプトをダウンロードして`static/`に配置
   - 外部通信が不要
   - バージョンを固定できる

**本番運用での推奨：**
- ✅ スクリプトをダウンロードして`static/`に配置
- ✅ バージョンを固定（例: `htmx.org@1.9.10`）
- ❌ CDNの`latest`は使わない

**HTMXと一緒によく使われるライブラリ：**
- **Alpine.js** - インタラクティブなUI（ドロップダウン、モーダルなど）
- **Tailwind CSS** - スタイリング
- **PicoCSS** - 軽量なCSSフレームワーク

### 重要なポイント
- 開発時はCDNでOK
- 本番運用ではローカルファイルを推奨
- バージョンを固定する
- Alpine.jsと組み合わせることが多い

### 参考コード例
```html
<!-- 開発用（CDN） -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- 本番用（ローカルファイル） -->
<script src="/static/htmx.min.js"></script>
```

### 参考リポジトリ
- https://github.com/motty93/htmx-alpine.js-tutorial
- https://github.com/motty93/mh3g-judge-table

### 関連トピック
- [FastAPI.md](./FastAPI.md)

