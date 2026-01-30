# ACE-Step-MCP

[ACE-Step](https://github.com/ace-step/ACE-Step) のための MCP (Model Context Protocol) サーバー実装です。Claude Desktop や gemini-cli などの MCP 対応クライアントを通じて、直接 ACE-Step モデルを使用して音楽を生成することができます。

## 機能

- **音楽生成**: テキストプロンプトから楽曲を生成します。
- **歌詞のサポート**: 生成される曲に歌詞を指定することができます。
- **カスタマイズ可能**: 曲の長さ、データ型、メモリ管理などのモデルパラメータを設定可能です。
- **GPU アクセラレーション**: CUDA をサポートし、高速な生成が可能です。

## 必要要件

- Python >= 3.10
- CUDA 対応 GPU (強く推奨)
- `uv`

## インストール

1. リポジトリをクローンします:
   ```bash
   git clone https://github.com/NON906/ACE-Step-MCP.git
   cd ACE-Step-MCP
   ```

2. 依存関係をインストールします:
   ```bash
   uv sync
   ```

3. モデルをインストールします。
   ```bash
   uv run ace-step-mcp-download
   ```

## 設定

### Claude Desktop

Claude Desktop で使用するには、`claude_desktop_config.json` に以下の設定を追加してください:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ace-step": {
      "command": "uvx",
      "args": [
        "--directory",
        "/path/to/ACE-Step-MCP",
        "run",
        "ace-step-mcp"
      ],
      "env": {
        "UNLOAD_AFTER_GENERATE": "true"
      }
    }
  }
}
```

> `/path/to/ACE-Step-MCP` は実際のパスに置き換えてください

### gemini-cli

上記を`~/.gemini/settings.json`（もしくは`.gemini/settings.json`）に追加してください

### 環境変数

以下の環境変数を使用してサーバーを設定できます:

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `CHECKPOINT_PATH` | モデルのチェックポイントディレクトリのパス。空の場合、デフォルトのモデルがダウンロードされます。 | "" |
| `TORCH_DTYPE` | PyTorch のデータ型 (例: `float16`, `bfloat16`)。 | `bfloat16` |
| `TORCH_COMPILE` | `true` に設定すると、`torch.compile` を有効にします。 | `false` |
| `CPU_OFFLOAD` | `true` に設定すると、CPU オフロードを有効にします。 | `false` |
| `OVERLAPPED_DECODE` | `true` に設定すると、オーバーラップデコードを有効にします。 | `false` |
| `UNLOAD_AFTER_GENERATE` | `true` に設定すると、生成ごとにモデルを VRAM からアンロードしてメモリを節約します。 | `false` |
| `CUDA_VISIBLE_DEVICES` | 使用する GPU デバイスを指定します (例: "cuda:0")。 | (デフォルト) |

## ツール

### `generate_music`

ACE-Step モデルを使用して音楽を生成します。

**パラメータ:**

- `prompt` (文字列, 必須): 生成する音楽の説明 (例: "upbeat pop song, 120 bpm")。
- `lyrics` (文字列, オプション): 曲の歌詞。デフォルトは "[instrumental]" です。
- `duration` (数値, オプション): 生成するオーディオの長さ（秒）。デフォルトは 60.0 です。
- `output_path` (文字列, オプション): 出力ファイルを保存する特定のパス。指定しない場合、ランダムなファイル名が生成され、カレントディレクトリに保存されます。

## ライセンス

本プロジェクトは、同梱されているライセンスファイルの条項に基づいてライセンスされています。
