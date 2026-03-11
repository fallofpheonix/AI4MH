#!/usr/bin/env python3
"""Render a markdown-ish submission file to a compact PDF (reportlab)."""

from __future__ import annotations

from pathlib import Path
import argparse
import html

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted


def build_story(md_text: str):
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        spaceAfter=4,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        spaceAfter=6,
        spaceBefore=6,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        spaceAfter=4,
        spaceBefore=6,
    )
    code = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.5,
        leading=10.5,
        spaceAfter=5,
        leftIndent=10,
    )

    story = []
    in_code = False
    code_lines: list[str] = []

    for raw in md_text.splitlines():
        line = raw.rstrip()

        if line.strip().startswith("```"):
            in_code = not in_code
            if not in_code and code_lines:
                story.append(Preformatted("\n".join(code_lines), code))
                code_lines = []
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            story.append(Spacer(1, 3))
            continue

        if line.startswith("# "):
            story.append(Paragraph(html.escape(line[2:].strip()), h1))
            continue

        if line.startswith("## "):
            story.append(Paragraph(html.escape(line[3:].strip()), h2))
            continue

        if line.startswith("### "):
            story.append(Paragraph(f"<b>{html.escape(line[4:].strip())}</b>", body))
            continue

        if line.startswith("- "):
            text = html.escape(line[2:].strip())
            story.append(Paragraph(f"&bull; {text}", body))
            continue

        # collapse inline code marker for rendering simplicity
        text = html.escape(line).replace("`", "")
        story.append(Paragraph(text, body))

    return story


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()

    src = args.input.read_text(encoding="utf-8")
    story = build_story(src)

    doc = SimpleDocTemplate(
        str(args.output),
        pagesize=LETTER,
        leftMargin=45,
        rightMargin=45,
        topMargin=40,
        bottomMargin=40,
        title="AI4MH GSoC Submission",
        author="AI4MH Contributor",
    )
    doc.build(story)


if __name__ == "__main__":
    main()
