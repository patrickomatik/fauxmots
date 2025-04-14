import os
import asyncio
import email
import json
import time
import uuid
from email.parser import BytesParser
from email.policy import default
from datetime import datetime
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as Server

from . import db
from .models import Email

class MessageHandler:
    def __init__(self, storage_path, app=None):
        self.storage_path = storage_path
        self.app = app
        
    async def handle_DATA(self, server, session, envelope):
        """Handle incoming email data."""
        # Parse the message
        message_data = envelope.content
        message = BytesParser(policy=default).parsebytes(message_data)
        
        # Extract headers
        sender = envelope.mail_from
        recipients = envelope.rcpt_tos
        subject = str(message.get('subject', ''))
        
        # Generate a unique filename
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.eml"
        file_path = os.path.join(self.storage_path, filename)
        
        # Write the raw email to file
        with open(file_path, 'wb') as f:
            f.write(message_data)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Check if email has attachments
        has_attachments = False
        for part in message.walk():
            if part.get_filename():
                has_attachments = True
                break
        
        # Create database record
        if self.app:
            with self.app.app_context():
                email_record = Email(
                    sender=sender,
                    recipients=recipients,
                    subject=subject,
                    filename=filename,
                    size=file_size,
                    has_attachments=has_attachments
                )
                db.session.add(email_record)
                db.session.commit()
        
        return '250 Message accepted for delivery'

class SMTPController:
    def __init__(self, app):
        self.app = app
        self.controller = None
        
    def start(self):
        """Start the SMTP server."""
        if self.controller:
            return
            
        host = self.app.config.get('SMTP_HOST', '127.0.0.1')
        port = self.app.config.get('SMTP_PORT', 1025)
        storage_path = self.app.config.get('EMAIL_STORAGE_PATH')
        
        handler = MessageHandler(storage_path, self.app)
        self.controller = Controller(
            handler,
            hostname=host,
            port=port
        )
        self.controller.start()
        
        print(f"SMTP server started on {host}:{port}")
        return True
        
    def stop(self):
        """Stop the SMTP server."""
        if self.controller:
            self.controller.stop()
            self.controller = None
            print("SMTP server stopped")
            return True
        return False
