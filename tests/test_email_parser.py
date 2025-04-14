import os
import unittest
import tempfile
from app.email_parser import decode_value, parse_payload, parse_email_file

class EmailParserTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temp directory
        for filename in os.listdir(self.temp_dir):
            os.unlink(os.path.join(self.temp_dir, filename))
        os.rmdir(self.temp_dir)
    
    def test_decode_value(self):
        self.assertEqual(decode_value(None), "")
        self.assertEqual(decode_value("Simple text"), "Simple text")
        
        # Test encoded header
        value = "=?utf-8?q?Test=20Subject?="
        self.assertEqual(decode_value(value), "Test Subject")
    
    def test_parse_email_file(self):
        # Create a simple test email file
        email_content = """From: sender@example.com
To: recipient@example.com
Subject: Test Email
Date: Mon, 01 Jan 2023 12:00:00 +0000
Content-Type: text/plain; charset="utf-8"

This is a test email body.
Hello world!
"""
        
        email_path = os.path.join(self.temp_dir, 'test_email.eml')
        with open(email_path, 'w') as f:
            f.write(email_content)
        
        result = parse_email_file(email_path)
        
        # Check headers
        self.assertEqual(result['headers']['From'], 'sender@example.com')
        self.assertEqual(result['headers']['To'], 'recipient@example.com')
        self.assertEqual(result['headers']['Subject'], 'Test Email')
        
        # Check body
        self.assertIn('This is a test email body.', result['body']['text/plain'])
        self.assertIn('Hello world!', result['body']['text/plain'])
        
        # No attachments should be found
        self.assertEqual(len(result['attachments']), 0)
    
    def test_parse_email_with_attachment(self):
        # Create a multipart email with attachment
        email_content = """From: sender@example.com
To: recipient@example.com
Subject: Email with Attachment
Date: Mon, 01 Jan 2023 12:00:00 +0000
Content-Type: multipart/mixed; boundary="boundary-string"

--boundary-string
Content-Type: text/plain; charset="utf-8"

This is the body text.

--boundary-string
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="test.txt"
Content-Transfer-Encoding: base64

VGhpcyBpcyBhIHRlc3QgYXR0YWNobWVudC4=

--boundary-string--
"""
        
        email_path = os.path.join(self.temp_dir, 'email_with_attachment.eml')
        with open(email_path, 'w') as f:
            f.write(email_content)
        
        result = parse_email_file(email_path)
        
        # Check headers
        self.assertEqual(result['headers']['Subject'], 'Email with Attachment')
        
        # Check body
        self.assertIn('This is the body text.', result['body']['text/plain'])
        
        # Check attachment
        self.assertEqual(len(result['attachments']), 1)
        self.assertEqual(result['attachments'][0]['filename'], 'test.txt')
        self.assertEqual(result['attachments'][0]['content_type'], 'application/octet-stream')

if __name__ == '__main__':
    unittest.main()
