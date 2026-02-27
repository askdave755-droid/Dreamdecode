from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
import io

def get_hebrew_year():
    """Convert current Gregorian year to Hebrew year (approximate)"""
    gregorian_year = datetime.now().year
    hebrew_year = gregorian_year + 3760
    return f"5770s"  # Simplified - you can make this more accurate if needed

def generate_dream_pdf(name: str, report: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#D4AF37'),
        alignment=1,  # Center
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )
    
    scripture_style = ParagraphStyle(
        'Scripture',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=20,
        rightIndent=20,
        textColor=colors.HexColor('#555555'),
        fontName='Times-Italic'
    )
    
    # Header
    story.append(Paragraph("DreamDecode", title_style))
    story.append(Paragraph(f"Prophetic Revelation for {name}", heading_style))
    story.append(Paragraph(f"Hebrew Year: {get_hebrew_year()}", body_style))
    story.append(Spacer(1, 20))
    
    # Interpretations
    story.append(Paragraph("Interpretations", heading_style))
    for interp in report.get('interpretations', []):
        story.append(Paragraph(f"<b>{interp['title']}</b>", body_style))
        story.append(Paragraph(interp['meaning'], body_style))
        story.append(Spacer(1, 10))
    
    # Scripture
    if 'scripture' in report:
        story.append(Paragraph("Scriptural Foundation", heading_style))
        scripture = report['scripture']
        story.append(Paragraph(
            f"<i>{scripture['reference']}</i><br/>{scripture['text']}", 
            scripture_style
        ))
        story.append(Paragraph(scripture['context'], body_style))
        story.append(Spacer(1, 10))
    
    # Prayer
    if 'prayer' in report:
        story.append(Paragraph("Personalized Prayer", heading_style))
        story.append(Paragraph(report['prayer'], body_style))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<i>This interpretation is provided for spiritual guidance and encouragement.</i>",
        ParagraphStyle('Footer', parent=body_style, fontSize=9, textColor=colors.grey)
    ))
    
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
