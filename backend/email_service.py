from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import os
import base64

def send_dream_email(to_email: str, name: str, report: dict, pdf_bytes: bytes, referral_code: str):
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    
    interpretations_html = "".join([
        f"<h3>{i['title']}</h3><p>{i['meaning']}</p>" 
        for i in report.get('interpretations', [])
    ])
    
    scripture = report.get('scripture', {})
    scripture_html = f"""
    <h3>Scriptural Foundation</h3>
    <p><i>{scripture.get('reference', '')}</i></p>
    <p>{scripture.get('text', '')}</p>
    <p>{scripture.get('context', '')}</p>
    """ if scripture else ""
    
    prayer = report.get('prayer', '')
    prayer_html = f"<h3>Personalized Prayer</h3><p>{prayer}</p>" if prayer else ""
    
    html_content = f"""
    <div style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; color: #2C3E50;">
        <h2 style="color: #D4AF37; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">
            Your Dream Revelation
        </h2>
        <p>Dear {name},</p>
        <p>As Joseph interpreted dreams in Egypt, and Daniel in Babylon, here is your divine revelation:</p>
        
        {interpretations_html}
        {scripture_html}
        {prayer_html}
        
        <div style="background-color: #F8F9FA; padding: 20px; border-left: 4px solid #D4AF37; margin-top: 30px;">
            <h3 style="margin-top: 0; color: #2C3E50;">Share the Blessing</h3>
            <p>Your personal blessing code: <strong style="font-size: 20px; color: #D4AF37;">{referral_code}</strong></p>
            <p>Share this with friends and family. They receive 50% off, and you receive heavenly rewards.</p>
        </div>
        
        <p style="font-size: 12px; color: #666; margin-top: 30px;">
            PDF attached for your records. Keep this revelation in a sacred place.
        </p>
    </div>
    """
    
    message = Mail(
        from_email=os.getenv('FROM_EMAIL'),
        to_emails=to_email,
        subject='Your Biblical Dream Interpretation Has Arrived',
        html_content=html_content
    )
    
    # Attach PDF
    encoded = base64.b64encode(pdf_bytes).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_name = FileName(f"dream-revelation-{referral_code}.pdf")
    attachment.file_type = FileType("application/pdf")
    attachment.disposition = Disposition("attachment")
    message.attachment = attachment
    
    try:
        response = sg.send(message)
        print(f"Email sent successfully: {response.status_code}")
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

def send_referrer_notification(referrer_email: str, referrer_name: str, new_person_name: str):
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    
    html_content = f"""
    <div style="font-family: Georgia, serif; max-width: 600px;">
        <h2 style="color: #D4AF37;">Blessing Multiplied!</h2>
        <p>Dear {referrer_name},</p>
        <p>Wonderful news! <strong>{new_person_name}</strong> has used your blessing code to receive their dream interpretation.</p>
        <p>As Scripture says: "The one who blesses others is abundantly blessed" (Proverbs 11:25).</p>
        <p>Your referral count has increased. Thank you for spreading the light.</p>
    </div>
    """
    
    message = Mail(
        from_email=os.getenv('FROM_EMAIL'),
        to_emails=referrer_email,
        subject='Someone Used Your DreamDecode Blessing Code!',
        html_content=html_content
    )
    
    try:
        sg.send(message)
        return True
    except Exception as e:
        print(f"Referrer email error: {str(e)}")
        return False
