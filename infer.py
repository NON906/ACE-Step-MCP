import click
import os
import uuid

from acestep.pipeline_ace_step import ACEStepPipeline


@click.command()
@click.option("--prompt", type=str, help="Music prompts to generate (English preferred) (Example: funk, pop, soul, rock, melodic, guitar, drums, bass, keyboard, percussion, 105 BPM, energetic, upbeat, groovy, vibrant, dynamic)")
@click.option("--lyrics", type=str, default="[instrumental]", help="Lyrics")
@click.option("--duration", type=float, default=60.0, help="Output length (seconds)")
@click.option("--output_path", type=str, default=None, help="Output file path")
def main(prompt, lyrics, duration, output_path):
    #os.environ["CUDA_VISIBLE_DEVICES"] = str(device_id)

    checkpoint_path = os.getenv("CHECKPOINT_PATH", "")
    dtype = os.getenv("TORCH_DTYPE", "bfloat16")
    torch_compile = bool(os.getenv("TORCH_COMPILE", ""))
    cpu_offload = bool(os.getenv("CPU_OFFLOAD", ""))
    overlapped_decode = bool(os.getenv("OVERLAPPED_DECODE", ""))

    model_demo = ACEStepPipeline(
        checkpoint_dir=checkpoint_path,
        dtype=dtype,
        torch_compile=torch_compile,
        cpu_offload=cpu_offload,
        overlapped_decode=overlapped_decode
    )

    output_path = output_path or f"output_{uuid.uuid4().hex}.mp4"
    if os.path.dirname(output_path) == "":
        output_path = "./" + output_path

    model_demo(
        format=os.path.splitext(output_path)[1][1:],
        audio_duration=duration,
        prompt=prompt,
        lyrics=lyrics,
        save_path=output_path
    )

    print(f"Success: {output_path}")

if __name__ == "__main__":
    main()
