#!/usr/bin/env python3
"""Render a PDF into page PNGs with macOS Quick Look and build a contact sheet."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter


def split_pdf(pdf_path: Path, pages_dir: Path) -> list[Path]:
    pages_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf_path))
    page_paths: list[Path] = []
    for idx, page in enumerate(reader.pages, start=1):
        out = pages_dir / f"page-{idx:02d}.pdf"
        writer = PdfWriter()
        writer.add_page(page)
        with out.open("wb") as handle:
            writer.write(handle)
        page_paths.append(out)
    return page_paths


def render_pages(page_paths: list[Path], pages_dir: Path, size: int) -> list[Path]:
    png_paths: list[Path] = []
    for page_path in page_paths:
        subprocess.run(
            ["qlmanage", "-t", "-s", str(size), "-o", str(pages_dir), str(page_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        png_path = page_path.with_suffix(page_path.suffix + ".png")
        if not png_path.exists():
            raise FileNotFoundError(f"Quick Look did not create {png_path}")
        png_paths.append(png_path)
    return png_paths


def build_contact_sheet(png_paths: list[Path], out_path: Path, columns: int) -> None:
    thumbs = []
    for path in png_paths:
        img = Image.open(path).convert("RGB")
        img.thumbnail((260, 360))
        thumbs.append((path, img.copy()))

    cell_w, cell_h = 300, 410
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for idx, (path, img) in enumerate(thumbs):
        row, col = divmod(idx, columns)
        x = col * cell_w + (cell_w - img.width) // 2
        y = row * cell_h + 28
        sheet.paste(img, (x, y))
        draw.text((col * cell_w + 12, row * cell_h + 8), path.stem.replace(".pdf", ""), fill=(40, 40, 40))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages-dir", type=Path, required=True)
    parser.add_argument("--contact-sheet", type=Path, required=True)
    parser.add_argument("--size", type=int, default=1200)
    parser.add_argument("--columns", type=int, default=4)
    args = parser.parse_args()

    page_paths = split_pdf(args.pdf, args.pages_dir)
    png_paths = render_pages(page_paths, args.pages_dir, args.size)
    build_contact_sheet(png_paths, args.contact_sheet, args.columns)
    print(f"Rendered {len(png_paths)} pages")
    print(f"Contact sheet: {args.contact_sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
