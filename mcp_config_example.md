# ACE Step MCP サーバー設定例

GitHub へアップロード後、`uvx` のみで実行できます。

## Claude Desktop 設定例

Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ace-step": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/YOUR_GITHUB_USER/ACE-Step-MCP",
        "ace-step-mcp"
      ],
      "env": {
        "CHECKPOINT_PATH": "d:\\path\\to\\your\\model_checkpoint",
        "TORCH_DTYPE": "bfloat16"
      }
    }
  }
}
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `CHECKPOINT_PATH` | モデルのチェックポイントディレクトリ | (空) |
| `TORCH_DTYPE` | torch のデータ型 | `bfloat16` |
| `TORCH_COMPILE` | torch compile を有効化 | (無効) |
| `CPU_OFFLOAD` | CPU オフロードを有効化 | (無効) |
| `OVERLAPPED_DECODE` | オーバーラップデコードを有効化 | (無効) |
