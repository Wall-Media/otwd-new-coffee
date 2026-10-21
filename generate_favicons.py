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
import struct
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


def generate_png(svg_path, output_path, size, background=None):
    """Generate a PNG from SVG at the specified size with optional background color."""
    if background:
        # Create PNG with background color
        from io import BytesIO
        # First render the SVG to PNG
        png_bytes = cairosvg.svg2png(
            url=str(svg_path),
            output_width=size,
            output_height=size
        )
        # Open it with PIL and add background
        foreground = Image.open(BytesIO(png_bytes))
        # Create background image
        background_img = Image.new('RGB', (size, size), background)
        # Paste foreground onto background (using alpha as mask if present)
        if foreground.mode == 'RGBA':
            background_img.paste(foreground, (0, 0), foreground)
        else:
            background_img.paste(foreground, (0, 0))
        background_img.save(output_path)
    else:
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(output_path),
            output_width=size,
            output_height=size
        )
    print(f"Generated {output_path.name} ({size}x{size})")


def generate_ico(svg_path, output_path, sizes):
    """Generate a multi-size ICO directly from SVG at the specified sizes."""
    from io import BytesIO
    images = []
    
    for size in sizes:
        # Render SVG to PNG bytes at this size
        png_bytes = cairosvg.svg2png(
            url=str(svg_path),
            output_width=size,
            output_height=size
        )
        # Open as PIL Image and convert to RGBA
        img = Image.open(BytesIO(png_bytes))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        images.append(img)
    
    # Write ICO file manually since Pillow's append_images doesn't always work correctly for ICO
    with open(output_path, 'wb') as f:
        # ICO header
        f.write(b'\x00\x00')  # Reserved
        f.write(b'\x01\x00')  # Type: 1 for ICO
        f.write(struct.pack('<H', len(images)))  # Number of images
        
        # Calculate offsets for image data
        offset = 6 + (16 * len(images))  # Header + directory entries
        image_data = []
        
        # Write directory entries
        for img in images:
            # Save image as PNG to bytes
            png_buffer = BytesIO()
            img.save(png_buffer, format='PNG')
            png_data = png_buffer.getvalue()
            image_data.append(png_data)
            
            # Directory entry
            width = img.width if img.width < 256 else 0
            height = img.height if img.height < 256 else 0
            f.write(struct.pack('B', width))  # Width
            f.write(struct.pack('B', height))  # Height
            f.write(b'\x00')  # Color palette (0 for PNG)
            f.write(b'\x00')  # Reserved
            f.write(b'\x01\x00')  # Color planes
            f.write(b'\x20\x00')  # Bits per pixel (32 for RGBA)
            f.write(struct.pack('<I', len(png_data)))  # Size of image data
            f.write(struct.pack('<I', offset))  # Offset to image data
            offset += len(png_data)
        
        # Write image data
        for png_data in image_data:
            f.write(png_data)
    
    print(f"Generated {output_path.name} (multi-size ICO with {', '.join(f'{size}x{size}' for size in sizes)})")


def main():
    if not SOURCE_SVG.exists():
        print(f"Error: Source SVG not found at {SOURCE_SVG}")
        sys.exit(1)

    print(f"Generating favicons from {SOURCE_SVG.name}...")

    # Generate PNGs
    temp_pngs = {}
    # Cream color from SITE.md: --cream:#fdf8ec
    CREAM = '#fdf8ec'
    
    for size in PNG_SIZES:
        if size == 180:
            # Apple touch icon with cream background
            output_path = OUTPUT_DIR / 'apple-touch-icon.png'
            generate_png(SOURCE_SVG, output_path, size, background=CREAM)
        else:
            output_path = OUTPUT_DIR / f'favicon-{size}.png'
            generate_png(SOURCE_SVG, output_path, size)
        
        temp_pngs[size] = output_path

    # Generate multi-size ICO from the ICO_SIZES directly from SVG
    ico_path = OUTPUT_DIR / 'favicon.ico'
    generate_ico(SOURCE_SVG, ico_path, ICO_SIZES)

    print("\nAll favicons generated successfully!")
    print("\nGenerated files:")
    print(f"  - favicon.ico (16, 32, 48)")
    print(f"  - favicon-48.png, favicon-96.png, favicon-192.png")
    print(f"  - apple-touch-icon.png (180x180)")


if __name__ == '__main__':
    main()
