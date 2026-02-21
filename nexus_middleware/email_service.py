#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
              🔮 NEXUS PRIME EMAIL SERVICE - SOVEREIGN COMMUNICATIONS
═══════════════════════════════════════════════════════════════════════════════
                      MrF's Universal Email Gateway
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import ssl
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Union
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class EmailConfig:
    """SMTP Configuration"""
    host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port: int = int(os.getenv("SMTP_PORT", "587"))
    user: str = os.getenv("SMTP_USER", "")
    password: str = os.getenv("SMTP_PASS", "")
    from_email: str = os.getenv("SMTP_FROM_EMAIL", "")
    from_name: str = os.getenv("SMTP_FROM_NAME", "NEXUS PRIME")
    use_tls: bool = os.getenv("SMTP_SECURE", "false").lower() != "true"  # TLS for 587


class NexusEmailService:
    """
    ═══════════════════════════════════════════════════════════════════════════
                        THE SOVEREIGN EMAIL GATEWAY
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    def __init__(self, config: Optional[EmailConfig] = None):
        self.config = config or EmailConfig()
        self._validate_config()
    
    def _validate_config(self):
        """Ensure configuration is complete"""
        if not all([self.config.host, self.config.user, self.config.password]):
            print("⚠️ WARNING: SMTP configuration incomplete!")
            print(f"   Host: {'✅' if self.config.host else '❌'}")
            print(f"   User: {'✅' if self.config.user else '❌'}")
            print(f"   Pass: {'✅' if self.config.password else '❌'}")
    
    def send_email(
        self,
        to: Union[str, List[str]],
        subject: str,
        body: str,
        html: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None
    ) -> dict:
        """
        ═══════════════════════════════════════════════════════════════════════
                             SEND SOVEREIGN MESSAGE
        ═══════════════════════════════════════════════════════════════════════
        """
        try:
            # Normalize recipients
            to_list = [to] if isinstance(to, str) else to
            cc_list = [cc] if isinstance(cc, str) else (cc or [])
            bcc_list = [bcc] if isinstance(bcc, str) else (bcc or [])
            
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.config.from_name} <{self.config.from_email}>"
            msg["To"] = ", ".join(to_list)
            
            if cc_list:
                msg["Cc"] = ", ".join(cc_list)
            if reply_to:
                msg["Reply-To"] = reply_to
            
            # Add body
            msg.attach(MIMEText(body, "plain", "utf-8"))
            
            # Add HTML if provided
            if html:
                msg.attach(MIMEText(html, "html", "utf-8"))
            
            # Add attachments
            if attachments:
                for filepath in attachments:
                    self._attach_file(msg, filepath)
            
            # All recipients
            all_recipients = to_list + cc_list + bcc_list
            
            # Send via SMTP
            with smtplib.SMTP(self.config.host, self.config.port) as server:
                server.ehlo()
                if self.config.use_tls:
                    server.starttls()
                    server.ehlo()
                server.login(self.config.user, self.config.password)
                server.sendmail(self.config.from_email, all_recipients, msg.as_string())
            
            return {
                "success": True,
                "message": f"✅ Email sent to {len(all_recipients)} recipients",
                "recipients": all_recipients,
                "subject": subject
            }
            
        except smtplib.SMTPAuthenticationError as e:
            return {
                "success": False,
                "error": "Authentication failed - check SMTP credentials",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "type": type(e).__name__
            }
    
    def _attach_file(self, msg: MIMEMultipart, filepath: str):
        """Attach a file to the email"""
        path = Path(filepath)
        if not path.exists():
            print(f"⚠️ Attachment not found: {filepath}")
            return
        
        with open(filepath, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={path.name}"
        )
        msg.attach(part)
    
    # ═══════════════════════════════════════════════════════════════════════
    #                        TEMPLATE METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def send_alert(self, to: str, alert_type: str, message: str) -> dict:
        """Send system alert email"""
        subject = f"🚨 NEXUS ALERT: {alert_type}"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #16213e; border-radius: 10px; padding: 30px; border: 1px solid #0f3460;">
                <h1 style="color: #e94560; margin: 0 0 20px;">🚨 SYSTEM ALERT</h1>
                <p style="color: #7f8c8d;">Alert Type: <strong style="color: #e74c3c;">{alert_type}</strong></p>
                <div style="background: #0f3460; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; white-space: pre-wrap;">{message}</p>
                </div>
                <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px; border-top: 1px solid #0f3460; padding-top: 15px;">
                    Sent by NEXUS PRIME AI System
                </p>
            </div>
        </body>
        </html>
        """
        return self.send_email(to, subject, message, html=html)
    
    def send_report(self, to: str, report_name: str, report_content: str, attachment_path: Optional[str] = None) -> dict:
        """Send system report email"""
        subject = f"📊 NEXUS REPORT: {report_name}"
        attachments = [attachment_path] if attachment_path else None
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #16213e; border-radius: 10px; padding: 30px; border: 1px solid #0f3460;">
                <h1 style="color: #00d9ff; margin: 0 0 20px;">📊 SYSTEM REPORT</h1>
                <h2 style="color: #fff;">{report_name}</h2>
                <div style="background: #0f3460; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <pre style="margin: 0; white-space: pre-wrap; font-family: monospace;">{report_content}</pre>
                </div>
                <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px; border-top: 1px solid #0f3460; padding-top: 15px;">
                    Generated by NEXUS PRIME AI System
                </p>
            </div>
        </body>
        </html>
        """
        return self.send_email(to, subject, report_content, html=html, attachments=attachments)
    
    def send_welcome(self, to: str, name: str) -> dict:
        """Send welcome email to new user/agent"""
        subject = f"🔮 Welcome to NEXUS PRIME, {name}!"
        body = f"Welcome {name}! You are now part of the NEXUS PRIME collective."
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%); border-radius: 10px; padding: 30px; border: 1px solid #0f3460;">
                <h1 style="color: #00d9ff; margin: 0 0 20px; text-align: center;">🔮 NEXUS PRIME</h1>
                <h2 style="color: #fff; text-align: center;">Welcome, {name}!</h2>
                <p style="text-align: center; color: #aaa;">You are now part of the collective consciousness.</p>
                <div style="background: #0f3460; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <p style="margin: 0; font-size: 18px; color: #00d9ff;">🌟 The Empire Awaits 🌟</p>
                </div>
                <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px; border-top: 1px solid #0f3460; padding-top: 15px; text-align: center;">
                    NEXUS PRIME AI System - MrF's Digital Empire
                </p>
            </div>
        </body>
        </html>
        """
        return self.send_email(to, subject, body, html=html)
    
    def send_status_update(self, to: str, status_data: dict) -> dict:
        """Send system status update"""
        subject = "🟢 NEXUS STATUS UPDATE"
        body = "\n".join([f"{k}: {v}" for k, v in status_data.items()])
        status_html = "".join([
            f'<tr><td style="padding: 10px; border-bottom: 1px solid #0f3460;">{k}</td>'
            f'<td style="padding: 10px; border-bottom: 1px solid #0f3460; color: #00d9ff;">{v}</td></tr>'
            for k, v in status_data.items()
        ])
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #16213e; border-radius: 10px; padding: 30px; border: 1px solid #0f3460;">
                <h1 style="color: #00ff88; margin: 0 0 20px;">🟢 SYSTEM STATUS</h1>
                <table style="width: 100%; border-collapse: collapse;">
                    {status_html}
                </table>
                <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px; border-top: 1px solid #0f3460; padding-top: 15px;">
                    NEXUS PRIME Monitoring System
                </p>
            </div>
        </body>
        </html>
        """
        return self.send_email(to, subject, body, html=html)


# ═══════════════════════════════════════════════════════════════════════════════
#                          ASYNC EMAIL SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

async def send_email_async(
    to: Union[str, List[str]],
    subject: str,
    body: str,
    **kwargs
) -> dict:
    """Async wrapper for email sending"""
    service = NexusEmailService()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: service.send_email(to, subject, body, **kwargs)
    )


# ═══════════════════════════════════════════════════════════════════════════════
#                                 CLI / TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_email():
    """Test email configuration"""
    print("═" * 60)
    print("        🔮 NEXUS EMAIL SERVICE TEST")
    print("═" * 60)
    
    service = NexusEmailService()
    print(f"\n📧 SMTP Host: {service.config.host}")
    print(f"📧 SMTP Port: {service.config.port}")
    print(f"📧 SMTP User: {service.config.user}")
    print(f"📧 From: {service.config.from_name} <{service.config.from_email}>")
    print(f"📧 TLS: {'Enabled' if service.config.use_tls else 'Disabled'}")
    
    # Send test email
    print("\n📤 Sending test email...")
    result = service.send_email(
        to=service.config.from_email,  # Send to self
        subject="🔮 NEXUS PRIME - Test Email",
        body="This is a test email from NEXUS PRIME Email Service.\n\nIf you received this, the email system is working correctly!",
        html="""
        <html>
        <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%); border-radius: 10px; padding: 30px; border: 1px solid #e94560;">
                <h1 style="color: #00d9ff; margin: 0 0 20px; text-align: center;">🔮 NEXUS PRIME</h1>
                <h2 style="color: #00ff88; text-align: center;">✅ Email System Working!</h2>
                <p style="text-align: center; color: #aaa;">Your email configuration is correct.</p>
                <div style="background: #0f3460; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <p style="margin: 0; font-size: 24px;">🚀 THE EMPIRE IS CONNECTED 🚀</p>
                </div>
            </div>
        </body>
        </html>
        """
    )
    
    if result["success"]:
        print(f"\n✅ {result['message']}")
    else:
        print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
        if 'details' in result:
            print(f"   Details: {result['details']}")
    
    return result


if __name__ == "__main__":
    test_email()
