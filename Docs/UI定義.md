# UI定義書

## 2026-01-03 - Monochrome Minimal UI（要望反映）
- Color: Black & White only（no accent colors）
- Language: English labels, minimal wording
- Layout: No sidebar; tasks grid + modal/side detail on card click
- Card: Show only title in grid; tap/click opens detail
- Detail: Open on card click (modal or right-side drawer), shows description/due/controls
- Typography: Smaller sizes overall; prefer system font or Inter/Noto Sans JP (thin weights)
- Spacing: Compact (small padding/margin)
- Borders/Gaps: Minimal; quadrants merge visually; thin hairline dividers at most
- Scroll: Fit in viewport; allow scroll inside quadrants if overflow
- Buttons/Inputs: Monochrome outlines; subtle hover (opacity)
- Export: Keep markdown export button, monochrome

## 1. レイアウト要件

### 1.1 画面サイズとスクロール
- **要件**: スクロールせずに画面内に収まる
- **現在の問題**: 画面が縦に長く、スクロールが必要
- **解決策**:
  - ビューポートの高さ（100vh）を活用
  - 4象限を均等に配置し、画面内に収める
  - ヘッダーとフォームの高さを最小化
  - 各象限内のスクロールは許可（タスクが多い場合）

### 1.2 象限間の境目
- **要件**: 象限間の境目をできるだけなくす
- **現在の問題**: 明確な境界線がある
- **解決策**:
  - グリッドのgapを最小化（0pxまたは非常に小さい値）
  - 境界線を削除または非常に薄く
  - 背景色を統一して境界を目立たせない
  - 視覚的な区切りは色の違いのみで表現

---

## 2. タイポグラフィ

### 2.1 フォントの選択
- **現在**: システムフォント（-apple-system, BlinkMacSystemFont, "Segoe UI"）
- **改善案**:
  - **オプション1**: 現在のシステムフォントを維持（読みやすさ重視）
  - **オプション2**: Google Fontsから選択（例: Inter, Poppins, Noto Sans JP）
  - **オプション3**: 日本語対応のWebフォント（例: Noto Sans JP, M PLUS Rounded 1c）

### 2.2 フォントサイズ
- **見出し（h1）**: 32px → 調整可能
- **象限タイトル（h2）**: 16px → 調整可能
- **タスクタイトル**: 15px → 調整可能
- **本文**: 14px → 調整可能
- **補助テキスト**: 12-13px → 調整可能

### 2.3 フォントウェイト
- **見出し**: 700（Bold）
- **象限タイトル**: 600（SemiBold）
- **タスクタイトル**: 600（SemiBold）
- **本文**: 400（Regular）
- **補助テキスト**: 400-500（Regular-Medium）

### 2.4 行間（line-height）
- **見出し**: 1.2-1.3
- **本文**: 1.5-1.6
- **タスクカード**: 1.5

### 2.5 レタースペーシング（letter-spacing）
- **見出し**: -0.02em（タイトな間隔）
- **本文**: 0（デフォルト）
- **小さいテキスト**: 0.01em（少し広め）

---

## 3. カラースキーム

### 3.1 象限の色
- **第1象限（緊急かつ重要）**: 赤系
  - 現在: `#ff6b6b`
  - 提案: より柔らかい赤（`#ff8787`）またはコーラル系
- **第2象限（重要だが緊急でない）**: 青系
  - 現在: `#4dabf7`
  - 提案: より柔らかい青（`#74c0fc`）またはスカイブルー系
- **第3象限（緊急だが重要でない）**: 黄系
  - 現在: `#ffd43b`
  - 提案: より柔らかい黄色（`#ffec99`）またはアンバー系
- **第4象限（緊急でも重要でもない）**: グレー系
  - 現在: `#868e96`
  - 提案: より柔らかいグレー（`#adb5bd`）またはライトグレー系

### 3.2 背景色
- **メイン背景**: グラデーションまたは単色
  - 現在: グラデーション（`#f5f7fa` → `#c3cfe2`）
  - 提案: より柔らかい単色（`#f7f6f3`）または非常に薄いグレー
- **カード背景**: 白またはオフホワイト
  - 現在: `#f7f6f3`
  - 提案: `#ffffff` または `#fafafa`

### 3.3 テキスト色
- **プライマリテキスト**: `#37352f`（濃いグレー）
- **セカンダリテキスト**: `#787774`（中程度のグレー）
- **ターシャリテキスト**: `#9b9a97`（薄いグレー）

---

## 4. スペーシング

### 4.1 パディング
- **コンテナ**: 24-32px
- **象限**: 20-24px
- **タスクカード**: 16px
- **フォーム**: 32px

### 4.2 マージン
- **象限間**: 0px（境目をなくす）
- **タスクカード間**: 12px
- **セクション間**: 24-32px

### 4.3 グリッドのgap
- **象限間**: 0px（境目をなくす）

---

## 5. シャドウとボーダー

### 5.1 シャドウ
- **カード**: 非常に薄いシャドウ（`rgba(15, 15, 15, 0.05) 0px 1px 2px`）
- **ホバー時**: 少し濃いシャドウ（`rgba(15, 15, 15, 0.1) 0px 2px 4px`）

### 5.2 ボーダー
- **象限**: 1px、非常に薄い色（`rgba(55, 53, 47, 0.09)`）
- **タスクカード**: 1px、非常に薄い色
- **フォーカス時**: 2px、アクセントカラー

---

## 6. アニメーションとトランジション

### 6.1 トランジション
- **ホバー**: 0.2s ease
- **フォーカス**: 0.2s ease
- **ドラッグ&ドロップ**: 150ms

### 6.2 アニメーション
- **カードホバー**: 軽く浮き上がる（`translateY(-1px)`）
- **ボタンホバー**: 軽く浮き上がる
- **フォーカス**: スムーズなアウトライン表示

---

## 7. レスポンシブデザイン

### 7.1 ブレークポイント
- **デスクトップ**: 1200px以上（2x2グリッド）
- **タブレット**: 768px-1199px（2x2グリッド、少し小さく）
- **モバイル**: 767px以下（1列レイアウト）

### 7.2 モバイル対応
- グリッドを1列に変更
- フォントサイズを少し小さく
- パディングを調整

---

## 8. 改善の優先順位

### 高優先度
1. ✅ スクロールせずに画面内に収まる
2. ✅ 象限間の境目をなくす
3. ✅ フォントの改善

### 中優先度
4. カラースキームの調整
5. スペーシングの最適化
6. アニメーションの改善

### 低優先度
7. レスポンシブデザインの改善
8. アクセシビリティの向上

---

## 9. フォントの選択肢（壁打ち用）

### オプション1: システムフォント（現在）
- **メリット**: 読み込みが速い、システムに最適化されている
- **デメリット**: デザインの個性が少ない

### オプション2: Inter（Google Fonts）
- **特徴**: モダンで読みやすい、Notionでも使用
- **メリット**: 洗練された見た目、多言語対応
- **デメリット**: 読み込みが必要

### オプション3: Noto Sans JP（Google Fonts）
- **特徴**: 日本語に最適化、読みやすい
- **メリット**: 日本語の表示が美しい
- **デメリット**: 読み込みが必要、ファイルサイズが大きい

### オプション4: M PLUS Rounded 1c（Google Fonts）
- **特徴**: 丸みを帯びた、親しみやすい
- **メリット**: 柔らかい印象、読みやすい
- **デメリット**: 読み込みが必要

### オプション5: システムフォント + 日本語フォントの組み合わせ
- **英語**: システムフォント（-apple-system等）
- **日本語**: Noto Sans JP または M PLUS Rounded 1c
- **メリット**: 読み込みを最小限に、日本語も美しく
- **デメリット**: 実装が少し複雑

---

## 10. 実装の方向性

### 10.1 レイアウト
```css
/* 画面全体を100vhに収める */
body {
    height: 100vh;
    overflow: hidden;
}

.matrix-grid {
    height: calc(100vh - ヘッダー高さ - フォーム高さ - マージン);
    gap: 0; /* 境目をなくす */
}
```

### 10.2 象限の境目
```css
.quadrant {
    border: none; /* 境界線を削除 */
    border-radius: 0; /* 角を丸めない */
}

/* 最初の象限のみ左上を丸める */
.quadrant-1 {
    border-top-left-radius: 12px;
}

/* 最後の象限のみ右下を丸める */
.quadrant-4 {
    border-bottom-right-radius: 12px;
}
```

### 10.3 フォント
```css
/* オプション1: システムフォント（現在） */
font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;

/* オプション2: Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* オプション3: Noto Sans JP */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
```

---

## 11. 次のステップ

1. **レイアウトの調整**
   - 画面を100vhに収める
   - 象限間のgapを0にする
   - 境界線を削除

2. **フォントの選択**
   - 上記のオプションから選択
   - 実装して確認

3. **細かい調整**
   - スペーシングの最適化
   - カラーの微調整
   - アニメーションの改善

---

## 12. 参考資料

- [Notion Design System](https://www.notion.so/)
- [Google Fonts](https://fonts.google.com/)
- [CSS Variables](https://developer.mozilla.org/ja/docs/Web/CSS/Using_CSS_custom_properties)

