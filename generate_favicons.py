#!/usr/bin/env python3
"""
Generate all favicon sizes from the source SVG.

Requires: pip install pillow cairosvg

Generates:
- favicon.ico (multi-size: 16x16, 32x32, 48x48)
- favicon-48.png, favicon-96.png, favicon-192.png
- apple-touch-icon.png (180x180)
"""

import os
import sys
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install pillow cairosvg")
    sys.exit(1)

ROOT = Path(__file__).parent
SOURCE_SVG = ROOT / 'assets/brand/favicon-source.svg'
OUTPUT_DIR = ROOT

# Icon sizes to generate
PNG_SIZES = [16, 32, 48, 96, 192, 180]  # 180 is apple-touch-icon
ICO_SIZES = [16, 32, 48]


def generate_png(svg_path, output_path, size):
    """Generate a PNG from SVG at the specified size."""
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(output_path),
        output_width=size,
        output_height=size
    )
    print(f"Generated {output_path.name} ({size}x{size})")


def generate_ico(png_paths, output_path):
    """Generate a multi-size ICO from PNG files."""
    images = [Image.open(p) for p in png_paths]
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images]
    )
    print(f"Generated {output_path.name} (multi-size ICO)")


def main():
    if not SOURCE_SVG.exists():
        print(f"Error: Source SVG not found at {SOURCE_SVG}")
        sys.exit(1)

    print(f"Generating favicons from {SOURCE_SVG.name}...")

    # Generate PNGs
    temp_pngs = {}
    for size in PNG_SIZES:
        if size == 180:
            # Apple touch icon
            output_path = OUTPUT_DIR / 'apple-touch-icon.png'
        else:
            output_path = OUTPUT_DIR / f'favicon-{size}.png'
        
        generate_png(SOURCE_SVG, output_path, size)
        temp_pngs[size] = output_path

    # Generate multi-size ICO from the ICO_SIZES PNGs
    ico_pngs = [temp_pngs[size] for size in ICO_SIZES]
    ico_path = OUTPUT_DIR / 'favicon.ico'
    generate_ico(ico_pngs, ico_path)

    print("\nAll favicons generated successfully!")
    print("\nGenerated files:")
    print(f"  - favicon.ico (16, 32, 48)")
    print(f"  - favicon-48.png, favicon-96.png, favicon-192.png")
    print(f"  - apple-touch-icon.png (180x180)")


if __name__ == '__main__':
    main()
