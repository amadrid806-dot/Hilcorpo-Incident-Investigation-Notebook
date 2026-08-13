from reportlab.lib.units import mm
from config import *
from content import SECTION_TITLES, TABS


def fit_logo(c, x, y, max_w, max_h, path=LOGO):
    """Fit the supplied project logo into a fixed box without distortion."""
    if not path.exists():
        return
    from PIL import Image
    im = Image.open(path)
    w, h = im.size
    scale = min(max_w / w, max_h / h)
    dw, dh = w * scale, h * scale
    c.drawImage(
        str(path), x, y + (max_h - dh) / 2,
        width=dw, height=dh,
        preserveAspectRatio=True, mask='auto'
    )


def draw_checkbox(c, x, y, label, checked=False, size=9, font=7.2):
    """Stylus-friendly checkbox with slightly larger target area."""
    c.setStrokeColor(MID)
    c.setLineWidth(0.7)
    c.rect(x, y - size + 1, size, size, fill=0)
    if checked:
        c.setStrokeColor(DARK)
        c.setLineWidth(1.1)
        c.line(x + 1.8, y - 3.5, x + 3.8, y - 5.7)
        c.line(x + 3.8, y - 5.7, x + 7.3, y - 1.8)
    c.setFillColor(DARK)
    c.setFont("Helvetica", font)
    c.drawString(x + size + 5, y - size + 1.8, label)


def draw_field(c, x, y, w, label, h=30, small=False):
    c.setFillColor(MID)
    c.setFont("Helvetica-Bold", 6.7 if small else 7.4)
    c.drawString(x, y, label.upper())
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.65)
    c.line(x, y - 16, x + w, y - 16)


def draw_dot_grid(c, x, y, w, h, spacing_mm=GRID_MM, dot=0.38):
    """Low-contrast 5 mm grid optimized for handwriting and sketching."""
    spacing = spacing_mm * mm
    c.setFillColor(GRID)
    yy = y
    while yy <= y + h:
        xx = x
        while xx <= x + w:
            c.circle(xx, yy, dot, stroke=0, fill=1)
            xx += spacing
        yy += spacing


def draw_lined_area(c, x, y, w, h, spacing=25):
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.45)
    yy = y + h - spacing
    while yy > y:
        c.line(x, yy, x + w, yy)
        yy -= spacing


def draw_section_box(c, x, y, w, h, title, subtitle=None):
    c.setFillColor(FAINT)
    c.roundRect(x, y, w, h, 7, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 11, y + h - 18, title)
    if subtitle:
        c.setFillColor(MID)
        c.setFont("Helvetica", 6.8)
        c.drawString(x + 11, y + h - 31, subtitle)


def _draw_nav_ribbon(c, w, h, section, section_starts):
    """Compact top navigation with larger tap targets and active-state emphasis."""
    available = w - 2 * MARGIN
    tabw = available / len(TABS)
    y = h - 86
    for i, (key, label) in enumerate(TABS):
        x = MARGIN + i * tabw
        active = key == section
        c.setFillColor(GREEN if active else FAINT)
        c.roundRect(x + 1, y, tabw - 2, TAB_H, 3.5, fill=1, stroke=0)
        c.setFillColor(WHITE if active else MID)
        c.setFont("Helvetica-Bold", 5.0)
        c.drawCentredString(x + tabw / 2, y + 7, label)
        if key in section_starts:
            c.linkRect(
                '', f'section_{key}',
                Rect=(x + 1, y, x + tabw - 1, y + TAB_H),
                relative=0, thickness=0
            )


def draw_header(c, w, h, section, page_num, section_starts):
    """Master interior page: clean brand strip, navigation, footer, and page number."""
    c.setFillColor(WHITE)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Header brand lockup
    fit_logo(c, MARGIN, h - 59, 72, 31)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawRightString(w - MARGIN, h - 35, SECTION_TITLES.get(section, section).upper())
    c.setStrokeColor(GREEN)
    c.setLineWidth(2.2)
    c.line(MARGIN, h - 65, w - MARGIN, h - 65)

    _draw_nav_ribbon(c, w, h, section, section_starts)

    # Footer
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.45)
    c.line(MARGIN, 26, w - MARGIN, 26)
    c.setFillColor(MID)
    c.setFont("Helvetica", 6.0)
    c.drawString(MARGIN, 14, f"{TITLE}  |  v{VERSION}")
    c.drawRightString(w - MARGIN, 14, f"Page {page_num}")


def page_title(c, x, y, title, subtitle=None):
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 15.5)
    c.drawString(x, y, title)
    c.setStrokeColor(GREEN)
    c.setLineWidth(1.4)
    c.line(x, y - 7, x + 38, y - 7)
    if subtitle:
        c.setFillColor(MID)
        c.setFont("Helvetica", 7.4)
        c.drawString(x, y - 20, subtitle)


def body_bounds(w, h):
    """Consistent writing-first body area."""
    return MARGIN, 42, w - 2 * MARGIN, h - 140
