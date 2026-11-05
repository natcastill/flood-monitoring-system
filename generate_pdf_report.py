#!/usr/bin/env python3
"""
generate_pdf_report.py - Compiles Workshop 1 Project Definition Report into PDF
Using ReportLab
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Data Analysis Programming (2026-II) — Workshop No. 1 Report")
            self.drawRightString(612 - 54, 750, "Team 2: Flood Monitoring and Risk (Texas)")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "Universidad Distrital Francisco José de Caldas — School of Engineering")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 46, 612 - 54, 46)
        
        self.restoreState()

def build_pdf():
    pdf_filename = os.path.join("workshop_1", "Project_Definition_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1A202C")
    )

    story = []

    # Title Block
    story.append(Paragraph("Data Analysis Programming — Semester 2026-II", subtitle_style))
    story.append(Paragraph("Workshop No. 1 — Hazard Definition, Source Validation, and Data Contract", title_style))
    story.append(Paragraph("<b>Hazard System:</b> Flood Monitoring and Risk (Texas Scope)<br/><b>Team 2:</b> Oscar Durán (20212020080), Laura Pardo (20221020146), Nicolás Romero (20222020023)<br/><b>Professor:</b> Eng. Carlos Andrés Sierra, M.Sc. | <b>Institution:</b> Universidad Distrital Francisco José de Caldas", body_style))
    story.append(Spacer(1, 10))

    # Section 1
    story.append(Paragraph("1. Project Overview & Hazard Definition", h1_style))
    story.append(Paragraph("<b>1.1 Physical Phenomenon & Motivation:</b> Flooding is one of the most recurring and destructive natural hazards in Texas, characterized by its exposure to the Gulf of Mexico (tropical moisture and hurricane surges) and the steep terrain of the Balcones Escarpment, historically designated as <i>Flash Flood Alley</i>. The system monitors flash floods (rapid runoff in urban and hill terrains), riverine floods (major river basin crests), and coastal surges.", body_style))
    story.append(Paragraph("<b>1.2 Severity Measurement & Units:</b> Quantified via rainfall accumulation (mm and inches over 1h, 3h, 24h, and 7d), flood crest heights (meters/feet above flood stage), direct economic losses (USD), fatalities, and National Weather Service alert severity levels (Minor, Moderate, Severe, Extreme).", body_style))
    story.append(Paragraph("<b>1.3 Geographic and Temporal Scope:</b> State of Texas (FIPS: 48), with dedicated monitoring focus on Harris County (Houston), Travis County (Austin), Bexar County (San Antonio), and Dallas/Tarrant counties. Historical baseline covers <b>2019 to 2024 (6 multi-year seasons)</b>, while the operational near-real-time situation monitors active NWS alerts, sub-hourly ASOS observations, and 7-day cumulative rainfall.", body_style))
    story.append(Paragraph("<b>1.4 Scope Exclusions:</b> Structural hydrodynamic 2D shallow-water simulations (e.g. HEC-RAS), pipe-level urban sewer networks, private insurance underwriting, and multi-decadal climate forecast modeling.", body_style))
    
    story.append(Spacer(1, 8))

    # Section 2
    story.append(Paragraph("2. Functional User & User Stories", h1_style))
    story.append(Paragraph("<b>Target Functional User:</b> Emergency Management Specialist / Hydrological Risk Analyst (e.g., Texas Division of Emergency Management - TDEM, Harris County Flood Control District). Supported decisions include barricading flooded low-water crossings, pre-positioning water rescue personnel, issuing localized evacuation advisories, and evaluating antecedent soil saturation.", body_style))
    
    user_stories_data = [
        [Paragraph("<b>ID</b>", body_style), Paragraph("<b>MoSCoW</b>", body_style), Paragraph("<b>User Story</b>", body_style), Paragraph("<b>Acceptance Criteria</b>", body_style)],
        [Paragraph("US-01", body_style), Paragraph("Must", body_style), Paragraph("As an emergency analyst, I want to view active NWS Flood and Flash Flood warnings on an interactive map so that I can immediately identify counties at risk.", body_style), Paragraph("Alerts rendered within 5m of publication, color-coded by severity, showing affected counties and expiration.", body_style)],
        [Paragraph("US-02", body_style), Paragraph("Must", body_style), Paragraph("As an operational analyst, I want to query live precipitation accumulations (1h, 3h, 24h) from airport stations (ASOS) so that I can detect flash flood conditions.", body_style), Paragraph("Station table updated sub-hourly, rainfall shown in mm with alerts for rates >25 mm/h.", body_style)],
        [Paragraph("US-03", body_style), Paragraph("Must", body_style), Paragraph("As a researcher, I want to compare current rainfall against the 5-year GHCN-Daily historical distribution so that I can detect anomalous rain (>95th percentile).", body_style), Paragraph("Historical percentiles computed per station-month; anomaly flag raised when exceeded.", body_style)],
        [Paragraph("US-04", body_style), Paragraph("Should", body_style), Paragraph("As a civil protection director, I want an automated Flood Risk Index (LOW / MED / HIGH / CRITICAL) so that command staff can deploy rescue assets objectively.", body_style), Paragraph("Index combining rainfall, alert tier, and recurrence score, refreshed every cycle.", body_style)],
        [Paragraph("US-05", body_style), Paragraph("Should", body_style), Paragraph("As a data engineer, I want to inspect watermark timestamps, pipeline runs, and rejected records so that I can verify data freshness and integrity.", body_style), Paragraph("Audit view displaying last poll timestamp, row counts, and error payloads for quarantined items.", body_style)],
        [Paragraph("US-06", body_style), Paragraph("Could", body_style), Paragraph("As an analyst, I want to correlate historical property damage with precipitation totals so that I can evaluate monetary vulnerability thresholds.", body_style), Paragraph("Correlation view linking NOAA Storm Events damages with GHCN rainfall.", body_style)]
    ]
    t_us = Table(user_stories_data, colWidths=[36, 46, 230, 192])
    t_us.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_us)

    story.append(Spacer(1, 10))

    # Section 3
    story.append(Paragraph("3. Four Validated Data Sources with Real Evidence", h1_style))
    story.append(Paragraph("All four sources were queried programmatically; authentic raw responses were preserved in <code>workshop_1/samples/</code>:", body_style))
    
    sources_summary = [
        [Paragraph("<b>Source Name</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Format</b>", body_style), Paragraph("<b>Records Retrieved</b>", body_style), Paragraph("<b>License & Auth</b>", body_style)],
        [Paragraph("NOAA Storm Events Database", body_style), Paragraph("Historical", body_style), Paragraph("Bulk CSV.GZ", body_style), Paragraph("582 (Texas 2024)", body_style), Paragraph("Public Domain (No auth)", body_style)],
        [Paragraph("GHCN-Daily via NCEI Access API", body_style), Paragraph("Historical", body_style), Paragraph("REST JSON", body_style), Paragraph("2,188 (2023-2024)", body_style), Paragraph("Public Domain (No auth)", body_style)],
        [Paragraph("NWS Station Observations API", body_style), Paragraph("Incremental", body_style), Paragraph("GeoJSON", body_style), Paragraph("500 (Texas ASOS)", body_style), Paragraph("Public Domain (User-Agent)", body_style)],
        [Paragraph("NWS Active Alerts API", body_style), Paragraph("Incremental", body_style), Paragraph("GeoJSON / CAP", body_style), Paragraph("253 (Texas alerts)", body_style), Paragraph("Public Domain (User-Agent)", body_style)],
    ]
    t_src = Table(sources_summary, colWidths=[140, 60, 70, 104, 130])
    t_src.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_src)

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Empirical Update Characterization:</b> Observations at Houston Hobby (KHOU) polled across a 60-minute interval confirmed timestamp advancement by exactly 1 hour with updated sensor readings. Active alert polling across 90 minutes verified that expired advisories disappear while new convective statements append. The watermark will track <code>properties.sent</code> with a 2-hour lookback window to catch alert cancellations and updates.", body_style))

    story.append(PageBreak())

    # Section 4
    story.append(Paragraph("4. Source Profiling & Data Quality Findings", h1_style))
    story.append(Paragraph("Executed top-to-bottom profiling in <code>notebooks/01_source_profiling.ipynb</code> identified five concrete data quality problems with real examples:", body_style))

    dq_findings = [
        Paragraph("<b>1. GHCN-Daily Whitespace Padding & String Typing:</b> Numeric fields (<code>PRCP</code>, <code>TMAX</code>) are returned as whitespace-padded strings (e.g. <code>'  104'</code>). Direct arithmetic raises <code>TypeError</code> without explicit stripping and coercion.", bullet_style),
        Paragraph("<b>2. GHCN-Daily Implicit Scaling:</b> Precipitation is reported in tenths of a millimeter without unit metadata (e.g. <code>'  612'</code> for San Antonio on 2024-01-22). Uncalibrated ingestion causes a 10x overestimation error ($61.2\\text{ mm}$ vs $612\\text{ mm}$).", bullet_style),
        Paragraph("<b>3. NOAA Storm Events Fragmented Non-UTC Timestamps:</b> Dates are fragmented across 4 columns (<code>BEGIN_YEARMONTH</code>, <code>BEGIN_DAY</code>, <code>BEGIN_TIME</code>, <code>CZ_TIMEZONE</code>) in civil daylight saving codes (<code>CST-6</code>, <code>CDT-5</code>), requiring timezone offset normalization.", bullet_style),
        Paragraph("<b>4. NWS Observations Sparseness in Accumulation Sensors:</b> Over 85% of records contain <code>value: null</code> for <code>precipitationLast3Hours</code>. The system must explicitly differentiate between zero rainfall and sensor offline status.", bullet_style),
        Paragraph("<b>5. NWS Alerts Spatial Geometry Disparity:</b> 36.4% of alerts lack GeoJSON geometry (<code>geometry: null</code>), relying strictly on county UGC/SAME codes. Direct PostGIS spatial joins require an administrative boundary lookup table.", bullet_style),
    ]
    for dq in dq_findings:
        story.append(dq)

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Cross-Source Overlap Verification (5 Real Event Pairs):</b>", h2_style))
    story.append(Paragraph("Cross-source matching linked NOAA Storm Events flood reports with GHCN-Daily station rainfall on identical dates and counties in Texas during 2024:", body_style))

    overlap_data = [
        [Paragraph("<b>Date</b>", body_style), Paragraph("<b>County</b>", body_style), Paragraph("<b>Storm Event ID</b>", body_style), Paragraph("<b>Reported Hazard</b>", body_style), Paragraph("<b>Coordinates</b>", body_style), Paragraph("<b>GHCN Rain</b>", body_style), Paragraph("<b>GHCN Station</b>", body_style)],
        [Paragraph("2024-01-22", body_style), Paragraph("BEXAR", body_style), Paragraph("1159212", body_style), Paragraph("Flash Flood", body_style), Paragraph("(29.48, -98.49)", body_style), Paragraph("61.2 mm", body_style), Paragraph("USW00012921", body_style)],
        [Paragraph("2024-01-24", body_style), Paragraph("HARRIS", body_style), Paragraph("1160174", body_style), Paragraph("Flood", body_style), Paragraph("(30.10, -95.76)", body_style), Paragraph("48.3 mm", body_style), Paragraph("USW00012918", body_style)],
        [Paragraph("2024-01-24", body_style), Paragraph("BEXAR", body_style), Paragraph("1159392", body_style), Paragraph("Flash Flood", body_style), Paragraph("(29.41, -98.61)", body_style), Paragraph("40.6 mm", body_style), Paragraph("USW00012921", body_style)],
        [Paragraph("2024-05-02", body_style), Paragraph("HARRIS", body_style), Paragraph("1188444", body_style), Paragraph("Flash Flood", body_style), Paragraph("(29.99, -95.28)", body_style), Paragraph("34.8 mm", body_style), Paragraph("USW00012918", body_style)],
        [Paragraph("2024-05-02", body_style), Paragraph("HARRIS", body_style), Paragraph("1188445", body_style), Paragraph("Flash Flood", body_style), Paragraph("(30.05, -95.46)", body_style), Paragraph("34.8 mm", body_style), Paragraph("USW00012918", body_style)],
    ]
    t_ov = Table(overlap_data, colWidths=[65, 55, 75, 80, 85, 65, 79])
    t_ov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ov)

    story.append(Spacer(1, 10))

    # Section 5
    story.append(Paragraph("5. Canonical Mapping & Ingestion Contract Draft", h1_style))
    story.append(Paragraph("The system unifies heterogeneous observations into the canonical <code>event</code> table (event_id, source, event_type, timestamp UTC, latitude, longitude, severity, raw_reference), extended by domain tables <code>flood_event_details</code> (causes, USD damages, fatalities) and <code>precipitation_reading_details</code> (station ID, mm rainfall, interval).", body_style))
    story.append(Paragraph("<b>Historical Strategy:</b> Yearly bulk partitioning of NOAA Storm Events and monthly station queries for GHCN-Daily.<br/><b>Incremental Strategy:</b> Watermark polling every 30m for NWS observations and 5-10m for NWS alerts with a 2-hour lookback window.<br/><b>Failure Recovery:</b> Ingestion operations execute in atomic database transactions. Watermarks advance strictly after commit. Malformed records are diverted to <code>rejected_record</code> (quarantine) without breaking pipeline execution.", body_style))

    story.append(Spacer(1, 10))

    # Section 6
    story.append(Paragraph("6. Flood Risk Index (FRI) Indicator Proposal", h1_style))
    story.append(Paragraph("The <b>Flood Risk Index (FRI)</b> is a calibrated heuristic metric between 0 and 100:", body_style))
    story.append(Paragraph("<b>FRI = 0.45 * I_precip + 0.35 * I_alert + 0.20 * I_hist</b>", ParagraphStyle('Formula', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#2B6CB0"))))
    story.append(Paragraph("Where <i>I_precip</i> measures 24h rainfall against the 95th historical percentile, <i>I_alert</i> encodes active NWS warnings (Watch=35, Warning=75, Flash Flood Emergency=100), and <i>I_hist</i> measures historical flood frequency for the county.", body_style))
    story.append(Paragraph("<b>Output Scale:</b> LOW (0-39), MEDIUM (40-69), HIGH (70-89), CRITICAL (90-100).<br/><b>Historical Validation:</b> Back-tested against the May 2024 Southeast Texas floods and Hurricane Harvey to verify high risk detection ($FRI \\ge 85$).<br/><b>Disclaimer:</b> The index is an operational situational awareness aid, not a deterministic hydrodynamic model.", body_style))

    story.append(Spacer(1, 10))

    # Section 7
    story.append(Paragraph("7. Risks & Mitigations", h1_style))
    story.append(Paragraph("• <b>NWS API Rate Limits:</b> Exponential backoff retries and caching; descriptive User-Agent.<br/>• <b>Missing Coordinates in Alerts:</b> Pre-loaded county boundary lookup linking UGC/SAME codes to centroids.<br/>• <b>NOAA Storm Events Latency:</b> Confined to historical baseline; live tracking driven by NWS feeds.<br/>• <b>Sensor Sparseness:</b> Spatial station averaging and explicit null checks.<br/>• <b>Bulk Ingestion Memory:</b> Batch processing (1,000 rows/commit) and streaming decoders.", body_style))

    story.append(Spacer(1, 10))

    # Section 8
    story.append(Paragraph("8. High-Level Architecture Overview", h1_style))
    story.append(Paragraph("The system runs via Docker Compose with PostgreSQL/PostGIS. Raw data landing zone preserves immutable evidence (<code>data/raw/source_YYYYMMDD_HHMMSS.ext</code>). An ingestion engine normalizes records into canonical and domain tables, while quarantined records enter <code>rejected_record</code>. Plotly Dash visualizes active alerts, precipitation anomalies, and the Flood Risk Index at <code>localhost:8050</code>.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully compiled to {pdf_filename}!")

if __name__ == "__main__":
    build_pdf()
