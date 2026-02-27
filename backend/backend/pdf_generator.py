from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def get_hebrew_year():
    return datetime.now().year + 3760

def generate_dream_pdf(name: str, report: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Times-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Italic'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#d4af37'),
        spaceAfter=12,
        fontName='Times-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        spaceAfter=12,
        textColor=colors.HexColor('#2c1810')
    )
    
    scripture_style = ParagraphStyle(
        'ScriptureStyle',
        parent=styles['Italic'],
        fontSize=11,
        textColor=colors.HexColor('#1a1a2e'),
        alignment=TA_CENTER,
        spaceAfter=6,
        leftIndent=20,
        rightIndent=20
    )
    
    # Header
    story.append(Paragraph(f"The Revelation of {name}", title_style))
    story.append(Paragraph("A Biblical Interpretation", subtitle_style))
    story.append(Paragraph(f"Interpreted on {datetime.now().strftime('%B %d, %Y')} | Hebrew Year {get_hebrew_year()}", 
                          subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Quote
    story.append(Paragraph('"In the last days, God says, I will pour out my Spirit on all people..." — Acts 2:17', 
                          subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Three Revelations
    story.append(Paragraph("Three Revelations", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    for interp in report['interpretations']:
        story.append(Paragraph(f"<b>{interp['title']}</b>", body_style))
        story.append(Paragraph(interp['meaning'], body_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Scripture
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Scriptural Anchor", heading_style))
    
    scripture_data = [[
        Paragraph(f'"{report["scripture"]["text"]}"', scripture_style)
    ], [
        Paragraph(f"<b>{report['scripture']['reference']}</b>", 
                 ParagraphStyle('Ref', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor('#d4af37')))
    ], [
        Paragraph(report['scripture']['context'], 
                 ParagraphStyle('Context', parent=body_style, alignment=TA_CENTER, fontSize=9, textColor=colors.HexColor('#666666')))
    ]]
    
    scripture_table = Table(scripture_data, colWidths=[6*inch])
    scripture_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f4f1ea')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d4af37')),
        ('PADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(scripture_table)
    
    # Prayer
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("A Prayer for Your Dream", heading_style))
    
    prayer_data = [[
        Paragraph(report['prayer'], 
                 ParagraphStyle('Prayer', parent=body_style, textColor=colors.HexColor('#1a1a2e'), 
                              alignment=TA_CENTER, fontSize=12))
    ]]
    
    prayer_table = Table(prayer_data, colWidths=[6*inch])
    prayer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d4af37')),
        ('PADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(prayer_table)
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph('"Do not interpretations belong to God?" — Genesis 40:8', 
                          ParagraphStyle('Footer', parent=subtitle_style, fontSize=10)))
    story.append(Paragraph('<b>DreamDecode</b> | Biblical Dream Interpretation', 
                          ParagraphStyle('Footer2', parent=subtitle_style, fontSize=9)))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
