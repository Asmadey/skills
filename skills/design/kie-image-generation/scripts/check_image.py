#!/usr/bin/env python3
"""Приёмка сгенерированных картинок: формат, размер, фон/альфа и контактный лист.

    python3 check_image.py a.webp b.webp --bg 11,13,18
    python3 check_image.py *.webp --bg 11,13,18 --sheet /tmp/sheet.png

Коды выхода: 0 — все кадры прошли, 1 — есть брак, 2 — ошибка аргументов.
"""
from __future__ import annotations

import argparse
import os
import sys

from PIL import Image


def _color(value: str) -> tuple[int, int, int]:
    parts = [int(p) for p in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("цвет в виде R,G,B")
    return tuple(parts)  # type: ignore[return-value]


def on_background(img: Image.Image, bg: tuple[int, int, int]) -> Image.Image:
    """Наложить кадр на цвет страницы — единственный способ оценивать прозрачный кадр."""
    if img.mode != "RGBA":
        return img.convert("RGB")
    canvas = Image.new("RGBA", img.size, (*bg, 255))
    canvas.alpha_composite(img)
    return canvas.convert("RGB")


def border_delta(img: Image.Image, bg: tuple[int, int, int]) -> tuple[float, str]:
    """Максимальное отличие цвета по рамке кадра от целевого фона."""
    rgb = on_background(img, bg)
    w, h = rgb.size
    px = rgb.load()
    worst, where = 0.0, ""
    step_x, step_y = max(1, w // 30), max(1, h // 30)
    for x in range(0, w, step_x):
        for y in (2, h - 3):
            d = max(abs(px[x, y][i] - bg[i]) for i in range(3))
            if d > worst:
                worst, where = d, f"{'верх' if y < h // 2 else 'низ'} x={x}"
    for y in range(0, h, step_y):
        for x in (2, w - 3):
            d = max(abs(px[x, y][i] - bg[i]) for i in range(3))
            if d > worst:
                worst, where = d, f"{'лево' if x < w // 2 else 'право'} y={y}"
    return worst, where


def corner_alpha(img: Image.Image) -> int:
    """Максимальная альфа в углах: >8 значит, что фон нарисован, а не прозрачен."""
    w, h = img.size
    px = img.load()
    return max(px[1, 1][3], px[w - 2, 1][3], px[1, h - 2][3], px[w - 2, h - 2][3])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--bg", type=_color, default=(11, 13, 18), help="цвет страницы, R,G,B")
    ap.add_argument("--tolerance", type=int, default=12, help="допуск отклонения фона")
    ap.add_argument("--expect", help="ожидаемый размер, напр. 1200x800")
    ap.add_argument("--sheet", help="собрать контактный лист в этот файл")
    ap.add_argument("--cols", type=int, default=3)
    args = ap.parse_args()

    fail = 0
    for path in args.files:
        if not os.path.exists(path):
            print(f"FAIL {path}: файла нет")
            fail += 1
            continue
        img = Image.open(path)
        fmt, mode, size = img.format, img.mode, img.size
        notes: list[str] = []
        ok = fmt == "WEBP"
        if not ok:
            notes.append(f"формат {fmt}, нужен WEBP")
        if args.expect:
            want = tuple(int(v) for v in args.expect.lower().split("x"))
            if size != want:
                ok = False
                notes.append(f"размер {size[0]}x{size[1]}, нужен {want[0]}x{want[1]}")
        if "A" in mode:
            alpha = corner_alpha(img)
            if alpha > 8:
                ok = False
                notes.append(f"углы не прозрачны (alpha={alpha})")
            else:
                notes.append(f"фон прозрачный (alpha={alpha})")
        else:
            delta, where = border_delta(img, args.bg)
            if delta > args.tolerance:
                ok = False
                notes.append(f"фон неровный: отклонение {delta:.0f} у края {where}")
            else:
                notes.append(f"фон ровный ({delta:.0f})")
        fail += 0 if ok else 1
        kb = os.path.getsize(path) // 1024
        print(f"{'OK  ' if ok else 'FAIL'} {os.path.basename(path):<44} {fmt} {mode:<5} "
              f"{size[0]}x{size[1]} {kb:>4} КБ | " + "; ".join(notes))

    if args.sheet:
        imgs = [Image.open(p) for p in args.files if os.path.exists(p)]
        if imgs:
            cell_w = 420
            thumbs = []
            for im in imgs:
                im = on_background(im, args.bg)
                im.thumbnail((cell_w - 20, cell_w - 20))
                thumbs.append(im)
            cols = max(1, args.cols)
            rows = (len(thumbs) + cols - 1) // cols
            cell_h = max(t.height for t in thumbs) + 20
            sheet = Image.new("RGB", (cols * cell_w + 20, rows * cell_h + 20), args.bg)
            for i, t in enumerate(thumbs):
                x = 10 + (i % cols) * cell_w + (cell_w - 20 - t.width) // 2
                y = 10 + (i // cols) * cell_h + (cell_h - 20 - t.height) // 2
                sheet.paste(t, (x, y))
            sheet.save(args.sheet)
            print(f"лист: {args.sheet} ({sheet.width}x{sheet.height}, фон {args.bg})")

    print(f"\nнеудач: {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
