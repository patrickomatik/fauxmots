import os
import unittest
import tempfile
from app import create_app, db
from app.models import Email

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.temp_dir = tempfile.mkdtemp()
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///{self.db_path}',
            'EMAIL_STORAGE_PATH': self.temp_dir,
            'SMTP_HOST': '127.0.0.1',
            'SMTP_PORT': 1025
        })
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
        
        # Clean up temp directory
        for filename in os.listdir(self.temp_dir):
            os.unlink(os.path.join(self.temp_dir, filename))
        os.rmdir(self.temp_dir)
    
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fauxmots', response.data)
        self.assertIn(b'No emails received yet', response.data)
    
    def test_api_config(self):
        response = self.client.get('/api/config')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['smtp_host'], '127.0.0.1')
        self.assertEqual(json_data['smtp_port'], 1025)
    
    def test_api_emails(self):
        response = self.client.get('/api/emails')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('emails', json_data)
        self.assertEqual(len(json_data['emails']), 0)  # No emails yet
    
    def test_email_listing(self):
        # Add a test email
        with self.app.app_context():
            email = Email(
                sender='test@example.com',
                recipients=['recipient@example.com'],
                subject='Test Subject',
                filename='test_email.eml',
                size=1024
            )
            db.session.add(email)
            db.session.commit()
            
            # Create a dummy email file
            with open(os.path.join(self.temp_dir, 'test_email.eml'), 'w') as f:
                f.write('From: test@example.com\r\nTo: recipient@example.com\r\nSubject: Test Subject\r\n\r\nThis is a test email.')
        
        # Test listing
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test@example.com', response.data)
        self.assertIn(b'Test Subject', response.data)
        
        # Test API listing
        response = self.client.get('/api/emails')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data['emails']), 1)
        self.assertEqual(json_data['emails'][0]['sender'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()
