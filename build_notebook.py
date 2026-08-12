#!/usr/bin/env python3
import argparse
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from config import *
from content import *
from drawing import *


def expand_specs(spec):
    return [(section, idx+1, count) for section,count in spec for idx in range(count)]


def section_starts_for(pages):
    out={}
    for n,(sec,idx,total) in enumerate(pages, start=1):
        if sec not in out: out[sec]=n
    return out


def draw_cover(c,w,h):
    c.setFillColor(DARK); c.rect(0,0,w,h,fill=1,stroke=0)
    c.setFillColor(GREEN); c.rect(0,h*0.71,w,10,fill=1,stroke=0)
    fit_logo(c, MARGIN, h-165, 190, 85)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold",27)
    c.drawString(MARGIN,h-250,"INCIDENT INVESTIGATION")
    c.drawString(MARGIN,h-284,"FIELD NOTEBOOK")
    c.setFillColor(HexColor("#B6C0C2")); c.setFont("Helvetica",11)
    c.drawString(MARGIN,h-310,SUBTITLE)
    c.setStrokeColor(HexColor("#5E686B")); c.setLineWidth(0.7)
    for i,label in enumerate(["INVESTIGATOR","BUSINESS UNIT","ASSET / AREA","YEAR"]):
        y=h-410-i*58
        c.setFillColor(HexColor("#B6C0C2")); c.setFont("Helvetica-Bold",7); c.drawString(MARGIN,y+18,label)
        c.line(MARGIN,y,w-MARGIN,y)
    c.setFillColor(HexColor("#8E9A9D")); c.setFont("Helvetica",7)
    c.drawString(MARGIN,34,"Version 1.0  |  Field-use notebook  |  Optimized for reMarkable")


def draw_contents(c,w,h,idx,starts):
    x,y,bw,bh=body_bounds(w,h); page_title(c,x,y+bh-10,"Contents","Tap a section tab or section name in the combined PDF.")
    items=[("Incident Information","incident"),("Interviews","interviews"),("Timeline","timeline"),("Scene Documentation","scene"),("Equipment & Energy","equipment"),("Human Factors","human"),("Evidence & Photos","evidence"),("Analysis","analysis"),("Corrective Actions","actions"),("Lessons Learned","lessons"),("Sketch Library","sketches"),("Quick Reference","reference"),("Notes","notes")]
    yy=y+bh-58
    for title,key in items:
        c.setFillColor(FAINT); c.roundRect(x,yy-24,bw,29,4,fill=1,stroke=0)
        c.setFillColor(DARK); c.setFont("Helvetica-Bold",8); c.drawString(x+10,yy-12,title)
        if key in starts:
            c.setFillColor(GREEN); c.drawRightString(x+bw-10,yy-12,str(starts[key]))
            c.linkRect('',f'section_{key}',Rect=(x,yy-24,x+bw,yy+5),relative=0,thickness=0)
        yy-=38


def draw_instructions(c,w,h):
    x,y,bw,bh=body_bounds(w,h); page_title(c,x,y+bh-10,"How to Use This Notebook","Capture facts first. Separate observations, evidence, and analysis.")
    tips=[("1","SECURE & DOCUMENT","Address immediate safety needs and preserve scene conditions before they change."),("2","INTERVIEW","Use open-ended questions. Record the person's sequence and terminology accurately."),("3","BUILD THE TIMELINE","Reconcile statements, records, equipment state, and communications."),("4","ANALYZE SYSTEMS","Consider barriers, equipment, planning, work conditions, and human performance influences."),("5","ACT & VERIFY","Assign corrective actions with owners, dates, and effectiveness verification.")]
    yy=y+bh-55
    for n,t,d in tips:
        c.setFillColor(GREEN); c.circle(x+16,yy-8,14,fill=1,stroke=0); c.setFillColor(WHITE); c.setFont("Helvetica-Bold",9); c.drawCentredString(x+16,yy-11,n)
        c.setFillColor(DARK); c.setFont("Helvetica-Bold",9); c.drawString(x+40,yy,t)
        c.setFillColor(MID); c.setFont("Helvetica",7.4); c.drawString(x+40,yy-14,d)
        yy-=72


def draw_incident(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h)
    titles=["Incident Identification","Classification & Consequence","Task & Work Scope","Hazards & Energy Sources","Initial Narrative","Investigation Team & Scope"]
    page_title(c,x,y+bh-10,titles[idx-1])
    top=y+bh-48
    if idx==1:
        cols=2; gap=18; fw=(bw-gap)/2
        for i,label in enumerate(INCIDENT_PROMPTS):
            col=i%2; row=i//2; draw_field(c,x+col*(fw+gap),top-row*47,fw,label)
        draw_section_box(c,x,y+60,bw,170,"INITIAL EVENT SUMMARY","Use concise, factual language. Avoid causes or conclusions.")
        draw_dot_grid(c,x+10,y+72,bw-20,125)
    elif idx==2:
        draw_section_box(c,x,top-120,bw,125,"EVENT CLASSIFICATION")
        xx=x+12; yy=top-42
        for i,item in enumerate(CLASSIFICATIONS):
            draw_checkbox(c,xx+(i%3)*(bw/3),yy-(i//3)*27,item,size=9,font=7)
        draw_section_box(c,x,top-265,bw,115,"ACTUAL CONSEQUENCE")
        draw_dot_grid(c,x+10,top-250,bw-20,62)
        draw_section_box(c,x,y+45,bw,120,"POTENTIAL CONSEQUENCE / SIF POTENTIAL")
        draw_checkbox(c,x+12,y+137,"Potential for serious injury/fatality",size=9)
        draw_dot_grid(c,x+10,y+57,bw-20,62)
    elif idx==3:
        for i,label in enumerate(["Task / activity","Crew / work group","Supervisor / person in charge","Company / contractor","Procedure / SOP reference","JSA / permit reference"]):
            draw_field(c,x,top-i*44,bw,label)
        draw_section_box(c,x,y+55,bw,170,"PLANNED VS. ACTUAL WORK","What was expected? What changed?")
        draw_dot_grid(c,x+10,y+68,bw-20,125)
    elif idx==4:
        draw_section_box(c,x,top-190,bw,195,"ENERGY SOURCES PRESENT")
        for i,item in enumerate(ENERGY_SOURCES): draw_checkbox(c,x+15+(i%2)*bw/2,top-42-(i//2)*29,item,size=9,font=7.4)
        draw_section_box(c,x,y+45,bw,180,"OTHER HAZARDS / CRITICAL CONTROLS")
        draw_dot_grid(c,x+10,y+58,bw-20,135)
    elif idx==5:
        draw_section_box(c,x,y+45,bw,bh-85,"INITIAL FACTUAL NARRATIVE","Describe what happened in sequence. Record known facts and identify unknowns.")
        draw_dot_grid(c,x+10,y+58,bw-20,bh-125)
    else:
        for i,label in enumerate(["Lead investigator","Operations representative","HSE representative","Technical / engineering SME","Contractor representative","Other team member"]): draw_field(c,x,top-i*42,bw,label)
        draw_section_box(c,x,y+45,bw,165,"INVESTIGATION SCOPE","Define what will be examined, key questions, and boundaries.")
        draw_dot_grid(c,x+10,y+58,bw-20,120)


def generic_notes(c,w,h,title,subtitle=None,grid=True):
    x,y,bw,bh=body_bounds(w,h); page_title(c,x,y+bh-10,title,subtitle)
    if grid: draw_dot_grid(c,x,y+35,bw,bh-90)
    else: draw_lined_area(c,x,y+35,bw,bh-90)


def draw_notifications(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Initial Notifications","External / Regulatory Notifications","Notification Notes"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx<3:
        cols=["PERSON / AGENCY","TIME","METHOD","BY WHOM"]
        top=y+bh-60; rh=39; widths=[.42,.17,.18,.23]
        xx=x
        for lab,frac in zip(cols,widths): c.setFillColor(FAINT); c.rect(xx,top,bw*frac,rh,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Helvetica-Bold",6); c.drawCentredString(xx+bw*frac/2,top+15,lab); xx+=bw*frac
        for r in range(8):
            yy=top-(r+1)*rh; xx=x
            for frac in widths: c.setStrokeColor(LIGHT); c.rect(xx,yy,bw*frac,rh,fill=0,stroke=1); xx+=bw*frac
    else: draw_dot_grid(c,x,y+35,bw,bh-90)


def draw_response(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Immediate Response Actions","Scene Control & Preservation","Initial Response Notes"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx==1:
        items=["Medical care / first aid addressed","Emergency response activated if needed","Operations placed in safe condition","Hazardous energy controlled","Area barricaded / access controlled","Leadership / HSE notified","Environmental release controlled","Evidence preserved before cleanup"]
        yy=y+bh-60
        for item in items: draw_checkbox(c,x+8,yy,item,size=10,font=7.6); yy-=34
        draw_section_box(c,x,y+50,bw,155,"IMMEDIATE ACTION DETAILS")
        draw_dot_grid(c,x+10,y+62,bw-20,110)
    elif idx==2:
        items=["Overall scene photographed","Equipment positions recorded","Controls / indicators photographed","Measurements completed","Weather / lighting documented","Witnesses identified","Physical evidence tagged","Equipment held from repair pending release"]
        yy=y+bh-60
        for item in items: draw_checkbox(c,x+8,yy,item,size=10,font=7.6); yy-=34
        draw_section_box(c,x,y+50,bw,155,"SCENE PRESERVATION NOTES")
        draw_dot_grid(c,x+10,y+62,bw-20,110)
    else: draw_dot_grid(c,x,y+35,bw,bh-90)


def draw_interviews(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h)
    titles=["Interview Information","Open Narrative","Before the Event","During the Event","After the Event","Work Conditions","Clarifying Questions","Interview Follow-Up"]
    page_title(c,x,y+bh-10,titles[idx-1],"Use open-ended, non-leading questions and record the person's own words where practical.")
    if idx==1:
        for i,label in enumerate(["Interviewee","Company","Job title / role","Interview date","Start / end time","Interview location","Interviewer(s)","Relationship to event"]): draw_field(c,x+(i%2)*(bw/2+5),y+bh-58-(i//2)*46,bw/2-10,label)
        draw_section_box(c,x,y+55,bw,165,"INVESTIGATOR OBSERVATIONS")
        draw_dot_grid(c,x+10,y+68,bw-20,120)
    elif idx in (2,3,4,5):
        prompts={2:"Tell me what happened from the beginning.",3:"What was happening before the event? What was the plan?",4:"Walk me through the event step-by-step. What did you see, hear, or feel?",5:"What happened immediately afterward? What actions were taken?"}
        draw_section_box(c,x,y+45,bw,bh-85,prompts[idx])
        draw_dot_grid(c,x+10,y+58,bw-20,bh-125)
    elif idx==6:
        for i,item in enumerate(HUMAN_FACTORS): draw_checkbox(c,x+8+(i%2)*bw/2,y+bh-64-(i//2)*31,item,size=9,font=7)
        draw_section_box(c,x,y+45,bw,190,"CONDITIONS THAT SHAPED THE WORK")
        draw_dot_grid(c,x+10,y+58,bw-20,145)
    else:
        generic_notes(c,w,h,titles[idx-1],"Capture unanswered questions, conflicts, documents to verify, and follow-up interviews.")


def draw_timeline(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Master Event Timeline","Planned vs. Actual Sequence","Communications Timeline","Decision Points","24-Hour Timeline Sketch"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx<=4:
        heads=[["TIME","EVENT / ACTION","SOURCE / VERIFICATION"],["STEP","PLANNED","ACTUAL / CHANGE"],["TIME","PERSON / METHOD","MESSAGE / INFORMATION"],["TIME","DECISION","INFORMATION AVAILABLE"]][idx-1]
        widths=[.16,.49,.35] if idx==1 else [.16,.42,.42]
        top=y+bh-58; rh=42; xx=x
        for lab,frac in zip(heads,widths): c.setFillColor(FAINT); c.rect(xx,top,bw*frac,rh,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Helvetica-Bold",6); c.drawCentredString(xx+bw*frac/2,top+16,lab); xx+=bw*frac
        for r in range(10):
            yy=top-(r+1)*rh; xx=x
            for frac in widths: c.setStrokeColor(LIGHT); c.rect(xx,yy,bw*frac,rh,fill=0,stroke=1); xx+=bw*frac
    else:
        c.setStrokeColor(DARK); c.setLineWidth(1); mid=y+bh/2; c.line(x,mid,x+bw,mid)
        for i in range(13):
            xx=x+i*bw/12; c.line(xx,mid-6,xx,mid+6); c.setFillColor(MID); c.setFont("Helvetica",5.7); c.drawCentredString(xx,mid+12,f"{i*2:02d}00")
        draw_dot_grid(c,x,y+35,bw,bh/2-45)


def draw_scene(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Scene Overview","Environmental Conditions","Equipment Position Log","Measurements","Critical Controls at Scene","Scene Sketch & Notes"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx==1:
        for i,label in enumerate(["Arrival date/time","GPS coordinates","Weather","Lighting","Area secured by","Scene changes before arrival"]): draw_field(c,x+(i%2)*(bw/2+5),y+bh-58-(i//2)*47,bw/2-10,label)
        draw_section_box(c,x,y+55,bw,240,"INITIAL OBSERVATIONS")
        draw_dot_grid(c,x+10,y+68,bw-20,195)
    elif idx in (2,5):
        items=["Lighting","Weather","Wind","Ground / surface","Housekeeping","Visibility","Access / egress","Congestion","Barricades","Guards","Spotter","Communication plan","Permit / JSA","Energy isolation"]
        for i,item in enumerate(items): draw_checkbox(c,x+8+(i%2)*bw/2,y+bh-62-(i//2)*30,item,size=9,font=7.1)
        draw_section_box(c,x,y+45,bw,190,"OBSERVATIONS")
        draw_dot_grid(c,x+10,y+58,bw-20,145)
    elif idx in (3,4):
        heads=["ITEM / EQUIPMENT","POSITION / MEASUREMENT","REFERENCE / NOTES"]
        widths=[.34,.31,.35]; top=y+bh-60; rh=47; xx=x
        for lab,frac in zip(heads,widths): c.setFillColor(FAINT); c.rect(xx,top,bw*frac,rh,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Helvetica-Bold",6); c.drawCentredString(xx+bw*frac/2,top+18,lab); xx+=bw*frac
        for r in range(9):
            yy=top-(r+1)*rh; xx=x
            for frac in widths: c.setStrokeColor(LIGHT); c.rect(xx,yy,bw*frac,rh,fill=0,stroke=1); xx+=bw*frac
    else: draw_dot_grid(c,x,y+35,bw,bh-90)


def draw_evidence(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Evidence Register","Photo Log","Document Review Log","Digital Evidence Log","Evidence Summary"]
    page_title(c,x,y+bh-10,titles[idx-1])
    heads=["ID","DESCRIPTION / SUBJECT","SOURCE / LOCATION","DATE / REF"]
    widths=[.12,.43,.27,.18]; top=y+bh-60; rh=44; xx=x
    for lab,frac in zip(heads,widths): c.setFillColor(FAINT); c.rect(xx,top,bw*frac,rh,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Helvetica-Bold",5.8); c.drawCentredString(xx+bw*frac/2,top+17,lab); xx+=bw*frac
    for r in range(10):
        yy=top-(r+1)*rh; xx=x
        for frac in widths: c.setStrokeColor(LIGHT); c.rect(xx,yy,bw*frac,rh,fill=0,stroke=1); xx+=bw*frac


def draw_equipment(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Equipment Identification","Hazardous Energy Assessment","Isolation & Verification","Safety Devices","Mechanical Integrity","Failure Mode Observations"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx==1:
        for i,label in enumerate(["Equipment description","Asset / serial number","Manufacturer / model","Owner","Inspection status","Maintenance reference"]): draw_field(c,x+(i%2)*(bw/2+5),y+bh-58-(i//2)*48,bw/2-10,label)
        generic_notes(c,w,h,titles[idx-1],"Record equipment condition before repair, adjustment, or return to service.")
    elif idx==2:
        for i,item in enumerate(ENERGY_SOURCES): draw_checkbox(c,x+8+(i%2)*bw/2,y+bh-62-(i//2)*34,item,size=10,font=7.5)
        draw_section_box(c,x,y+45,bw,205,"ENERGY SOURCE DETAILS / STORED ENERGY")
        draw_dot_grid(c,x+10,y+58,bw-20,160)
    elif idx==3:
        items=["Lock / tag","Electrical disconnect","Valve isolation","Blind / blank","Double block & bleed","Pressure released","Mechanical block","Lowered to stable position","Zero energy verified","Try/test performed"]
        for i,item in enumerate(items): draw_checkbox(c,x+8+(i%2)*bw/2,y+bh-62-(i//2)*34,item,size=10,font=7.4)
        draw_section_box(c,x,y+45,bw,190,"VERIFICATION METHOD & OBSERVATIONS")
        draw_dot_grid(c,x+10,y+58,bw-20,145)
    else: generic_notes(c,w,h,titles[idx-1])


def draw_human(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Work Context","Communication & Coordination","Procedures & Work Practices","Work Environment","Performance Influences","Organizational Factors"]
    page_title(c,x,y+bh-10,titles[idx-1],"Understand how conditions shaped performance; do not assign blame based on outcome.")
    if idx in (1,5):
        for i,item in enumerate(HUMAN_FACTORS): draw_checkbox(c,x+8+(i%2)*bw/2,y+bh-62-(i//2)*31,item,size=9,font=7)
        draw_section_box(c,x,y+45,bw,185,"OBSERVATIONS / EVIDENCE")
        draw_dot_grid(c,x+10,y+58,bw-20,140)
    else: generic_notes(c,w,h,titles[idx-1])


def draw_analysis(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Investigation Summary","Contributing Factors","Barrier Analysis","5 Whys","Root Cause / System Findings","Analysis Cross-Check"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx==3:
        heads=["BARRIER","PRESENT?","EFFECTIVE?","EVIDENCE / COMMENTS"]; widths=[.32,.15,.15,.38]; top=y+bh-60; rh=45; xx=x
        for lab,frac in zip(heads,widths): c.setFillColor(FAINT); c.rect(xx,top,bw*frac,rh,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Helvetica-Bold",5.7); c.drawCentredString(xx+bw*frac/2,top+17,lab); xx+=bw*frac
        for r in range(10):
            yy=top-(r+1)*rh; xx=x
            for frac in widths: c.setStrokeColor(LIGHT); c.rect(xx,yy,bw*frac,rh,fill=0,stroke=1); xx+=bw*frac
    elif idx==4:
        yy=y+bh-60
        for n in range(1,6):
            draw_section_box(c,x,yy-78,bw,72,f"WHY {n}")
            draw_lined_area(c,x+10,yy-68,bw-20,42,20); yy-=86
    else: generic_notes(c,w,h,titles[idx-1])


def draw_actions(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h); titles=["Corrective Action Register","Immediate Actions","Long-Term Actions","Action Quality Review","Verification of Effectiveness","Investigation Closure"]
    page_title(c,x,y+bh-10,titles[idx-1])
    if idx in (1,3):
        heads=["ID","ACTION","OWNER","DUE","STATUS"]; widths=[.10,.48,.18,.12,.12]; top=y+bh-60; rh=47; xx=x
        for lab,frac in zip(heads,widths): c.setFillColor(FAINT); c.rect(xx,top,bw*frac,rh,fill=1,stroke=0); c.setFillColor(DARK); c.setFont("Helvetica-Bold",5.8); c.drawCentredString(xx+bw*frac/2,top+18,lab); xx+=bw*frac
        for r in range(9):
            yy=top-(r+1)*rh; xx=x
            for frac in widths: c.setStrokeColor(LIGHT); c.rect(xx,yy,bw*frac,rh,fill=0,stroke=1); xx+=bw*frac
    else: generic_notes(c,w,h,titles[idx-1])


def draw_lessons(c,w,h,idx):
    titles=["What Went Well","Opportunities for Improvement","Lessons Learned for Sharing"]
    generic_notes(c,w,h,titles[idx-1],"Capture learning that can improve similar work elsewhere.")


def draw_reference(c,w,h,idx):
    x,y,bw,bh=body_bounds(w,h)
    titles=["Investigation Workflow","Interview Best Practices","Evidence Collection Checklist","Photo Documentation Checklist","Scene Preservation Checklist","Common Investigation Pitfalls","Oil & Gas Hazard Reference","Field Measurement Guide"]
    page_title(c,x,y+bh-10,titles[idx-1])
    refs={
        1:["Address immediate safety needs","Secure and preserve the scene","Document initial conditions","Interview separately","Collect and organize evidence","Build and validate the timeline","Analyze barriers and system factors","Assign actions and verify effectiveness","Share lessons learned"],
        2:["Start broad: Tell me what happened","Ask what was expected and what changed","Avoid leading or blame-focused wording","Ask what information was available at the time","Clarify sequence, positions, signals, and equipment state","Ask what made the work easier or harder","End with: What else should I know?"],
        3:["Overall scene","Equipment positions","Damaged components","Controls / indicators","JSA / permit / procedure","Training / qualification records","Inspection / maintenance records","SCADA / alarm / trend data","Measurements and sketches","Witness statements"],
        4:["Overall orientation","Mid-range context","Close-up detail","Use scale / ruler when useful","Capture labels and IDs","Photograph before moving items","Record direction / viewpoint","Avoid relying on digital zoom"],
        5:["Control access","Photograph before disturbance","Record weather and lighting","Document equipment state","Measure before cleanup","Identify witnesses","Tag physical evidence","Hold relevant components pending release"],
        6:["Confirmation bias","Hindsight bias","Anchoring on first explanation","Single-cause thinking","Mixing assumptions with facts","Overlooking successful controls","Corrective actions limited to retraining","Failure to verify effectiveness"],
        7:["Line of fire","Stored energy","Pressure release","Dropped object","Mobile equipment","Electrical exposure","H2S / toxic gas","Fire / explosion","Excavation / underground utilities","Working at height"],
        8:["Record units","Establish a fixed reference point","Capture height / width / clearance","Record equipment orientation","Note valve / control positions","Use sketches with north arrow","Cross-reference photos","Verify critical measurements when practical"],
    }
    yy=y+bh-58
    for item in refs[idx]: draw_checkbox(c,x+8,yy,item,size=9,font=7.5); yy-=34
    draw_section_box(c,x,y+45,bw,155,"FIELD NOTES")
    draw_dot_grid(c,x+10,y+58,bw-20,110)


def draw_sketch(c,w,h,idx):
    titles=["Well Pad Layout","Tank Battery / Facility","Workover Rig Layout","Drilling Rig Layout","Pipeline / ROW","Excavation / Utility Crossing","Vehicle / Mobile Equipment Scene","Blank Engineering Grid"]
    x,y,bw,bh=body_bounds(w,h); page_title(c,x,y+bh-10,titles[idx-1],"Use arrows, dimensions, equipment IDs, north arrow, and photo references.")
    # engineering-style grid
    c.setStrokeColor(HexColor("#E7EBEC")); c.setLineWidth(0.25)
    spacing=14
    yy=y+35
    while yy<y+bh-55:
        c.line(x,yy,x+bw,yy); yy+=spacing
    xx=x
    while xx<x+bw:
        c.line(xx,y+35,xx,y+bh-55); xx+=spacing
    c.setStrokeColor(MID); c.setLineWidth(0.8); c.rect(x,y+35,bw,bh-90,fill=0,stroke=1)
    c.setFillColor(MID); c.setFont("Helvetica-Bold",7); c.drawString(x+8,y+45,"NORTH  ↑")


def render_page(c,w,h,sec,idx,total,page_num,starts):
    if sec=="cover": draw_cover(c,w,h); return
    if sec in starts and starts[sec]==page_num:
        c.bookmarkPage(f'section_{sec}'); c.addOutlineEntry(SECTION_TITLES.get(sec,sec),f'section_{sec}',level=0,closed=False)
    draw_header(c,w,h,sec,page_num,starts)
    if sec=="contents": draw_contents(c,w,h,idx,starts)
    elif sec=="instructions": draw_instructions(c,w,h)
    elif sec=="incident": draw_incident(c,w,h,idx)
    elif sec=="notifications": draw_notifications(c,w,h,idx)
    elif sec=="response": draw_response(c,w,h,idx)
    elif sec=="interviews": draw_interviews(c,w,h,idx)
    elif sec=="timeline": draw_timeline(c,w,h,idx)
    elif sec=="scene": draw_scene(c,w,h,idx)
    elif sec=="evidence": draw_evidence(c,w,h,idx)
    elif sec=="equipment": draw_equipment(c,w,h,idx)
    elif sec=="human": draw_human(c,w,h,idx)
    elif sec=="analysis": draw_analysis(c,w,h,idx)
    elif sec=="actions": draw_actions(c,w,h,idx)
    elif sec=="lessons": draw_lessons(c,w,h,idx)
    elif sec=="reference": draw_reference(c,w,h,idx)
    elif sec=="sketches": draw_sketch(c,w,h,idx)
    elif sec=="notes": generic_notes(c,w,h,"Investigator Notes","5 mm dot grid")


def build_pdf(path, specs, fmt="remarkable"):
    pages=expand_specs(specs); starts=section_starts_for(pages); w,h=PAGE_SIZES[fmt]
    c=canvas.Canvas(str(path),pagesize=(w,h),pageCompression=1)
    c.setTitle(TITLE); c.setAuthor("Hilcorp Incident Investigation Notebook Project")
    for page_num,(sec,idx,total) in enumerate(pages,start=1):
        render_page(c,w,h,sec,idx,total,page_num,starts)
        c.showPage()
    c.save(); return len(pages)


def all_specs():
    combined=[]
    for specs in RELEASES.values(): combined.extend(specs)
    return combined


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--format",choices=PAGE_SIZES.keys(),default="remarkable")
    ap.add_argument("--all-formats",action="store_true")
    args=ap.parse_args()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    formats=list(PAGE_SIZES) if args.all_formats else [args.format]
    for fmt in formats:
        for name,specs in RELEASES.items():
            n=build_pdf(OUTPUT/f"{name}_{fmt}.pdf",specs,fmt); print(f"Built {name}_{fmt}.pdf ({n} pages)")
        n=build_pdf(OUTPUT/f"Hilcorp_Incident_Investigation_Field_Notebook_v1_{fmt}.pdf",all_specs(),fmt)
        print(f"Built combined {fmt} PDF ({n} pages)")

if __name__=="__main__": main()
