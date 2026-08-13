from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LOGO = ASSETS / "logo" / "hilcorp_logo.jpg"
OUTPUT = ROOT / "output"

PAGE_SIZES = {
    "remarkable": letter,
    "letter": letter,
    "a4": A4,
}

# Brand + e-ink palette
GREEN = HexColor("#007A53")
GREEN_DARK = HexColor("#005C3F")
DARK = HexColor("#172124")
MID = HexColor("#697579")
LIGHT = HexColor("#DDE3E4")
FAINT = HexColor("#F4F6F6")
WHITE = HexColor("#FFFFFF")
GRID = HexColor("#C7CDCF")

# Layout constants tuned for handwriting and reMarkable use
MARGIN = 36
HEADER_H = 72
FOOTER_H = 30
TAB_H = 20
GRID_MM = 5
BODY_TOP_GAP = 8
VERSION = "1.2"
TITLE = "Hilcorp Incident Investigation Field Notebook"
SUBTITLE = "Upstream Oil & Gas Operations"
REVISION = "Design refinement release"
