#!/usr/bin/env python3
"""Create a fictional, explicitly illustrative client discussion deck."""

from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


C = {
    "navy": "0B1F5B",
    "title": "16294A",
    "ink": "1E293B",
    "slate": "64748B",
    "paper": "FFFFFF",
    "white": "FFFFFF",
    "mist": "F8FAFC",
    "border": "D7DEE9",
    "sage": "0E8C8C",
    "steel": "034EA2",
    "copper": "F97316",
    "green": "50B848",
    "sage_light": "33B2C1",
    "plum": "6366F1",
    "soft_sage": "EEF7F7",
    "soft_steel": "EEF2F7",
    "soft_copper": "FFF7ED",
    "soft_green": "EAF7EF",
    "soft_plum": "F5F3FF",
}


def rgb(value: str) -> RGBColor:
    return RGBColor.from_string(value)


def set_background(slide, color: str) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(C[color])


def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    *,
    size=18,
    color="ink",
    bold=False,
    font="Aptos",
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin=0,
):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(margin)
    frame.margin_top = frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    paragraph.space_after = Pt(0)
    run = paragraph.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb(C[color])
    return box


def add_box(
    slide,
    x,
    y,
    w,
    h,
    *,
    fill="white",
    line="border",
    radius=True,
    corner_ratio=0.04,
    line_width=1,
):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(
        shape_type, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    if radius:
        shape.adjustments[0] = corner_ratio
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(C[fill])
    shape.line.color.rgb = rgb(C[line])
    shape.line.width = Pt(line_width)
    return shape


def add_rule(slide, y=0.0, color="navy", h=0.055):
    add_box(slide, 0, y, 13.333, h, fill=color, line=color, radius=False)


def add_title(slide, title, subtitle=None, section=None):
    add_rule(slide)
    if section:
        add_text(
            slide,
            section.upper(),
            0.66,
            0.27,
            4.6,
            0.23,
            size=10,
            color="steel",
            bold=True,
        )
    wrapped_title = "\n" in title
    title_size = 25 if wrapped_title or len(title) > 70 else 28
    add_text(
        slide,
        title,
        0.66,
        0.50,
        12.0,
        0.90 if wrapped_title else 0.80,
        size=title_size,
        color="title",
        bold=True,
    )
    if subtitle:
        add_text(
            slide,
            subtitle,
            0.66,
            1.43 if wrapped_title else 1.38,
            11.8,
            0.30,
            size=14,
            color="slate",
        )


def add_footer(slide, number):
    add_text(
        slide,
        "ILLUSTRATIVE CLIENT DISCUSSION",
        0.66,
        7.12,
        4.0,
        0.18,
        size=9,
        color="slate",
        bold=True,
    )
    add_text(
        slide,
        str(number),
        12.25,
        7.10,
        0.4,
        0.2,
        size=9,
        color="slate",
        align=PP_ALIGN.RIGHT,
    )


def make_deck(output: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.title = "Illustrative AI Support Pilot"
    prs.core_properties.subject = "Smoke test for craft-client-pptx"
    prs.core_properties.author = "Craft Client PPTX"
    blank = prs.slide_layouts[6]

    # 1 — Quiet cover
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_box(slide, 0, 0, 0.12, 7.5, fill="steel", line="steel", radius=False)
    add_box(slide, 9.20, 1.15, 0.025, 4.65, fill="border", line="border", radius=False)
    add_text(
        slide,
        "ILLUSTRATIVE CLIENT DISCUSSION",
        0.74,
        0.72,
        4.5,
        0.28,
        size=11,
        color="steel",
        bold=True,
    )
    add_text(
        slide,
        "A practical AI support pilot\nfor service operations",
        0.74,
        1.45,
        7.9,
        1.75,
        size=34,
        color="title",
        bold=True,
    )
    add_text(
        slide,
        "A bounded eight-week proposal to validate workflow fit, controls and adoption.",
        0.74,
        3.52,
        7.6,
        0.72,
        size=18,
        color="slate",
    )
    add_text(
        slide,
        "Prepared for discussion  |  Fictional scenario",
        0.74,
        6.54,
        5.8,
        0.32,
        size=12,
        color="slate",
    )
    add_text(
        slide,
        "01",
        9.58,
        1.36,
        2.6,
        1.1,
        size=58,
        color="steel",
        bold=False,
        align=PP_ALIGN.LEFT,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "EXECUTIVE\nMINIMAL",
        9.60,
        2.72,
        2.7,
        0.76,
        size=14,
        color="navy",
        bold=True,
        align=PP_ALIGN.LEFT,
    )
    add_box(slide, 9.58, 4.34, 2.68, 0.54, fill="soft_sage", line="soft_sage")
    add_text(
        slide,
        "CALM · PRECISE · HUMAN",
        9.80,
        4.50,
        2.30,
        0.20,
        size=10,
        color="sage",
        bold=True,
    )

    # 2 — Executive answer
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_title(
        slide,
        "A focused pilot can test value without changing the core workflow",
        "The decision is whether to validate one use case under explicit human control.",
        "Executive answer",
    )
    add_box(slide, 0.66, 1.78, 4.05, 4.77, fill="navy", line="navy")
    add_text(
        slide,
        "Decision today",
        1.00,
        2.15,
        3.25,
        0.35,
        size=15,
        color="sage_light",
        bold=True,
    )
    add_text(
        slide,
        "Approve discovery for one bounded support workflow.",
        1.00,
        2.80,
        3.05,
        1.45,
        size=28,
        color="paper",
        bold=True,
    )
    add_text(
        slide,
        "No production automation is proposed at this stage.",
        1.00,
        5.45,
        3.0,
        0.62,
        size=15,
        color="paper",
    )
    rows = [
        ("01", "Scope", "One workflow, one team, named owner"),
        ("02", "Control", "Human approval remains mandatory"),
        ("03", "Evidence", "Continue only if agreed exit criteria are met"),
    ]
    for i, (number, label, body) in enumerate(rows):
        y = 1.90 + i * 1.46
        add_box(slide, 5.08, y, 7.55, 1.12, fill="white", line="border")
        add_text(
            slide,
            number,
            5.36,
            y + 0.28,
            0.62,
            0.35,
            size=18,
            color="sage",
            bold=True,
        )
        add_text(
            slide,
            label,
            6.12,
            y + 0.20,
            1.42,
            0.32,
            size=14,
            color="slate",
            bold=True,
        )
        add_text(
            slide,
            body,
            7.55,
            y + 0.18,
            4.45,
            0.60,
            size=17,
            color="ink",
            bold=True,
        )
    add_footer(slide, 2)

    # 3 — Process
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_title(
        slide,
        "Three handoffs create avoidable waiting time in the support cycle",
        "The pilot focuses on the preparation step, not on final decision authority.",
        "Observed workflow",
    )
    steps = [
        ("1", "Receive", "Request and context"),
        ("2", "Prepare", "Collect evidence"),
        ("3", "Review", "Expert judgment"),
        ("4", "Respond", "Communicate action"),
    ]
    for i, (number, label, note) in enumerate(steps):
        x = 0.70 + i * 3.10
        selected = i == 1
        fill = "soft_copper" if selected else "mist"
        line = "copper" if selected else "border"
        add_box(slide, x, 2.08, 2.55, 2.18, fill=fill, line=line)
        add_text(
            slide,
            number,
            x + 0.22,
            2.30,
            0.50,
            0.45,
            size=22,
            color="copper" if selected else "sage",
            bold=True,
        )
        add_text(
            slide,
            label,
            x + 0.22,
            2.94,
            1.95,
            0.40,
            size=20,
            color="navy",
            bold=True,
        )
        add_text(
            slide,
            note,
            x + 0.22,
            3.48,
            1.95,
            0.36,
            size=14,
            color="slate",
        )
        if i < 3:
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.CHEVRON,
                Inches(x + 2.66),
                Inches(2.84),
                Inches(0.34),
                Inches(0.56),
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = rgb(C["border"])
            arrow.line.color.rgb = rgb(C["border"])
    add_box(slide, 3.80, 4.78, 5.75, 1.22, fill="soft_copper", line="copper")
    add_text(
        slide,
        "Pilot focus",
        4.12,
        5.05,
        1.15,
        0.28,
        size=13,
        color="copper",
        bold=True,
    )
    add_text(
        slide,
        "Reduce preparation effort while preserving expert review.",
        5.35,
        4.98,
        3.75,
        0.48,
        size=18,
        color="ink",
        bold=True,
    )
    add_footer(slide, 3)

    # 4 — Layered architecture
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_title(
        slide,
        "Human approval remains the control point across the proposed\npilot",
        "A simple layered view keeps the technical solution connected to operational safeguards.",
        "Technology narrative",
    )
    add_box(slide, 0.68, 1.85, 3.25, 4.65, fill="navy", line="navy")
    add_text(
        slide,
        "Design principle",
        1.02,
        2.18,
        2.35,
        0.32,
        size=14,
        color="sage_light",
        bold=True,
    )
    add_text(
        slide,
        "Assist preparation.\nKeep decisions human.",
        1.02,
        2.78,
        2.42,
        1.50,
        size=23,
        color="paper",
        bold=True,
    )
    add_text(
        slide,
        "Each transition has an owner, an audit trail and a fallback.",
        1.02,
        5.35,
        2.36,
        0.70,
        size=15,
        color="paper",
    )
    layers = [
        ("1", "User workflow", "Existing request and review channel", "soft_sage", "sage"),
        ("2", "AI assistance", "Draft, retrieve and summarize", "soft_steel", "steel"),
        ("3", "Controls", "Approval, access and traceability", "soft_copper", "copper"),
        ("4", "Knowledge", "Approved sources only", "white", "plum"),
    ]
    for i, (number, label, body, fill, accent) in enumerate(layers):
        y = 1.87 + i * 1.15
        add_box(slide, 4.36, y, 8.25, 0.92, fill=fill, line=accent)
        add_text(
            slide,
            number,
            4.64,
            y + 0.21,
            0.40,
            0.26,
            size=14,
            color=accent,
            bold=True,
        )
        add_text(
            slide,
            label,
            5.20,
            y + 0.17,
            2.10,
            0.30,
            size=16,
            color="navy",
            bold=True,
        )
        add_text(
            slide,
            body,
            7.50,
            y + 0.17,
            4.50,
            0.32,
            size=15,
            color="ink",
        )
    add_footer(slide, 4)

    # 5 — Roadmap
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_title(
        slide,
        "Eight weeks are enough to validate fit, controls and adoption",
        "All timing is illustrative and subject to access, owner availability and scope confirmation.",
        "Proposed plan",
    )
    phases = [
        ("Weeks 1–2", "Discover", "Confirm workflow\nand evidence"),
        ("Weeks 3–4", "Configure", "Prepare bounded\nprototype"),
        ("Weeks 5–6", "Exercise", "Run supervised\nscenarios"),
        ("Weeks 7–8", "Decide", "Review criteria\nand next step"),
    ]
    accents = ["copper", "green", "steel", "plum"]
    for i, (period, phase, body) in enumerate(phases):
        x = 0.70 + i * 3.08
        add_text(
            slide,
            period,
            x,
            1.82,
            2.40,
            0.28,
            size=12,
            color=accents[i],
            bold=True,
        )
        add_box(slide, x, 2.18, 2.62, 2.00, fill="mist", line=accents[i])
        add_text(
            slide,
            phase,
            x + 0.24,
            2.48,
            2.04,
            0.40,
            size=20,
            color="navy",
            bold=True,
        )
        add_text(
            slide,
            body,
            x + 0.24,
            3.16,
            2.00,
            0.60,
            size=15,
            color="slate",
        )
    add_text(
        slide,
        "Exit criteria",
        0.72,
        4.72,
        1.25,
        0.30,
        size=14,
        color="navy",
        bold=True,
    )
    gates = [
        ("Workflow fit", "Useful in agreed scenarios"),
        ("Control fit", "Owners accept safeguards"),
        ("Adoption fit", "Team can use the process"),
    ]
    for i, (label, body) in enumerate(gates):
        x = 2.15 + i * 3.46
        add_box(slide, x, 4.55, 3.04, 1.18, fill="white", line="border")
        add_text(
            slide,
            label,
            x + 0.22,
            4.78,
            2.36,
            0.28,
            size=14,
            color="sage",
            bold=True,
        )
        add_text(
            slide,
            body,
            x + 0.22,
            5.20,
            2.50,
            0.30,
            size=14,
            color="ink",
        )
    add_footer(slide, 5)

    # 6 — Risk and assumption register
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_title(
        slide,
        "Proceed only if access, ownership and review capacity are\nconfirmed",
        "Open conditions are presented explicitly to support a balanced customer decision.",
        "Assumptions and risks",
    )
    columns = [
        ("Type", 0.72, 1.42),
        ("Condition", 2.14, 4.62),
        ("Owner", 6.76, 2.02),
        ("Treatment / validation", 8.78, 3.80),
    ]
    for label, x, w in columns:
        add_text(
            slide,
            label,
            x,
            1.86,
            w,
            0.30,
            size=13,
            color="slate",
            bold=True,
        )
    rows = [
        ("Assumption", "Approved knowledge sources can be identified", "Client", "Confirm during discovery"),
        ("Dependency", "A workflow owner is available for weekly review", "Joint", "Nominate before kickoff"),
        ("Risk", "Sensitive data may limit representative testing", "Client", "Use sanitized scenarios first"),
        ("Risk", "Users may treat drafts as final answers", "Joint", "Keep approval and audit controls"),
    ]
    fills = ["soft_sage", "white", "soft_copper", "white"]
    type_colors = ["sage", "steel", "copper", "copper"]
    for i, row in enumerate(rows):
        y = 2.22 + i * 0.97
        add_box(slide, 0.66, y, 12.00, 0.77, fill=fills[i], line="border")
        add_text(
            slide,
            row[0],
            0.88,
            y + 0.20,
            1.14,
            0.27,
            size=13,
            color=type_colors[i],
            bold=True,
        )
        add_text(
            slide,
            row[1],
            2.14,
            y + 0.16,
            4.35,
            0.36,
            size=14,
            color="ink",
        )
        add_text(
            slide,
            row[2],
            6.77,
            y + 0.18,
            1.72,
            0.28,
            size=14,
            color="ink",
            bold=True,
        )
        add_text(
            slide,
            row[3],
            8.80,
            y + 0.16,
            3.36,
            0.36,
            size=14,
            color="ink",
        )
    add_box(slide, 0.66, 6.34, 12.0, 0.43, fill="navy", line="navy")
    add_text(
        slide,
        "Recommendation: confirm these conditions before committing to the pilot schedule.",
        0.96,
        6.43,
        10.95,
        0.24,
        size=14,
        color="paper",
        bold=True,
    )
    add_footer(slide, 6)

    # 7 — Next step
    slide = prs.slides.add_slide(blank)
    set_background(slide, "paper")
    add_title(
        slide,
        "Confirm scope, nominate owners and begin discovery",
        "The immediate ask is limited to preparation for a bounded pilot.",
        "Next step",
    )
    actions = [
        ("01", "Confirm scope", "Select one workflow and define exclusions."),
        ("02", "Nominate owners", "Assign business, technical and control reviewers."),
        ("03", "Open discovery", "Provide approved examples and access constraints."),
    ]
    accents = ["sage", "steel", "plum"]
    for i, (number, label, body) in enumerate(actions):
        x = 0.72 + i * 4.18
        add_box(slide, x, 1.98, 3.72, 2.58, fill="mist", line=accents[i])
        add_text(
            slide,
            number,
            x + 0.28,
            2.22,
            0.70,
            0.42,
            size=22,
            color=accents[i],
            bold=True,
        )
        add_text(
            slide,
            label,
            x + 0.28,
            2.94,
            2.90,
            0.40,
            size=20,
            color="navy",
            bold=True,
        )
        add_text(
            slide,
            body,
            x + 0.28,
            3.54,
            2.86,
            0.66,
            size=15,
            color="slate",
        )
    add_box(slide, 0.72, 5.14, 12.0, 1.20, fill="navy", line="navy")
    add_text(
        slide,
        "Proposed decision",
        1.08,
        5.42,
        1.78,
        0.30,
        size=14,
        color="sage_light",
        bold=True,
    )
    add_text(
        slide,
        "Authorize discovery; return with validated scope, controls and exit criteria.",
        3.04,
        5.34,
        8.72,
        0.50,
        size=20,
        color="paper",
        bold=True,
    )
    add_footer(slide, 7)

    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))


def main() -> int:
    parser = argparse.ArgumentParser()
    default = Path(__file__).resolve().parent.parent / "tests" / "smoke-test.pptx"
    parser.add_argument("--output", type=Path, default=default)
    args = parser.parse_args()
    make_deck(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
