from datetime import datetime
import os
import json
from . import db

class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    recipients = db.Column(db.Text, nullable=False)  # JSON list
    subject = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    has_attachments = db.Column(db.Boolean, default=False)
    
    def __init__(self, sender, recipients, subject, filename, size, has_attachments=False):
        self.sender = sender
        self.recipients = json.dumps(recipients) if isinstance(recipients, list) else recipients
        self.subject = subject
        self.filename = filename
        self.size = size
        self.has_attachments = has_attachments
    
    @property
    def recipients_list(self):
        """Return recipients as a list."""
        try:
            return json.loads(self.recipients)
        except:
            return []
    
    @property
    def date_formatted(self):
        """Return formatted date string."""
        return self.date.strftime('%Y-%m-%d %H:%M:%S')
    
    def delete_file(self, storage_path):
        """Delete the associated email file."""
        full_path = os.path.join(storage_path, self.filename)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
