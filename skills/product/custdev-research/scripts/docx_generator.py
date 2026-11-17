#!/usr/bin/env python3
"""
docx_generator.py — Corporate DOCX Document Generator for CustDev Interviews.
Generates structured Word documents with respondent profile, numbered summary bullets,
speaker badges, timestamps, and full dialogue transcripts.
"""

import os
import sys
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def format_time(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def group_timeline(timeline):
    blocks = []
    curr_speaker = None
    curr_start = 0.0
    curr_end = 0.0
    curr_texts = []

    for item in timeline:
        speaker = item.get("speaker", "Участник")
        start = item.get("start", 0.0)
        end = item.get("end", 0.0)
        text = item.get("text", "").strip()

        if not text:
            continue

        if speaker != curr_speaker:
            if curr_speaker is not None and curr_texts:
                blocks.append({
                    "speaker": curr_speaker,
                    "start": curr_start,
                    "end": curr_end,
                    "text": " ".join(curr_texts)
                })
            curr_speaker = speaker
            curr_start = start
            curr_end = end
            curr_texts = [text]
        else:
            curr_end = end
            curr_texts.append(text)

    if curr_speaker is not None and curr_texts:
        blocks.append({
            "speaker": curr_speaker,
            "start": curr_start,
            "end": curr_end,
            "text": " ".join(curr_texts)
        })

    return blocks

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def generate_custdev_docx(
    transcripts_data_list,
    summary_bullets,
    output_docx_path,
    title="JGGL: Кастдев-интервью и UX-тестирование",
    date_str="01.09.2026",
    interviewer="Влад JGGL",
    interviewer_role="Product Manager / Интервьюер (JGGL) — ведение кастдева, навигация по сценариям, проверка продуктовых гипотез",
    respondent="Алиса",
    respondent_profile="Алиса, 25 лет, маркетолог. Опыт в AI: ежедневно генерирует картинки и видео в Midjourney, Kling, Nano Banana; ранее музыку не создавала. В JGGL новый пользователь (только зарегистрировалась из интереса, заполнила профиль и фото).",
    extra_participants=None
):
    """
    Generates professional DOCX document with detailed client profile and numbered summary list.
    `extra_participants` — optional list of (label, profile) tuples for group sessions
    (each becomes an additional row under the respondent row).
    """
    extra_participants = list(extra_participants or [])
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x17, 0x2B, 0x4D)

    # Document Header Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run(title)
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x52, 0xCC)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    run_sub = sub_p.add_run(f"Полная расшифровка встречи и реестр продуктовых наблюдений • {date_str}")
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x5E, 0x6C, 0x84)

    # Participants Table with Detailed Client Profile
    tbl = doc.add_table(rows=3 + len(extra_participants), cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    col_widths = [Inches(2.0), Inches(4.8)]
    for row in tbl.rows:
        for i, cell in enumerate(row.cells):
            cell.width = col_widths[i]

    set_cell_background(tbl.cell(0, 0), "DEEBFF")
    set_cell_background(tbl.cell(0, 1), "DEEBFF")

    p0 = tbl.cell(0, 0).paragraphs[0]
    r0 = p0.add_run("Участник")
    r0.bold = True
    r0.font.color.rgb = RGBColor(0x07, 0x47, 0xA6)

    p1 = tbl.cell(0, 1).paragraphs[0]
    r1 = p1.add_run("Профиль и роль в исследовании")
    r1.bold = True
    r1.font.color.rgb = RGBColor(0x07, 0x47, 0xA6)

    # Interviewer row
    tbl.cell(1, 0).paragraphs[0].add_run(interviewer).bold = True
    tbl.cell(1, 1).paragraphs[0].add_run(interviewer_role)

    # Respondent row with full profile
    tbl.cell(2, 0).paragraphs[0].add_run(respondent).bold = True
    tbl.cell(2, 1).paragraphs[0].add_run(respondent_profile)

    # Additional participants (group sessions)
    for row_idx, (label, profile) in enumerate(extra_participants, 3):
        tbl.cell(row_idx, 0).paragraphs[0].add_run(label).bold = True
        tbl.cell(row_idx, 1).paragraphs[0].add_run(profile)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Numbered Summary List
    h1 = doc.add_heading(level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(8)
    r_h1 = h1.add_run("1. Ключевые итоги и продуктовые инсайты (Executive Summary)")
    r_h1.font.size = Pt(15)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(0x00, 0x52, 0xCC)

    # Render summary bullets as a clean numbered list
    for idx, bullet in enumerate(summary_bullets, 1):
        clean_bullet = bullet.strip()
        if not clean_bullet:
            continue
        # Strip existing leading numbering if present
        if clean_bullet[0].isdigit() and (clean_bullet[1:3] in [". ", ") ", ": "]):
            clean_bullet = clean_bullet[3:].strip()
        elif clean_bullet[:3].isdigit() and clean_bullet[3:5] in [". ", ") "]:
            clean_bullet = clean_bullet[5:].strip()

        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.2)

        r_num = p.add_run(f"{idx}. ")
        r_num.bold = True
        r_num.font.color.rgb = RGBColor(0x07, 0x47, 0xA6)

        r_text = p.add_run(clean_bullet)
        r_text.font.size = Pt(11)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Section 2+: Full Transcripts
    for part_idx, t_data in enumerate(transcripts_data_list, 1):
        timeline = t_data.get("timeline", [])
        blocks = group_timeline(timeline)

        part_num = part_idx + 1
        custom_label = t_data.get("part_label")
        if custom_label:
            part_title = f"{part_num}. Стенограмма: {custom_label}"
        elif len(transcripts_data_list) > 1:
            part_title = f"{part_num}. Стенограмма Части {part_idx}"
        else:
            part_title = f"{part_num}. Полная стенограмма встречи"
        h1_part = doc.add_heading(level=1)
        h1_part.paragraph_format.space_before = Pt(16)
        h1_part.paragraph_format.space_after = Pt(8)
        r_h1_part = h1_part.add_run(part_title)
        r_h1_part.font.size = Pt(15)
        r_h1_part.font.bold = True
        r_h1_part.font.color.rgb = RGBColor(0x00, 0x52, 0xCC)

        for block in blocks:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15

            spk = block["speaker"]
            time_str = f"[{format_time(block['start'])} - {format_time(block['end'])}]"

            r_time = p.add_run(f"{time_str} ")
            r_time.font.size = Pt(9.5)
            r_time.font.color.rgb = RGBColor(0x89, 0x93, 0xA4)

            r_spk = p.add_run(f"{spk}: ")
            r_spk.bold = True
            if spk == interviewer:
                r_spk.font.color.rgb = RGBColor(0x00, 0x52, 0xCC)
            else:
                r_spk.font.color.rgb = RGBColor(0x00, 0x87, 0x5A)

            r_txt = p.add_run(block["text"])
            r_txt.font.size = Pt(10.5)

        doc.add_paragraph().paragraph_format.space_after = Pt(14)

    output_path = Path(output_docx_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"✅ Generated DOCX report with client profile and numbered summary: {output_path}")

if __name__ == "__main__":
    pass
