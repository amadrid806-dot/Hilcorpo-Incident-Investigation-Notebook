"""Structured content for the notebook.
All prompts are intentionally general and not tied to any specific incident.
"""

RELEASES = {
    "release-01-foundation": [
        ("cover", 1), ("contents", 2), ("instructions", 1),
        ("incident", 6), ("notifications", 3), ("response", 3), ("notes", 8),
    ],
    "release-02-investigation": [
        ("interviews", 8), ("timeline", 5), ("scene", 6), ("evidence", 5),
    ],
    "release-03-analysis": [
        ("equipment", 6), ("human", 6), ("analysis", 6), ("actions", 6),
    ],
    "release-04-reference": [
        ("lessons", 3), ("reference", 8), ("sketches", 8), ("notes", 5),
    ],
}

SECTION_TITLES = {
    "cover": "Cover",
    "contents": "Contents",
    "instructions": "How to Use",
    "incident": "Incident Information",
    "notifications": "Notifications",
    "response": "Initial Response",
    "interviews": "Interviews",
    "timeline": "Timeline",
    "scene": "Scene Documentation",
    "evidence": "Evidence & Photos",
    "equipment": "Equipment & Energy",
    "human": "Human Factors",
    "analysis": "Analysis",
    "actions": "Corrective Actions",
    "lessons": "Lessons Learned",
    "reference": "Quick Reference",
    "sketches": "Sketch Library",
    "notes": "Notes",
}

TABS = [
    ("incident", "INCIDENT"), ("interviews", "INTERVIEW"),
    ("timeline", "TIMELINE"), ("scene", "SCENE"),
    ("equipment", "EQUIPMENT"), ("human", "HUMAN"),
    ("evidence", "EVIDENCE"), ("analysis", "ANALYSIS"),
    ("actions", "ACTIONS"), ("sketches", "SKETCHES"),
    ("reference", "REFERENCE"),
]

INCIDENT_PROMPTS = [
    "Incident / Event Number", "Date", "Time", "Business Unit", "Asset / Area",
    "Well / Facility / Location", "GPS Coordinates", "Lead Investigator",
]

CLASSIFICATIONS = [
    "Injury / Illness", "Near Miss", "Property Damage", "Vehicle",
    "Environmental", "Fire / Explosion", "Process Safety", "Security", "Other",
]

ENERGY_SOURCES = [
    "Electrical", "Mechanical", "Hydraulic", "Pneumatic", "Pressure",
    "Gravity", "Thermal", "Chemical", "H2S", "Stored Energy",
]

HUMAN_FACTORS = [
    "Planning / preparation", "Communication / coordination", "Procedure usability",
    "Training / experience", "Workload / competing priorities", "Fatigue / hours worked",
    "Time pressure", "Unexpected conditions", "Distractions / interruptions",
    "Workspace / access", "Tool / equipment availability", "Supervision / leadership",
]
