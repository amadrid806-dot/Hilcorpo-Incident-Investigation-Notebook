from reportlab.lib.colors import HexColor
from config import DARK, GREEN, WHITE, MID, LIGHT, FAINT, MARGIN, TAB_H, TITLE, VERSION, SUBTITLE
from content import SECTION_TITLES, TABS
from drawing import fit_logo


def draw_cover(c, w, h):
    """Premium, handwriting-first cover for Version 1.2."""
    c.setFillColor(DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # restrained Hilcorp accent
    c.setFillColor(GREEN)
    c.rect(0, h - 12, w, 12, fill=1, stroke=0)
    c.rect(MARGIN, h * 0.675, 72, 4, fill=1, stroke=0)

    # logo block
    fit_logo(c, MARGIN, h - 150, 170, 66)

    # title hierarchy
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(MARGIN, h - 225, "INCIDENT INVESTIGATION")
    c.drawString(MARGIN, h - 257, "FIELD NOTEBOOK")

    c.setFillColor(HexColor("#B8C1C3"))
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN, h - 282, SUBTITLE)
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN, h - 298, "Evidence-based field documentation • Interviews • Timeline • Analysis • Actions")

    # identity panel
    panel_y = h - 515
    panel_h = 158
    c.setFillColor(HexColor("#202C2F"))
    c.roundRect(MARGIN, panel_y, w - 2*MARGIN, panel_h, 7, fill=1, stroke=0)

    labels = [
        ("INVESTIGATOR", 0, 0),
        ("BUSINESS UNIT", 1, 0),
        ("ASSET / AREA", 0, 1),
        ("YEAR", 1, 1),
    ]
    col_gap = 18
    inner_w = w - 2*MARGIN - 28
    col_w = (inner_w - col_gap) / 2
    left = MARGIN + 14
    top = panel_y + panel_h - 30
    for label, col, row in labels:
        x = left + col * (col_w + col_gap)
        y = top - row * 66
        c.setFillColor(HexColor("#95A2A5"))
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(x, y, label)
        c.setStrokeColor(HexColor("#536064"))
        c.setLineWidth(0.8)
        c.line(x, y - 22, x + col_w, y - 22)

    # field-use note
    c.setFillColor(HexColor("#AAB4B6"))
    c.setFont("Helvetica", 7)
    c.drawString(MARGIN, 45, f"Version {VERSION}  •  Optimized for reMarkable and print")
    c.drawRightString(w - MARGIN, 45, "Upstream Oil & Gas Operations")


def draw_header(c, w, h, section, page_num, section_starts):
    """Refined master header/footer and larger tap-friendly navigation."""
    c.setFillColor(WHITE)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # logo and section title
    fit_logo(c, MARGIN, h - 54, 72, 28)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawRightString(w - MARGIN, h - 34, SECTION_TITLES.get(section, section).upper())

    # primary accent rule
    c.setStrokeColor(GREEN)
    c.setLineWidth(2.2)
    c.line(MARGIN, h - 61, w - MARGIN, h - 61)

    # navigation ribbon
    available = w - 2*MARGIN
    tabw = available / len(TABS)
    y = h - 82
    for idx, (key, label) in enumerate(TABS):
        x = MARGIN + idx * tabw
        active = key == section
        c.setFillColor(GREEN if active else FAINT)
        c.roundRect(x + 1, y, tabw - 2, TAB_H, 3, fill=1, stroke=0)
        c.setFillColor(WHITE if active else MID)
        c.setFont("Helvetica-Bold", 5.0)
        c.drawCentredString(x + tabw/2, y + 6, label)
        if key in section_starts:
            c.linkRect('', f'section_{key}', Rect=(x + 1, y, x + tabw - 1, y + TAB_H), relative=0, thickness=0)

    # footer
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.5)
    c.line(MARGIN, 27, w - MARGIN, 27)
    c.setFillColor(MID)
    c.setFont("Helvetica", 6.2)
    c.drawString(MARGIN, 14, f"{TITLE}  |  Version {VERSION}")
    c.drawRightString(w - MARGIN, 14, f"Page {page_num}")
