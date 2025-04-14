#!/usr/bin/env python3
"""
Test script to send an email to the Fauxmots SMTP server.
"""

import smtplib
import argparse
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parse_args():
    parser = argparse.ArgumentParser(description='Send a test email to the Fauxmots SMTP server')
    parser.add_argument('--host', default='127.0.0.1', help='SMTP server host')
    parser.add_argument('--port', type=int, default=1025, help='SMTP server port')
    parser.add_argument('--from', dest='from_addr', default='sender@example.com', help='From address')
    parser.add_argument('--to', dest='to_addr', default='recipient@example.com', help='To address')
    parser.add_argument('--subject', default='Test Email', help='Email subject')
    parser.add_argument('--html', action='store_true', help='Send HTML email')
    return parser.parse_args()

def main():
    args = parse_args()
    
    print(f"Sending test email to {args.host}:{args.port}...")
    
    if args.html:
        # Create a multipart message with HTML
        msg = MIMEMultipart('alternative')
        msg['Subject'] = args.subject
        msg['From'] = args.from_addr
        msg['To'] = args.to_addr
        
        # Plain text version
        text_content = "This is a test email from the Fauxmots test script.\n\nHello World!"
        part1 = MIMEText(text_content, 'plain')
        
        # HTML version
        html_content = """
        <html>
          <head></head>
          <body>
            <h1>Test Email</h1>
            <p>This is a <b>test email</b> from the Fauxmots test script.</p>
            <p>Hello <span style="color: blue;">World</span>!</p>
          </body>
        </html>
        """
        part2 = MIMEText(html_content, 'html')
        
        # Add parts to message
        msg.attach(part1)
        msg.attach(part2)
    else:
        # Simple plain text message
        msg = EmailMessage()
        msg.set_content("This is a test email from the Fauxmots test script.\n\nHello World!")
        msg['Subject'] = args.subject
        msg['From'] = args.from_addr
        msg['To'] = args.to_addr
    
    try:
        with smtplib.SMTP(args.host, args.port) as server:
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
