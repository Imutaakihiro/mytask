# Alpine.js

## 2024-01-02 - Alpine.jsとは

### 質問
alpine.js これはなに？

### 回答
Alpine.jsは、軽量でシンプルなJavaScriptフレームワークです。HTMLに直接インタラクティブな機能を追加できます。

**Alpine.jsの特徴：**
- **軽量**: 圧縮後のサイズが約7.1kBと非常に小さい
- **簡単な導入**: CDN経由でスクリプトタグを追加するだけで使用開始
- **宣言的な記述**: HTML属性を使用してデータのバインディングやイベントのハンドリング
- **jQueryのような手軽さ**と**Vue.jsのような宣言的な記述**を組み合わせた

**Vue.jsやReactとの違い：**
- Vue.js/React: 大規模なフレームワーク、学習コストが高い
- Alpine.js: 軽量、HTMLに直接書ける、学習コストが低い

### 重要なポイント
- 軽量でシンプルなJavaScriptフレームワーク
- HTML属性でインタラクティブな機能を追加
- HTMXと組み合わせて使うことが多い
- 小規模なプロジェクトや既存のHTMLに機能を追加したい場合に適している

### 主なディレクティブ

#### x-data
コンポーネントごとにデータを定義
```html
<div x-data="{ open: false }">
  <!-- コンポーネントのデータ -->
</div>
```

#### x-show
要素の表示・非表示を切り替え
```html
<div x-show="open">
  コンテンツが表示されます
</div>
```

#### x-on (@)
イベントの監視（クリックなど）
```html
<button @click="open = !open">切り替え</button>
```

#### x-bind (:)
HTMLの属性にデータをバインド
```html
<input :value="message" />
```

### 参考コード例

#### 基本的な例
```html
<div x-data="{ open: false }">
  <button @click="open = !open">切り替え</button>
  <div x-show="open">
    コンテンツが表示されます
  </div>
</div>
```

#### HTMXと組み合わせた例
```html
<!-- HTMXで部分更新、Alpine.jsでインタラクティブなUI -->
<div x-data="{ showModal: false }">
  <button 
    hx-get="/api/tasks"
    hx-target="#tasks"
    @click="showModal = true"
  >
    タスクを取得
  </button>
  
  <div x-show="showModal" class="modal">
    <div id="tasks"></div>
  </div>
</div>
```

### HTMXとAlpine.jsの使い分け

**HTMX:**
- サーバーとの通信（部分更新）
- フォーム送信
- ページ遷移なしの更新

**Alpine.js:**
- クライアント側のインタラクティブなUI
- ドロップダウン、モーダル、アコーディオン
- 状態管理（表示/非表示の切り替えなど）

### 読み込み方法

#### 開発用（CDN）
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.5/dist/cdn.min.js"></script>
```

#### 本番用（ローカルファイル）
```html
<script defer src="/static/alpine.min.js"></script>
```

### 参考資料
- [Alpine.js公式ドキュメント](https://alpinejs.dev/)
- [HTMX.md](./HTMX.md)

### 関連トピック
- [HTMX.md](./HTMX.md)
- [UI-UX設計.md](./UI-UX設計.md)


