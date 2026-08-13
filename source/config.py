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

GREEN = HexColor("#007A53")
DARK = HexColor("#172124")
MID = HexColor("#697579")
LIGHT = HexColor("#E6EAEB")
FAINT = HexColor("#F3F5F5")
WHITE = HexColor("#FFFFFF")

MARGIN = 34
HEADER_H = 70
FOOTER_H = 28
TAB_H = 18
GRID_MM = 5
VERSION = "1.0"
TITLE = "Hilcorp Incident Investigation Field Notebook"
SUBTITLE = "Upstream Oil & Gas Operations"
