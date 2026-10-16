#!/usr/bin/env python3
"""
Self-check validator for sketch-design HTML presentations and whiteboard diagrams.
Validates custom element semantics, 1600x900 coordinate bounds, tone palette, and security rules.
Usage:
    python3 scripts/self_check.py file.html [file2.html ...]
"""

import sys
import re
from html.parser import HTMLParser
from pathlib import Path

VALID_TONES = {"orange", "green", "purple", "pink", "blue", "teal", "yellow", "red", "gray"}
VALID_SK_TAGS = {
    "sk-deck", "sk-slide", "sk-title", "sk-box", "sk-doc", "sk-bubble",
    "sk-chip", "sk-mark", "sk-meter", "sk-arrow", "sk-note", "sk-caption",
    "sk-spark", "sk-figure", "sk-dice"
}

class SketchValidator(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.errors = []
        self.has_deck = False
        self.slides_count = 0
        self.current_slide = None
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower == "sk-deck":
            self.has_deck = True

        elif tag_lower == "sk-slide":
            self.slides_count += 1
            self.current_slide = self.slides_count
            tone = attr_dict.get("tone")
            if tone and tone not in VALID_TONES:
                self.errors.append(f"Slide #{self.slides_count}: invalid tone='{tone}'. Expected one of {sorted(VALID_TONES)}")

        elif tag_lower.startswith("sk-"):
            if tag_lower not in VALID_SK_TAGS:
                self.errors.append(f"Unknown custom element <{tag_lower}>")

            # Check coordinate bounds on 1600x900 canvas
            x = attr_dict.get("x")
            y = attr_dict.get("y")
            w = attr_dict.get("w")
            h = attr_dict.get("h")

            if x is not None and w is not None:
                try:
                    xf = float(x)
                    wf = float(w)
                    if xf + wf > 1650:
                        self.errors.append(f"<{tag_lower}> bounds x={x} w={w} exceeds 1600px stage width (overflow by {xf+wf-1600:.0f}px)")
                    if xf < -50:
                        self.errors.append(f"<{tag_lower}> bounds x={x} negative stage overflow")
                except ValueError:
                    pass

            if y is not None and h is not None:
                try:
                    yf = float(y)
                    hf = float(h)
                    if yf + hf > 950:
                        self.errors.append(f"<{tag_lower}> bounds y={y} h={h} exceeds 900px stage height (overflow by {yf+hf-900:.0f}px)")
                    if yf < -50:
                        self.errors.append(f"<{tag_lower}> bounds y={y} negative stage overflow")
                except ValueError:
                    pass

            # Check ergonomic safe-bounds for speech bubbles
            if tag_lower == "sk-bubble":
                if w is not None and float(w) < 320:
                    self.errors.append(f"<sk-bubble> width w={w} is too narrow for comfortable speech bubble (recommended w >= 360)")
                if h is not None and float(h) < 130:
                    self.errors.append(f"<sk-bubble> height h={h} is too short (recommended h >= 140)")

            # Check arrow coordinates
            if tag_lower == "sk-arrow":
                for coord in ["x1", "x2"]:
                    val = attr_dict.get(coord)
                    if val:
                        try:
                            vf = float(val)
                            if vf < -50 or vf > 1650:
                                self.errors.append(f"<sk-arrow> {coord}={val} outside 1600px stage bounds")
                        except ValueError:
                            pass
                for coord in ["y1", "y2"]:
                    val = attr_dict.get(coord)
                    if val:
                        try:
                            vf = float(val)
                            if vf < -50 or vf > 950:
                                self.errors.append(f"<sk-arrow> {coord}={val} outside 900px stage bounds")
                        except ValueError:
                            pass

        # Disallow unsafe remote scripts (only bundle.js or inline authorized)
        if tag_lower == "script":
            src = attr_dict.get("src")
            if src and (src.startswith("http://") or src.startswith("https://")):
                self.errors.append(f"Unauthorized external script source: '{src}'. Zero-dependency rule requires local bundle.js.")

        # Disallow inline executable event handlers
        for k in attr_dict:
            if k.lower().startswith("on"):
                self.errors.append(f"Forbidden inline executable attribute '{k}' on <{tag_lower}>")

def validate_file(path_str):
    path = Path(path_str)
    if not path.is_file():
        print(f"FAIL {path}: File not found", file=sys.stderr)
        return False

    content = path.read_text(encoding="utf-8")
    parser = SketchValidator(path.name)
    parser.feed(content)

    if not parser.has_deck and "<svg" not in content:
        parser.errors.append("Document missing <sk-deck> container or standalone <svg>")

    if re.search(r"\.inner-content\s*\{[^}]*padding\s*:", content):
        parser.errors.append("Double-padding detected: .inner-content should NOT define its own padding (parent .sk-box-inner already provides safe padding). Use width: 100%; height: 100%; justify-content: space-evenly instead.")

    if parser.errors:
        print(f"FAIL {path}:")
        for err in parser.errors:
            print(f"  - {err}", file=sys.stderr)
        return False
    else:
        print(f"OK {path}")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 self_check.py <file.html> [file2.html ...]")
        sys.exit(1)

    all_ok = True
    for arg in sys.argv[1:]:
        if not validate_file(arg):
            all_ok = False

    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
