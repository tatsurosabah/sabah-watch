# Sabah Watch

サバ州の無国籍・難民に関するニュースを、iPhone のホーム画面から1タップで読むための個人用 PWA。

- 公開URL: https://tatsurosabah.github.io/sabah-watch/
- Google ニュース検索（英語・マレー語）と Google アラートの RSS を **GitHub Actions が1日4回**
  （サバ時間 8時 / 14時 / 20時 / 深夜2時）取得し、
  サバ州の無国籍・難民関連だけに絞り、日本語訳を付けて `news.json` にコミットする。
- アプリ（`index.html` 1枚）は同一オリジンの `news.json` を読むだけ。サーバー不要。
- 既読／保存／タグ／メモは端末内 `localStorage`（キー `sw_state`）にのみ保存される。

## iPhone に入れる

1. Safari で公開URLを開く
2. 共有ボタン → **ホーム画面に追加**
3. 以後はアイコンから全画面（standalone）で起動する

## Google アラートの RSS を追加する（任意）

Google ニュース検索だけでも動くが、アラートを足すと **記事の実URLと抜粋** が取れる
（Google ニュース由来の記事は news.google.com 経由のリンクで、抜粋は付かない）。

なお news.google.com 経由のリンクも、**ブラウザで開けば記事に着地する**（実測で 5/5 成功）。
収集時に実URLへ変換できないだけで、読む分には支障はない。

1. https://www.google.com/alerts を開く
2. 追いたいキーワードのアラートで「オプションを表示」→ **配信先: RSS フィード** を選ぶ
   （メール配信のアラートとは別に、RSS 用のアラートをもう1本作ってもよい）
3. 一覧に出る RSS アイコンのリンク（`https://www.google.com/alerts/feeds/…`）をコピー
4. `feeds.json` の `google_alerts` 配列に貼る:

```json
"google_alerts": [
  "https://www.google.com/alerts/feeds/1234567890/9876543210"
],
```

5. `git push` する。`feeds.json` を変更した push は即座に更新ジョブが走る。

## 収集条件を変える

`feeds.json` の `google_news` にクエリを足す／減らす。`hl` / `ceid` で言語を切り替える
（`en-MY` / `MY:en` = 英語、`ms-MY` / `MY:ms` = マレー語）。

摘発・強制送還のニュース（`Sabah PATI` クエリ由来）が多すぎると感じたら、その1行を消せばよい。

絞り込みとタグ付けのルールは `fetch_news.py` の `SABAH_RE` / `TOPIC_RE` / `TAG_RULES` にある。

## 手元で動かす

```bash
python3 -m http.server 8778 --directory .        # http://localhost:8778
python3 fetch_news.py                            # 取得＋翻訳して news.json を更新
python3 fetch_news.py --no-translate             # 翻訳を飛ばす（動作確認用）
python3 make_icon.py                             # アイコン（サバ州旗）を作り直す
```

macOS の python.org 版で SSL 証明書エラーが出る場合は `SW_INSECURE_SSL=1` を付ける。

## 更新するときの注意

- **`index.html` や `sw.js` を変えたら `sw.js` の `CACHE` の版番号を必ず上げる**
  （`sabah-watch-v1` → `v2`）。上げないと古いキャッシュが残って新版が反映されない。
  `index.html` の `CACHE_LABEL` も揃えておくと設定画面で確認できる。
- `news.json` は Actions が上書きするので、手元で編集しても push 時に競合しやすい。
  ローカルで実行したら `git pull --rebase` してから push する。
- 翻訳は非公式の Google 翻訳エンドポイントを使っている。止まった場合は原文のまま表示され、
  アプリは壊れない（`title_ja` が空になるだけ）。

## ファイル

| ファイル | 役割 |
|---|---|
| `index.html` | アプリ本体（1枚完結） |
| `news.json` | 収集結果。Actions が自動更新 |
| `feeds.json` | 収集元と絞り込みの設定 |
| `fetch_news.py` | 収集・絞り込み・タグ付け・翻訳 |
| `make_icon.py` | アイコン生成（サバ州旗。`LAYOUT` で正方形への収め方を切替） |
| `sw.js` | Service Worker（オフライン表示） |
| `.github/workflows/update.yml` | 1日4回の自動更新 |
