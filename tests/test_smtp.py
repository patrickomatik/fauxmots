import os
import unittest
import tempfile
import smtplib
import time
from email.message import EmailMessage
from app import create_app, db
from app.smtp_server import SMTPController
from app.models import Email

class SMTPTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a running SMTP server for testing."""
        # Create a temporary directory for email storage
        cls.temp_dir = tempfile.mkdtemp()
        
        # Configure test application
        cls.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'EMAIL_STORAGE_PATH': cls.temp_dir,
            'SMTP_HOST': '127.0.0.1',
            'SMTP_PORT': 19025  # Use a non-standard port for testing
        })
        
        # Initialize database
        with cls.app.app_context():
            db.create_all()
            
        # Start SMTP server
        with cls.app.app_context():
            cls.smtp_controller = SMTPController(cls.app)
            cls.smtp_controller.start()
        
        # Give it a moment to start up
        time.sleep(1)
    
    @classmethod
    def tearDownClass(cls):
        """Stop the SMTP server and clean up."""
        # Stop SMTP server
        cls.smtp_controller.stop()
        
        # Clean up temporary directory
        for filename in os.listdir(cls.temp_dir):
            os.unlink(os.path.join(cls.temp_dir, filename))
        os.rmdir(cls.temp_dir)
    
    def setUp(self):
        """Set up test client and clean database before each test."""
        self.client = self.app.test_client()
        
        # Clean up any emails from previous tests
        with self.app.app_context():
            db.session.query(Email).delete()
            db.session.commit()
    
    def send_test_email(self, subject="Test Subject", body="This is a test email."):
        """Utility method to send a test email to our SMTP server."""
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = 'sender@example.com'
        msg['To'] = 'recipient@example.com'
        
        # Connect to our SMTP server and send the message
        try:
            with smtplib.SMTP('127.0.0.1', 19025) as server:
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def test_smtp_server_running(self):
        """Test that the SMTP server is running and accepting connections."""
        try:
            with smtplib.SMTP('127.0.0.1', 19025) as server:
                status = server.noop()[0]
                self.assertEqual(status, 250)
        except:
            self.fail("Could not connect to SMTP server")
    
    def test_send_and_receive_email(self):
        """Test sending an email and verifying it's saved and appears in the web interface."""
        # Send a test email
        subject = "Integration Test"
        body = "This is an integration test email."
        self.assertTrue(self.send_test_email(subject, body))
        
        # Allow a brief moment for processing
        time.sleep(0.5)
        
        # Check database for the email
        with self.app.app_context():
            emails = Email.query.all()
            self.assertEqual(len(emails), 1)
            self.assertEqual(emails[0].sender, 'sender@example.com')
            self.assertEqual(emails[0].subject, subject)
            
            # Check file exists
            file_path = os.path.join(self.temp_dir, emails[0].filename)
            self.assertTrue(os.path.exists(file_path))
            
            # Check file content
            with open(file_path, 'r') as f:
                content = f.read()
                self.assertIn(subject, content)
                self.assertIn(body, content)
        
        # Check web interface shows the email
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(subject.encode(), response.data)
        self.assertIn('sender@example.com'.encode(), response.data)
    
    def test_multiple_recipients(self):
        """Test sending an email to multiple recipients."""
        msg = EmailMessage()
        msg.set_content("Email to multiple recipients")
        msg['Subject'] = "Multiple Recipients Test"
        msg['From'] = 'sender@example.com'
        msg['To'] = 'recipient1@example.com, recipient2@example.com'
        msg['Cc'] = 'cc@example.com'
        
        with smtplib.SMTP('127.0.0.1', 19025) as server:
            server.send_message(msg)
        
        # Allow a brief moment for processing
        time.sleep(0.5)
        
        # Check database
        with self.app.app_context():
            emails = Email.query.all()
            self.assertEqual(len(emails), 1)
            
            # Check recipients list contains all recipients
            recipients = emails[0].recipients_list
            self.assertEqual(len(recipients), 3)
            self.assertIn('recipient1@example.com', recipients)
            self.assertIn('recipient2@example.com', recipients)
            self.assertIn('cc@example.com', recipients)
    
    def test_html_email(self):
        """Test sending an HTML email."""
        msg = EmailMessage()
        msg['Subject'] = "HTML Email Test"
        msg['From'] = 'sender@example.com'
        msg['To'] = 'recipient@example.com'
        
        # Add HTML content
        html_content = """
        <html>
            <body>
                <h1>HTML Email</h1>
                <p>This is an <b>HTML</b> email test.</p>
            </body>
        </html>
        """
        msg.add_alternative(html_content, subtype='html')
        
        with smtplib.SMTP('127.0.0.1', 19025) as server:
            server.send_message(msg)
        
        # Allow a brief moment for processing
        time.sleep(0.5)
        
        # Check email was received
        with self.app.app_context():
            emails = Email.query.all()
            self.assertEqual(len(emails), 1)
            
            # Check file exists
            file_path = os.path.join(self.temp_dir, emails[0].filename)
            self.assertTrue(os.path.exists(file_path))
        
        # Check detail view shows HTML content
        with self.app.app_context():
            email_id = Email.query.first().id
            
        response = self.client.get(f'/email/{email_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HTML Email', response.data)
        self.assertIn(b'html-content', response.data)  # HTML tab should be present

if __name__ == '__main__':
    unittest.main()
