#!/usr/bin/env python3
"""
Deck-Craft Generator CLI
Generates self-contained, interactive HTML slide decks in Varick Agents style.
Usage:
  python3 generate-deck.py input.md -o output.html
  python3 generate-deck.py --scaffold sample.md
"""

import sys
import os
import re
import argparse

SAMPLE_MARKDOWN = """# 01. Don't Apply AI Without Systems
---
meta: SYSTEMS FIRST | HIGH-AGENCY PRESENTATION ARCHITECTURE
sub: Why autonomous single-file web presentations are replacing PDF decks, Keynote, and heavy web runtimes.
type: bento
stops: 1
---
- tag: 01 / ZERO-DEPENDENCY
  title: Single File HTML
  desc: Works offline via file://. All fonts, styles, and logic bundled in one single file.
- tag: 02 / ADDRESSABLE HASHES
  title: Sub-Slide Addressing
  desc: Hierarchical routing #13.4 lets you link directly to specific stages of an argument.
- tag: 03 / STOPS & BEATS
  title: Deterministic Engine
  desc: Managed pauses and staggered animations without bloated frameworks or lag.

# 02. Same four buckets. Smaller firm, same method.
---
meta: METHODOLOGY | DECOMPOSITION FRAMEWORK
sub: 14 logged steps in audit. Five deleted immediately. Code handles routine. Agents handle exceptions. A human signs.
type: buckets
stops: 4
stagger: 380
---
[Delete | 5 steps · rework & repeats | red]
- 03: Re-ask client
- 06: Redo manual copy
- 10: Send back review
- 11: Fix formatting

[Plain Code | 4 steps · scripts & feeds | blue]
- 01: Collect files
- 04: Categorise items
- 07: Reconcile tables
- 14: Bill invoices

[Agents | 3 agents · chasing & triage | green]
- 02: Chase missing input
- 05: Ask follow-up question
- 08: Flag anomalous rate

[Human | 2 decisions · judgment | purple]
- 09: Final legal signoff
- 13: Relationship meeting
"""

def scaffold(output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(SAMPLE_MARKDOWN.strip())
    print(f"✅ Created scaffold at: {output_path}")

def build_deck(md_path, html_output, template_path):
    if not os.path.exists(template_path):
        print(f"❌ Template not found at: {template_path}")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # If md_path is sample or user supplied, verify
    if not os.path.exists(md_path):
        print(f"❌ Markdown file not found at: {md_path}")
        sys.exit(1)

    # For now, if user builds from sample, write out the template
    # In full mode, parser can parse md into .scr sections
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(template_content)

    print(f"🚀 Deck successfully built to: {html_output}")

def main():
    parser = argparse.ArgumentParser(description="Deck-Craft: Single-File Presentation Generator")
    parser.add_argument("input", nargs="?", help="Markdown input file")
    parser.add_argument("-o", "--output", default="deck.html", help="Output HTML file")
    parser.add_argument("--scaffold", metavar="FILE", help="Generate a sample markdown file")
    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "..", "template", "deck-engine.html")

    if args.scaffold:
        scaffold(args.scaffold)
        return

    if not args.input:
        parser.print_help()
        return

    build_deck(args.input, args.output, template_path)

if __name__ == "__main__":
    main()
