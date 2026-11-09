#!/usr/bin/env python3
"""Encode numbered full-frame PNGs into a checked, looping research GIF."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageSequence


def parse_color(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("matte must be a six-digit hex color")
    try:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("invalid matte color") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frames", type=Path, help="directory of alphabetically numbered PNG frames")
    parser.add_argument("output", type=Path, help="output GIF")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--target-seconds", type=float, default=5.0)
    parser.add_argument("--max-width", type=int, default=960)
    parser.add_argument("--colors", type=int, default=128)
    parser.add_argument("--max-mb", type=float, default=12.0)
    parser.add_argument("--matte", type=parse_color, default=(15, 23, 42))
    args = parser.parse_args()
    if not 5 <= args.fps <= 30 or not 16 <= args.colors <= 256 or args.max_width < 320:
        parser.error("fps must be 5–30, colors 16–256, and max-width at least 320")
    paths = sorted(args.frames.glob("*.png"))
    if not paths:
        parser.error("no PNG frames found")
    nominal_seconds = len(paths) / args.fps
    if abs(nominal_seconds - args.target_seconds) > 0.2:
        parser.error(f"{len(paths)} frames at {args.fps} fps = {nominal_seconds:.2f}s; expected {args.target_seconds:.2f}s")

    rgb_frames: list[Image.Image] = []
    original_size = None
    for path in paths:
        with Image.open(path) as frame:
            if original_size is None:
                original_size = frame.size
            elif frame.size != original_size:
                parser.error(f"frame size differs: {path.name}")
            rgba = frame.convert("RGBA")
            base = Image.new("RGB", rgba.size, args.matte)
            base.paste(rgba, mask=rgba.getchannel("A"))
            if base.width > args.max_width:
                height = round(base.height * args.max_width / base.width)
                base = base.resize((args.max_width, height), Image.Resampling.LANCZOS)
            rgb_frames.append(base)

    # One palette for every frame prevents GIF color flicker.
    sample_count = min(12, len(rgb_frames))
    sample_ids = [round(i * (len(rgb_frames) - 1) / max(1, sample_count - 1)) for i in range(sample_count)]
    thumb_width = 240
    thumb_height = round(thumb_width * rgb_frames[0].height / rgb_frames[0].width)
    grid = Image.new("RGB", (thumb_width * 4, thumb_height * 3), args.matte)
    for slot, index in enumerate(sample_ids):
        thumb = rgb_frames[index].resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        grid.paste(thumb, ((slot % 4) * thumb_width, (slot // 4) * thumb_height))
    # Reserve exact high-contrast accents. A purely frequency-based palette tends
    # to sacrifice thin colored lines and short callouts to large dark backgrounds.
    anchors = [
        (79, 219, 230), (77, 146, 246), (122, 235, 167),
        (250, 112, 119), (176, 137, 255), (241, 247, 255),
        (143, 163, 188), (9, 19, 35), (18, 33, 55),
    ]
    learned_colors = args.colors - len(anchors)
    palette = grid.quantize(colors=learned_colors, method=Image.Quantize.MEDIANCUT)
    palette_data = palette.getpalette()
    for offset, rgb in enumerate(anchors):
        start = (learned_colors + offset) * 3
        palette_data[start : start + 3] = list(rgb)
    palette.putpalette(palette_data)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in rgb_frames]
    durations = [10 * (round((i + 1) * 100 / args.fps) - round(i * 100 / args.fps)) for i in range(len(indexed))]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    indexed[0].save(
        args.output,
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        disposal=1,
        optimize=True,
    )

    with Image.open(args.output) as encoded:
        actual_ms = sum(frame.info.get("duration", 0) for frame in ImageSequence.Iterator(encoded))
        actual_size = encoded.size
        actual_frames = encoded.n_frames
        loop = encoded.info.get("loop")
    size_mb = args.output.stat().st_size / 1_000_000
    print(f"{args.output}: {actual_size[0]}x{actual_size[1]}, {actual_frames} frames, {actual_ms/1000:.2f}s, loop={loop}, {size_mb:.2f} MB")
    if loop != 0 or abs(actual_ms / 1000 - args.target_seconds) > 0.12:
        raise SystemExit("GIF timing or loop metadata failed validation")
    if size_mb > args.max_mb:
        raise SystemExit(f"GIF exceeds {args.max_mb:g} MB; reduce colors, dimensions, or frame count")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
