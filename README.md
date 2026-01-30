# ACE-Step-MCP

(日本語のREADMEは[README_ja.md](README_ja.md)を参照してください)

An MCP (Model Context Protocol) Server implementation for [ACE-Step](https://github.com/ace-step/ACE-Step), allowing you to generate music using the ACE-Step model directly through MCP-compatible clients like Claude Desktop or gemini-cli.

## Features

- **Music Generation**: Generate music tracks from text prompts.
- **Lyrics Support**: Optionally specify lyrics for the generated song.
- **Customizable**: Configure model parameters like duration, data type, and memory management.
- **GPU Acceleration**: Supports CUDA for fast generation.

## Requirements

- Python >= 3.10
- CUDA-enabled GPU (strongly recommended)
- `uv`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NON906/ACE-Step-MCP.git
   cd ACE-Step-MCP
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Install the model:
   ```bash
   uv run ace-step-mcp-download
   ```

## Configuration

### Claude Desktop

To use this with Claude Desktop, add the following configuration to your `claude_desktop_config.json`:

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

> Replace `/path/to/ACE-Step-MCP` with the actual path.

### gemini-cli

Add the configuration above to `~/.gemini/settings.json` (or `.gemini/settings.json`).

### Environment Variables

You can configure the server using the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `CHECKPOINT_PATH` | Path to the model checkpoint directory. If empty, the default model is downloaded. | "" |
| `TORCH_DTYPE` | Data type for PyTorch (e.g., `float16`, `bfloat16`). | `bfloat16` |
| `TORCH_COMPILE` | Set to `true` to enable `torch.compile`. | `false` |
| `CPU_OFFLOAD` | Set to `true` to enable CPU offloading. | `false` |
| `OVERLAPPED_DECODE` | Set to `true` to enable overlapped decoding. | `false` |
| `UNLOAD_AFTER_GENERATE` | Set to `true` to unload the model from VRAM after each generation to save memory. | `false` |
| `CUDA_VISIBLE_DEVICES` | Specify the GPU device ID to use (e.g., "cuda:0"). | (Default) |

## Tools

### `generate_music`

Generates music using the ACE-Step model.

**Parameters:**

- `prompt` (string, required): Description of the music to generate (e.g., "upbeat pop song, 120 bpm").
- `lyrics` (string, optional): Lyrics for the song. Default is "[instrumental]".
- `duration` (number, optional): Duration of the generated audio in seconds. Default is 60.0.
- `output_path` (string, optional): specific path to save the output file. If not provided, a random filename is generated in the current directory.

## License

This project is licensed under the terms of the included license file.
