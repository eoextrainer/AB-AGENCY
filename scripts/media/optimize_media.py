from __future__ import annotations

import json
import subprocess
from pathlib import Path


def build_ffmpeg_commands(input_path: Path, output_dir: Path) -> list[list[str]]:
    stem = input_path.stem
    return [
        [
            "ffmpeg",
            "-i",
            str(input_path),
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-preset",
            "medium",
            str(output_dir / f"{stem}.mp4"),
        ],
        [
            "ffmpeg",
            "-i",
            str(input_path),
            "-c:v",
            "libvpx-vp9",
            "-b:v",
            "0",
            "-crf",
            "33",
            str(output_dir / f"{stem}.webm"),
        ],
    ]


def optimize_asset(input_file: str, output_folder: str) -> dict:
    input_path = Path(input_file)
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    commands = build_ffmpeg_commands(input_path, output_dir)
    for command in commands:
        subprocess.run(command, check=True)

    manifest = {
        "source": str(input_path),
        "outputs": [str(output_dir / f"{input_path.stem}.mp4"), str(output_dir / f"{input_path.stem}.webm")],
    }
    (output_dir / f"{input_path.stem}.manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Optimize AB Agency media assets into MP4 and WebM delivery formats.")
    parser.add_argument("input_file")
    parser.add_argument("output_folder")
    args = parser.parse_args()
    optimize_asset(args.input_file, args.output_folder)