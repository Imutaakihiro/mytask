# UI/UX設計

## 2024-01-02 - ドラッグ&ドロップ: Alpine.js vs Sortable.js

### 質問
Alpine.jsのみでも可能ですが、要件定義に合わせてSortable.jsで。どちらが最適？

### 回答
このプロジェクトでは**Sortable.jsが最適**です。

### 簡単な違い

#### Alpine.js
**得意なこと：**
- 表示/非表示の切り替え
- モーダル、ドロップダウン
- フォームのバリデーション
- **ドラッグ&ドロップは苦手**（オマケ機能）

**イメージ：**
```
Alpine.js = スイッチやボタンのようなUI操作が得意
ドラッグ&ドロップ = できるけど、あまり得意じゃない
```

#### Sortable.js
**得意なこと：**
- **ドラッグ&ドロップが専門**
- リスト内の並び替え
- **複数のリスト間での移動**（これが重要！）

**イメージ：**
```
Sortable.js = ドラッグ&ドロップのプロ
「ここからあそこへ移動」が超得意
```

### このプロジェクトで必要なこと

**象限間の移動 = 複数のリスト間での移動**

```
第1象限 → 第2象限
第2象限 → 第3象限
第3象限 → 第4象限
```

**結論：**
- ✅ **Sortable.jsが最適** - ドラッグ&ドロップ専門で、複数リスト間の移動が得意
- ❌ Alpine.js - ドラッグ&ドロップは苦手（他の機能がメイン）

### 簡単に言うと

**Alpine.js:**
- 「表示する/隠す」が得意
- 「ドラッグ&ドロップ」は苦手

**Sortable.js:**
- 「ドラッグ&ドロップ」が専門
- 「ここからあそこへ移動」が超得意

**このプロジェクト:**
- 象限間移動（複数のリスト間）が必要
- → **Sortable.jsが最適！**

### このプロジェクトでの要件

**要件定義書より：**
- 象限間の移動（複数のリスト間での要素移動）
- ドロップ時にHTMXでサーバーに送信
- FastAPIで象限を更新

**判断：**
- ✅ **Sortable.jsが最適**
  - 象限間移動（複数リスト間）に強い
  - HTMXとの連携が容易
  - 要件定義書でも指定されている

### 実装方針

#### Sortable.jsの使い方
```javascript
// 各象限にSortable.jsを適用
const quadrant1 = new Sortable(document.getElementById('quadrant-1'), {
  group: 'quadrants',  // 同じグループ内で移動可能
  animation: 150,
  onEnd: function(evt) {
    // ドロップ時にHTMXでサーバーに送信
    const taskId = evt.item.dataset.taskId;
    const newQuadrant = evt.to.dataset.quadrant;
    htmx.ajax('PATCH', `/api/tasks/${taskId}`, {
      values: {quadrant: newQuadrant}
    });
  }
});
```

#### HTMXとの連携
```html
<div id="quadrant-1" data-quadrant="1">
  <div class="task" data-task-id="1">タスク1</div>
  <div class="task" data-task-id="2">タスク2</div>
</div>
```

### 重要なポイント
- **Sortable.jsが最適**: 象限間移動（複数リスト間）に強い
- HTMXとの連携が容易
- 要件定義書でも指定されている
- Alpine.jsは他のインタラクティブなUI（モーダル、ドロップダウンなど）で使用

### 推奨構成
- **HTMX**: サーバー通信（部分更新、フォーム送信）
- **Sortable.js**: ドラッグ&ドロップ（象限間移動）
- **Alpine.js**: その他のインタラクティブなUI（モーダル、表示/非表示など）

### 参考資料
- [Sortable.js公式ドキュメント](https://sortablejs.github.io/Sortable/)
- [Alpine.js.md](./Alpine.js.md)
- [HTMX.md](./HTMX.md)

### 関連トピック
- [アーキテクチャ設計.md](./アーキテクチャ設計.md)

