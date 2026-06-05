# MiMo-Nexus

<p align="center">
  <strong>Token 効率的な AI コーディングのための軽量 MCP インテリジェントゲートウェイ</strong>
</p>

<p align="center">
  <a href="#インストール">インストール</a> •
  <a href="#クイックスタート">クイックスタート</a> •
  <a href="#機能">機能</a> •
  <a href="#api-リファレンス">API リファレンス</a> •
  <a href="README.md">English</a> •
  <a href="README_zh.md">中文</a>
</p>

---

## 概要

MiMo-Nexus は、AI コーディングアシスタント（Claude Code、Cursor など）からの大規模コードベース分析リクエストを傍受し、Xiaomi MiMo 2.5 Pro API にオフロードする軽量 MCP（Model Context Protocol）ゲートウェイです。

**問題点：** AI アシスタントが大規模プロジェクトを読み取る際、大量のトークンを消費し、高額な API 請求書とコンテキストオーバーフローが発生します。

**解決策：** MiMo-Nexus はスマートプロキシとして機能し、ローカルコードをスキャンし、効率的にパッケージングして、MiMo 2.5 Pro の 1M コンテキストウィンドウ（約 $1/M トークン）に送信し、簡潔な分析結果を AI アシスタントに返します。

**結果：** より深いコード分析を実現しながら、トークンコストを 60-95% 節約。

## 機能

- **Token 効率的な分析** - コードベース全体の分析を MiMo 2.5 Pro の 1M コンテキストウィンドウにオフロード
- **OpenAI 互換 API** - シームレスな統合のために標準 OpenAI SDK を使用
- **思考モデルサポート** - Gemini フォーマットで MiMo 2.5 Omni の推論チェーンにアクセス
- **音声フィードバック** - MiMo TTS を使用して音声ビルド通知を生成
- **スマートファイルフィルタリング** - .git、node_modules、バイナリファイルなどの無関係なファイルを自動スキップ
- **MCP プロトコル** - MCP 対応の AI アシスタントですぐに動作

## インストール

### 前提条件

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー
- [platform.xiaomimimo.com](https://platform.xiaomimimo.com) から取得した MiMo API キー

### uv でインストール（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/t0ri333/mimo-nexus-mcp.git
cd mimo-nexus-mcp

# 依存関係をインストール
uv sync

# 環境テンプレートをコピー
cp .env.example .env

# .env を編集して API キーを追加
# XIAOMI_MIMO_API_KEY=your_key_here
```

### PyPI からインストール（公開後）

```bash
pip install mimo-nexus-mcp
```

## クイックスタート

### 1. API キーを設定

```bash
# 環境テンプレートをコピー
cp .env.example .env

# .env を編集して API キーを追加
# https://platform.xiaomimimo.com でキーを取得
XIAOMI_MIMO_API_KEY=your_key_here
```

### 2. Claude Code に登録

```bash
# MCP サーバーをグローバルに登録
claude mcp add \
  --env XIAOMI_MIMO_API_KEY=$XIAOMI_MIMO_API_KEY \
  --transport stdio \
  mimo-nexus \
  -- uv run server.py
```

### 3. ワークフローで使用

Claude Code で、次のように質問するだけです：

```
このプロジェクトの認証モジュールを分析し、潜在的なセキュリティ脆弱性を特定してください。
```

Claude Code は自動的に MiMo-Nexus を呼び出し、以下を実行します：
1. ローカルソースファイルをスキャン
2. 構造化ペイロードにパッケージング
3. MiMo 2.5 Pro に送信して詳細分析
4. 簡潔なレポートを返却（数千トークンを節約）

## API リファレンス

### MCP ツール

#### `mimo_global_repo_analyzer`

MiMo 2.5 Pro の 1M コンテキストにオフロードしてコードベース全体を分析。

**パラメータ：**
- `directory_path` (str)：プロジェクトディレクトリの絶対パス
- `architectural_query` (str)：分析の具体的な質問または焦点
- `model` (str, オプション)：モデル ID（デフォルト：`mimo-v2.5-pro`）
- `use_thinking` (bool, オプション)：`mimo-v2.5-omni` の思考モードを有効化

**戻り値：** ファイル参照と具体的な推奨事項を含む詳細な分析レポート。

#### `mimo_code_query`

完全な分析なしでコードベースについて簡単なクエリ。

**パラメータ：**
- `question` (str)：コードに関する具体的な質問
- `directory_path` (str, オプション)：プロジェクトルートディレクトリ（デフォルト：`.`）
- `model` (str, オプション)：モデル ID（デフォルト：`mimo-v2.5-pro`）

**戻り値：** プロジェクト構造に基づいた簡潔な回答。

#### `mimo_voice_broadcaster`

MiMo TTS を使用して音声フィードバックを生成。

**パラメータ：**
- `report_text` (str)：音声に変換するテキストコンテンツ
- `vibe_style` (str, オプション)：感情トーンプリセット
  - `professional_engineer`：冷静で正確なシニアエンジニア
  - `urgent_warning`：不安なシステム管理者の警告
  - `calm_success`：ビルド成功後の温かい満足感
  - `hacker_cyberpunk`：早口のサイバーパンクハッカー

**戻り値：** `audio_path`（ローカルファイルパス）と `metadata` を含む辞書。

## サポートされているモデル

| モデル | ID | フォーマット | コンテキスト | 用途 |
|--------|-----|-------------|-------------|------|
| MiMo 2.5 Pro | `mimo-v2.5-pro` | OpenAI | 1Mトークン | コード分析、アーキテクチャレビュー |
| MiMo 2.5 | `mimo-v2.5` | OpenAI | 1Mトークン | 軽量クエリ |
| MiMo 2.5 Omni | `mimo-v2.5-omni` | OpenAI / Gemini | 1Mトークン | 推論チェーン付き思考モード |

## 設定

### 環境変数

| 変数 | 必須 | 説明 |
|------|------|------|
| `XIAOMI_MIMO_API_KEY` | はい | MiMo API キー |

### 推論パラメータ

ゲートウェイは MiMo の公式推奨に基づいた最適化パラメータを使用：

| パラメータ | 標準モデル | 思考モデル |
|-----------|-----------|-----------|
| Temperature | 0.3 | 1.0 |
| Top P | 0.95 | 0.95 |

## アーキテクチャ

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Claude Code    │────▶│  MiMo-Nexus      │────▶│  MiMo 2.5 Pro   │
│  (ローカル AI)  │◀────│  MCP ゲートウェイ │◀────│  API (クラウド) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        │                   ┌────┴────┐
        │                   │ ローカル│
        │                   │ ファイル│
        │                   └─────────┘
        ▼
  簡潔な結果 (300トークン)
  生コードではなく (80,000トークン)
```

## 貢献

貢献を歓迎します！まず[貢献ガイド](CONTRIBUTING.md)をお読みください。

## ライセンス

MIT ライセンス - 詳細は [LICENSE](LICENSE) を参照。

## 謝辞

- MCP プロトコル処理に [FastMCP](https://github.com/jlowin/fastmcp) を使用
- [Xiaomi MiMo 2.5 Pro](https://platform.xiaomimimo.com) によるクラウド推論
- [headroom](https://github.com/anthropics/headroom) のトークン最適化コンセプトに着想
