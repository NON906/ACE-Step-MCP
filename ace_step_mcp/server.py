from mcp.server.fastmcp import FastMCP
import os
import uuid
import sys
from typing import Optional
from pydantic import BaseModel, Field

from acestep.pipeline_ace_step import ACEStepPipeline


# Response schemas
class GenerateMusicResponse(BaseModel):
    """Response schema for generate_music tool."""
    result: str
    output_path: Optional[str] = Field(default=None, description="Path to the generated audio file")
    error: Optional[str] = Field(default=None, description="Error message if generation failed")


# Initialize FastMCP
mcp = FastMCP("ACE-Step-MCP")

# Load model configuration from environment variables
checkpoint_path = os.getenv("CHECKPOINT_PATH", "")
dtype = os.getenv("TORCH_DTYPE", "bfloat16")
torch_compile = bool(os.getenv("TORCH_COMPILE", ""))
cpu_offload = bool(os.getenv("CPU_OFFLOAD", ""))
overlapped_decode = bool(os.getenv("OVERLAPPED_DECODE", ""))

print(f"Loading ACEStepPipeline with checkpoint={checkpoint_path}, dtype={dtype}...", file=sys.stderr)

# Initialize the pipeline globally
try:
    model_demo = ACEStepPipeline(
        checkpoint_dir=checkpoint_path,
        dtype=dtype,
        torch_compile=torch_compile,
        cpu_offload=cpu_offload,
        overlapped_decode=overlapped_decode
    )
    print("ACEStepPipeline loaded successfully.", file=sys.stderr)
except Exception as e:
    print(f"Failed to load ACEStepPipeline: {e}", file=sys.stderr)
    model_demo = None


@mcp.tool()
def generate_music(
    prompt: str,
    lyrics: str = "[instrumental]",
    duration: float = 60.0,
    output_path: Optional[str] = None
) -> GenerateMusicResponse:
    """
    Generate music using ACE Step.

    Args:
        prompt: Music prompts to generate (e.g. "funk, pop, soul, 105 BPM")
        lyrics: Lyrics for the song (default: "[instrumental]")
        duration: Output length in seconds (default: 60.0)
        output_path: Optional output file path. If not provided, a random UUID name will be used.
    
    Returns:
        GenerateMusicResponse with success status and output_path or error.
    """
    if model_demo is None:
        return GenerateMusicResponse(result="error", error="Model failed to initialize. Check server logs.")

    # Determine output path
    if not output_path:
        output_path = f"output_{uuid.uuid4().hex}.mp3"
    
    # Handle relative paths
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    
    # Ensure directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Generating music for prompt: '{prompt}'...", file=sys.stderr)
    try:
        model_demo(
            format=os.path.splitext(output_path)[1][1:],
            audio_duration=duration,
            prompt=prompt,
            lyrics=lyrics,
            save_path=output_path
        )
        return GenerateMusicResponse(result="success", output_path=output_path)
    except Exception as e:
        return GenerateMusicResponse(result="error", error=str(e))


def main():
    mcp.run()


if __name__ == "__main__":
    main()
