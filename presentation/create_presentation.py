"""Create the CogniStream project presentation from verified EDA outputs."""

from pathlib import Path

import pandas as pd
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
EDA = ROOT / "outputs" / "eda"
OUT = ROOT / "presentation" / "CogniStream_Project_Presentation.pptx"

NAVY = RGBColor(31, 48, 73)
TEAL = RGBColor(27, 158, 119)
ORANGE = RGBColor(217, 95, 2)
GRAY = RGBColor(90, 90, 90)


def add_title(slide, title, subtitle=None):
    title_box = slide.shapes.add_textbox(Inches(0.55), Inches(0.25), Inches(12.2), Inches(0.65))
    p = title_box.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY
    if subtitle:
        box = slide.shapes.add_textbox(Inches(0.58), Inches(0.9), Inches(12), Inches(0.35))
        p = box.text_frame.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(12)
        p.font.color.rgb = GRAY


def add_bullets(slide, bullets, left=0.8, top=1.35, width=11.5, height=5.5, size=20):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.clear()
    for index, item in enumerate(bullets):
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = RGBColor(45, 45, 45)
        p.space_after = Pt(12)
    return box


def add_image_slide(prs, title, image_name, caption):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title)
    slide.shapes.add_picture(str(EDA / image_name), Inches(0.65), Inches(1.2), width=Inches(8.3))
    add_bullets(slide, [caption], left=9.15, top=1.55, width=3.35, height=4.5, size=17)
    return slide


def main():
    success = pd.read_csv(EDA / "success_group_summary.csv")
    cognitive = pd.read_csv(EDA / "cognitive_load_summary.csv")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.75), Inches(1.55), Inches(12), Inches(1.2))
    p = title.text_frame.paragraphs[0]
    p.text = "CogniStream"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    subtitle = slide.shapes.add_textbox(Inches(1), Inches(3.0), Inches(11.3), Inches(1.2))
    p = subtitle.text_frame.paragraphs[0]
    p.text = "Developer Flow-State & Cognitive Load Analytics"
    p.font.size = Pt(26)
    p.font.color.rgb = TEAL
    p.alignment = PP_ALIGN.CENTER
    add_bullets(slide, ["Data Analytics Internship Project", "Prepared by Prince Kumar"], left=2.2, top=4.55, width=8.9, height=1.2, size=18)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "1. Project objective")
    add_bullets(slide, [
        "Understand how developer work habits relate to task success.",
        "Study cognitive load as a possible early-warning signal.",
        "Clean, analyze and visualize the dataset.",
        "Deliver an interactive dashboard for decision-oriented insights.",
    ])

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "2. Dataset overview")
    add_bullets(slide, [
        "500 developer-task records and 9 numeric fields.",
        "Measures include coding hours, sleep, distractions, commits, bugs, AI usage and cognitive load.",
        "Target: task_success — 0 means unsuccessful, 1 means successful.",
        "No date, developer ID or team ID is available; analysis is cross-sectional.",
    ])

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "3. Data preparation")
    add_bullets(slide, [
        "Preserved the raw CSV and created a processed analysis copy.",
        "Validated expected columns and converted fields to numeric types.",
        "Checked duplicates, missing values and domain ranges.",
        "Result: 500 valid rows retained; 0 duplicates, 0 missing cells and 0 invalid rows.",
    ])

    add_image_slide(prs, "4. Task-success distribution", "01_task_success_balance.png", "303 records are successful and 197 are unsuccessful. The observed task-success rate is 60.6%.")
    add_image_slide(prs, "5. Feature distributions", "02_feature_distributions.png", "The plots show the operating ranges of coding hours, sleep, distractions and cognitive load, split by outcome.")
    add_image_slide(prs, "6. Productivity comparison", "03_features_by_task_outcome.png", "Successful records show higher average coding hours and commits, while unsuccessful records show more bugs and slightly higher cognitive load.")
    add_image_slide(prs, "7. Cognitive-load analysis", "05_success_by_cognitive_load.png", "The high-load group has the lowest observed success rate: 36.8%, compared with 64.1% for low load and 68.2% for medium load.")
    add_image_slide(prs, "8. Correlation overview", "06_correlation_heatmap.png", "Correlation helps prioritize questions for deeper analysis; it does not prove causation.")

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "9. Key findings")
    add_bullets(slide, [
        "Successful records: 5.98 average coding hours, 5.35 commits and 0.70 bugs.",
        "Unsuccessful records: 3.53 average coding hours, 3.47 commits and 1.10 bugs.",
        "High cognitive load: 36.8% success rate and 1.25 average bugs.",
        "Medium cognitive load: 68.2% success rate and 0.86 average bugs.",
    ])

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "10. Dashboard design")
    add_bullets(slide, [
        "KPI cards: records, task-success rate, average cognitive load, coding hours and bugs.",
        "Filters: task outcome and cognitive-load group.",
        "Charts: outcome balance, success rate by load, coding hours vs load and selectable feature comparisons.",
        "The dashboard is implemented in dashboard/app.py using Streamlit.",
    ])

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "11. Recommendations")
    add_bullets(slide, [
        "Use cognitive load, bugs and distractions as monitoring indicators.",
        "Investigate high-load records early rather than relying only on final task outcomes.",
        "Use coding hours and commits as productivity context, not as standalone performance targets.",
        "Collect dates and anonymized developer/team IDs in the next dataset version.",
    ])

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "12. Limitations and conclusion")
    add_bullets(slide, [
        "This is observational data; relationships should not be described as causal.",
        "The data has no longitudinal or team-level identifiers.",
        "The dashboard provides a practical monitoring prototype.",
        "Next step: validate patterns with larger, dated and anonymized observations.",
    ])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
